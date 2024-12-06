import asyncio
import os
import shutil
from exponent.core.remote_execution.languages.types import (
    StreamedOutputPiece,
    ShellExecutionResult,
)
from typing import Optional, Callable, AsyncGenerator, Union


STDOUT_FD = 1
STDERR_FD = 2
MAX_TIMEOUT = 300


async def read_stream(
    stream: asyncio.StreamReader, fd: int, output: list[tuple[int, str]]
) -> AsyncGenerator[StreamedOutputPiece, None]:
    while True:
        try:
            data = await stream.read(4096)
            if not data:
                break
            chunk = data.decode()
            output.append((fd, chunk))
            yield StreamedOutputPiece(content=chunk)
        except asyncio.CancelledError:
            raise
        except Exception:
            break


async def execute_shell_streaming(
    code: str,
    working_directory: str,
    timeout: int,
    should_halt: Optional[Callable[[], bool]] = None,
) -> AsyncGenerator[Union[StreamedOutputPiece, ShellExecutionResult], None]:
    timeout_seconds = min(timeout, MAX_TIMEOUT)

    shell_path = (
        os.environ.get("SHELL")
        or shutil.which("bash")
        or shutil.which("sh")
        or "/bin/sh"
    )

    process = await asyncio.create_subprocess_exec(
        shell_path,
        "-l",
        "-c",
        code,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=working_directory,
    )

    exit_code = None
    output: list[tuple[int, str]] = []
    halted = False
    timed_out = False
    assert process.stdout
    assert process.stderr

    async def monitor_halt() -> None:
        nonlocal halted
        while True:
            if should_halt and should_halt():
                process.kill()
                halted = True
                break
            if process.returncode is not None:
                break
            await asyncio.sleep(0.1)

    def on_timeout() -> None:
        nonlocal timed_out
        timed_out = True
        process.kill()

    try:
        halt_task = asyncio.create_task(monitor_halt()) if should_halt else None
        timeout_handle = asyncio.get_running_loop().call_later(
            timeout_seconds, on_timeout
        )

        # Stream stdout and stderr concurrently using wait
        stdout_gen = read_stream(process.stdout, STDOUT_FD, output)
        stderr_gen = read_stream(process.stderr, STDERR_FD, output)

        stdout_task = asyncio.create_task(stdout_gen.__anext__())
        stderr_task = asyncio.create_task(stderr_gen.__anext__())
        pending = {stdout_task, stderr_task}

        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                try:
                    piece = await task
                    yield piece

                    # Schedule next read from the same stream
                    if task is stdout_task and not process.stdout.at_eof():
                        stdout_task = asyncio.create_task(stdout_gen.__anext__())
                        pending.add(stdout_task)
                    elif task is stderr_task and not process.stderr.at_eof():
                        stderr_task = asyncio.create_task(stderr_gen.__anext__())
                        pending.add(stderr_task)
                except StopAsyncIteration:
                    continue

        exit_code = await process.wait()
        timeout_handle.cancel()

    except asyncio.CancelledError:
        process.kill()
        raise
    finally:
        if halt_task and not halt_task.done():
            halt_task.cancel()
            try:
                await halt_task
            except asyncio.CancelledError:
                pass

    formatted_output = "".join([chunk for (_, chunk) in output]).strip() + "\n\n"

    yield ShellExecutionResult(
        output=formatted_output,
        cancelled_for_timeout=timed_out,
        exit_code=None if timed_out else exit_code,
        halted=halted,
    )
