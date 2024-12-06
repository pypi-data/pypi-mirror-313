import asyncio
import os
import shutil
from dataclasses import dataclass
from typing import Optional, Callable

STDOUT_FD = 1
STDERR_FD = 2
MAX_TIMEOUT = 300


"""
Deprecated, use shell_streaming.py
"""


@dataclass
class ShellExecutionResult:
    output: str
    cancelled_for_timeout: bool
    exit_code: Optional[int]
    halted: bool = False


async def execute_shell(
    code: str,
    working_directory: str,
    timeout: int,
    should_halt: Optional[Callable[[], bool]] = None,
) -> ShellExecutionResult:
    timeout = min(timeout, MAX_TIMEOUT)

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
    assert process.stdout
    assert process.stderr

    stdout_capture_task = asyncio.create_task(
        capture(process.stdout, STDOUT_FD, output)
    )
    stderr_capture_task = asyncio.create_task(
        capture(process.stderr, STDERR_FD, output)
    )

    async def capture_until_exit() -> int:
        nonlocal halted
        while True:
            if should_halt and should_halt():
                process.kill()
                halted = True
                break

            if process.returncode is not None:
                break

            await asyncio.sleep(0.1)

        return await process.wait()

    try:
        exit_code = await asyncio.wait_for(capture_until_exit(), timeout)
    except (TimeoutError, asyncio.TimeoutError):  # noqa: UP041
        process.kill()
    except Exception:
        raise
    finally:
        # Wait for capture tasks to complete naturally after streams are closed
        await asyncio.gather(
            stdout_capture_task, stderr_capture_task, return_exceptions=True
        )

    formatted_output = "".join([chunk for (_, chunk) in output]).strip() + "\n\n"

    return ShellExecutionResult(
        output=formatted_output,
        cancelled_for_timeout=exit_code is None and not halted,
        exit_code=exit_code,
        halted=halted,
    )


async def capture(
    stream: asyncio.StreamReader, fd: int, output: list[tuple[int, str]]
) -> None:
    while True:
        data = await stream.read(4096)
        if not data:
            break

        chunk = data.decode()
        output.append((fd, chunk))
