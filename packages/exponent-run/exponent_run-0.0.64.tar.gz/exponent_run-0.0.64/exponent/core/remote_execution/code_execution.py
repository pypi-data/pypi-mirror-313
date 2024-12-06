from typing import Optional, Callable, AsyncGenerator, Union
from exponent.core.remote_execution.languages.python_execution import (
    execute_python,
    execute_python_streaming,
)
from exponent.core.remote_execution.languages.shell import execute_shell
from exponent.core.remote_execution.languages.shell_streaming import (
    execute_shell_streaming,
)
from exponent.core.remote_execution.languages.types import StreamedOutputPiece
from exponent.core.remote_execution.session import RemoteExecutionClientSession
from exponent.core.remote_execution.types import (
    CodeExecutionRequest,
    CodeExecutionResponse,
    StreamingCodeExecutionResponse,
    StreamingCodeExecutionResponseChunk,
    StreamingCodeExecutionRequest,
)

from exponent.core.remote_execution.utils import assert_unreachable

EMPTY_OUTPUT_STRING = "(No output)"


async def execute_code(
    request: CodeExecutionRequest,
    session: RemoteExecutionClientSession,
    working_directory: str,
    should_halt: Optional[Callable[[], bool]] = None,
) -> CodeExecutionResponse:
    try:
        if request.language == "python":
            output = await execute_python(request.content, session.kernel)
            return CodeExecutionResponse(
                content=output or EMPTY_OUTPUT_STRING,
                correlation_id=request.correlation_id,
            )
        elif request.language == "shell":
            result = await execute_shell(
                request.content, working_directory, request.timeout, should_halt
            )
            return CodeExecutionResponse(
                content=result.output or EMPTY_OUTPUT_STRING,
                cancelled_for_timeout=result.cancelled_for_timeout,
                exit_code=result.exit_code,
                correlation_id=request.correlation_id,
                halted=result.halted,
            )

        return assert_unreachable(request.language)

    except Exception as e:  # noqa: BLE001 - TODO (Josh): Specialize errors for execution
        return CodeExecutionResponse(
            content="An error occurred while executing the code: " + str(e),
            correlation_id=request.correlation_id,
        )


async def execute_code_streaming(
    request: StreamingCodeExecutionRequest,
    session: RemoteExecutionClientSession,
    working_directory: str,
    should_halt: Optional[Callable[[], bool]] = None,
) -> AsyncGenerator[
    Union[StreamingCodeExecutionResponseChunk, StreamingCodeExecutionResponse], None
]:
    if request.language == "python":
        async for output in execute_python_streaming(
            request.content, session.kernel, user_interrupted=should_halt
        ):
            if isinstance(output, StreamedOutputPiece):
                yield StreamingCodeExecutionResponseChunk(
                    content=output.content, correlation_id=request.correlation_id
                )
            else:
                yield StreamingCodeExecutionResponse(
                    correlation_id=request.correlation_id,
                    content=output.output or EMPTY_OUTPUT_STRING,
                    halted=output.halted,
                )

    elif request.language == "shell":
        async for shell_output in execute_shell_streaming(
            request.content, working_directory, request.timeout, should_halt
        ):
            if isinstance(shell_output, StreamedOutputPiece):
                yield StreamingCodeExecutionResponseChunk(
                    content=shell_output.content, correlation_id=request.correlation_id
                )
            else:
                yield StreamingCodeExecutionResponse(
                    correlation_id=request.correlation_id,
                    content=shell_output.output or EMPTY_OUTPUT_STRING,
                    halted=shell_output.halted,
                    exit_code=shell_output.exit_code,
                    cancelled_for_timeout=shell_output.cancelled_for_timeout,
                )
