from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Optional, TypeVar, Union, Dict

from dataclasses import dataclass
from exponent.core.remote_execution.error_info import serialize_error_info
from exponent.core.types.event_types import (
    CodeBlockEvent,
    CommandEvent,
    FileWriteEvent,
    LocalEventType,
)
import websockets.client
import websockets.exceptions
from httpx import (
    AsyncClient,
    codes as http_status,
)
from pydantic import BaseModel

from exponent.commands.utils import ConnectionTracker
from exponent.core.remote_execution import files, system_context
from exponent.core.remote_execution.code_execution import (
    execute_code,
    execute_code_streaming,
)
from exponent.core.remote_execution.command_execution import execute_command
from exponent.core.remote_execution.file_write import execute_file_write
from exponent.core.remote_execution.session import (
    RemoteExecutionClientSession,
    get_session,
)
from exponent.core.remote_execution.types import (
    CLIConnectedState,
    CodeExecutionRequest,
    StreamingCodeExecutionRequest,
    CommandRequest,
    CreateChatResponse,
    ExecutionEndResponse,
    FileWriteRequest,
    GetAllTrackedFilesRequest,
    GetFileAttachmentRequest,
    GetFileAttachmentsRequest,
    GetMatchingFilesRequest,
    HaltRequest,
    HaltResponse,
    HeartbeatInfo,
    ListFilesRequest,
    RemoteExecutionRequestType,
    RemoteExecutionResponseType,
    RunWorkflowRequest,
    StartChatRequest,
    StartChatResponse,
    SwitchCLIChatRequest,
    SwitchCLIChatResponse,
    SystemContextRequest,
    UseToolsConfig,
    ErrorResponse,
)
from exponent.core.remote_execution.utils import (
    convert_event_to_execution_request,
    deserialize_api_response,
    deserialize_request_data,
    serialize_message,
)

logger = logging.getLogger(__name__)


TModel = TypeVar("TModel", bound=BaseModel)


@dataclass
class WSDisconnected:
    pass


@dataclass
class SwitchCLIChat:
    new_chat_uuid: str


REMOTE_EXECUTION_CLIENT_EXIT_INFO = Union[WSDisconnected, SwitchCLIChat]


class RemoteExecutionClient:
    def __init__(
        self,
        session: RemoteExecutionClientSession,
    ):
        self.current_session = session

        self.file_cache: files.FileCache = files.FileCache(session.working_directory)

        # for active code executions, track whether they should be halted
        # correlation_id -> should_halt
        self._halt_states: Dict[str, bool] = {}
        self._halt_lock = asyncio.Lock()

    @property
    def working_directory(self) -> str:
        return self.current_session.working_directory

    @property
    def api_client(self) -> AsyncClient:
        return self.current_session.api_client

    @property
    def ws_client(self) -> AsyncClient:
        return self.current_session.ws_client

    async def add_code_execution_to_halt_states(self, correlation_id: str) -> None:
        async with self._halt_lock:
            self._halt_states[correlation_id] = False

    async def halt_all_code_executions(self) -> None:
        async with self._halt_lock:
            self._halt_states = {
                correlation_id: True for correlation_id in self._halt_states.keys()
            }

    async def clear_halt_state(self, correlation_id: str) -> None:
        async with self._halt_lock:
            self._halt_states.pop(correlation_id, None)

    def get_halt_check(self, correlation_id: str) -> Callable[[], bool]:
        def should_halt() -> bool:
            # Don't need to lock here, since just reading from dict
            return self._halt_states.get(correlation_id, False)

        return should_halt

    async def run_connection(  # noqa: PLR0915,PLR0912
        self,
        chat_uuid: str,
        connection_tracker: Optional[ConnectionTracker] = None,
    ) -> REMOTE_EXECUTION_CLIENT_EXIT_INFO:
        self.current_session.set_chat_uuid(chat_uuid)

        async for websocket in self.ws_connect(
            f"/api/ws/chat/{chat_uuid}",
        ):
            if connection_tracker is not None:
                await connection_tracker.set_connected(True)

            beats: asyncio.Queue[HeartbeatInfo] = asyncio.Queue()
            requests: asyncio.Queue[RemoteExecutionRequestType] = asyncio.Queue()
            results: asyncio.Queue[RemoteExecutionResponseType] = asyncio.Queue()

            async def beat() -> None:
                while True:
                    info = self.get_heartbeat_info()
                    await beats.put(info)
                    await asyncio.sleep(3)

            # Lock to ensure that only one executor can grab a
            # request at a time.
            requests_lock = asyncio.Lock()

            # Lock to ensure that only one executor can put a
            # result in the results queue at a time.
            results_lock = asyncio.Lock()

            async def executor() -> None:
                # We use locks here to protect the request/result
                # queues from being accessed by multiple executors.
                while True:
                    async with requests_lock:
                        request = await requests.get()

                    try:
                        if isinstance(request, StreamingCodeExecutionRequest):
                            async for (
                                streaming_response
                            ) in self.handle_streaming_request(request):
                                async with results_lock:
                                    await results.put(streaming_response)
                        else:
                            # Note that we don't want to hold the lock here
                            # because we want other executors to be able to
                            # grab requests while we're handling a request.
                            response = await self.handle_request(request)
                            async with results_lock:
                                await results.put(response)
                    except Exception as e:
                        logger.error(
                            f"Error handling request {request.namespace}:\n\n{e}"
                        )
                        async with results_lock:
                            await results.put(
                                ErrorResponse(
                                    error_type="request_error",
                                    correlation_id=request.correlation_id,
                                    request_namespace=request.namespace,
                                    error_info=serialize_error_info(e),
                                )
                            )

            beat_task = asyncio.create_task(beat())

            # Three parallel executors to handle requests
            executor_tasks = [
                asyncio.create_task(executor()),
                asyncio.create_task(executor()),
                asyncio.create_task(executor()),
            ]

            try:
                while True:
                    recv = asyncio.create_task(websocket.recv())
                    get_beat = asyncio.create_task(beats.get())
                    get_result = asyncio.create_task(results.get())

                    done, pending = await asyncio.wait(
                        [recv, get_beat, get_result],
                        return_when=asyncio.FIRST_COMPLETED,
                    )

                    for task in pending:
                        task.cancel()

                        try:
                            await task
                        except asyncio.CancelledError:
                            pass

                    if recv in done:
                        msg = json.loads(str(recv.result()))

                        if msg["type"] == "request":
                            data = json.dumps(msg["data"])
                            request = deserialize_request_data(data)

                            if isinstance(request, HaltRequest):
                                logger.debug(
                                    f"Received HaltRequest for correlation_id {request.correlation_id}"
                                )
                                await self.halt_all_code_executions()
                                data = json.loads(
                                    serialize_message(
                                        HaltResponse(
                                            correlation_id=request.correlation_id,
                                        )
                                    )
                                )
                                msg = json.dumps({"type": "result", "data": data})
                                logger.debug(
                                    f"Sending HaltResponse for correlation_id {request.correlation_id}"
                                )
                                await websocket.send(msg)
                            elif isinstance(request, SwitchCLIChatRequest):
                                data = json.loads(
                                    serialize_message(
                                        SwitchCLIChatResponse(
                                            correlation_id=request.correlation_id,
                                        )
                                    )
                                )
                                msg = json.dumps({"type": "result", "data": data})
                                await websocket.send(msg)
                                return SwitchCLIChat(
                                    new_chat_uuid=request.new_chat_uuid
                                )
                            elif isinstance(
                                request, CodeExecutionRequest
                            ) or isinstance(request, StreamingCodeExecutionRequest):
                                await self.add_code_execution_to_halt_states(
                                    request.correlation_id
                                )
                                await requests.put(request)
                            else:
                                await requests.put(request)

                    elif get_beat in done:
                        info = get_beat.result()
                        data = json.loads(info.model_dump_json())
                        msg = json.dumps({"type": "heartbeat", "data": data})
                        await websocket.send(msg)

                    elif get_result in done:
                        response = get_result.result()
                        data = json.loads(serialize_message(response))
                        msg = json.dumps({"type": "result", "data": data})
                        await websocket.send(msg)

            except websockets.exceptions.ConnectionClosed as e:
                if e.rcvd is not None and e.rcvd.code == 1000:  # noqa: PLR2004
                    break
            except TimeoutError:
                pass
            finally:
                beat_task.cancel()

                for executor_task in executor_tasks:
                    executor_task.cancel()

                await asyncio.gather(beat_task, *executor_tasks, return_exceptions=True)

            if connection_tracker is not None:
                await connection_tracker.set_connected(False)

        return WSDisconnected()

    async def check_remote_end_event(self, chat_uuid: str) -> bool:
        response = await self.api_client.get(
            f"/api/remote_execution/{chat_uuid}/execution_end",
        )
        execution_end_response = await deserialize_api_response(
            response, ExecutionEndResponse
        )
        return execution_end_response.execution_ended

    async def create_chat(self) -> CreateChatResponse:
        response = await self.api_client.post(
            "/api/remote_execution/create_chat",
        )
        return await deserialize_api_response(response, CreateChatResponse)

    async def start_chat(
        self, chat_uuid: str, prompt: str, use_tools_config: UseToolsConfig
    ) -> StartChatResponse:
        response = await self.api_client.post(
            "/api/remote_execution/start_chat",
            json=StartChatRequest(
                chat_uuid=chat_uuid,
                prompt=prompt,
                use_tools_config=use_tools_config,
            ).model_dump(),
            timeout=60,
        )
        return await deserialize_api_response(response, StartChatResponse)

    async def run_workflow(self, chat_uuid: str, workflow_id: str) -> None:
        response = await self.api_client.post(
            "/api/remote_execution/run_workflow",
            json=RunWorkflowRequest(
                chat_uuid=chat_uuid,
                workflow_id=workflow_id,
            ).model_dump(),
            timeout=60,
        )
        if response.status_code != http_status.OK:
            raise Exception(
                f"Failed to run workflow with status code {response.status_code} and response {response.text}"
            )

    def get_heartbeat_info(self) -> HeartbeatInfo:
        return HeartbeatInfo(
            system_info=system_context.get_system_info(self.working_directory),
        )

    async def send_heartbeat(self, chat_uuid: str) -> CLIConnectedState:
        logger.info(f"Sending heartbeat for chat_uuid {chat_uuid}")
        heartbeat_info = self.get_heartbeat_info()
        response = await self.api_client.post(
            f"/api/remote_execution/{chat_uuid}/heartbeat",
            content=heartbeat_info.model_dump_json(),
            timeout=60,
        )
        if response.status_code != http_status.OK:
            raise Exception(
                f"Heartbeat failed with status code {response.status_code} and response {response.text}"
            )
        connected_state = await deserialize_api_response(response, CLIConnectedState)
        logger.info(f"Heartbeat response: {connected_state}")
        return connected_state

    async def handle_request(
        self, request: Union[RemoteExecutionRequestType, LocalEventType]
    ) -> RemoteExecutionResponseType:
        if isinstance(request, (CodeBlockEvent, FileWriteEvent, CommandEvent)):
            request = convert_event_to_execution_request(request)

        try:
            response: RemoteExecutionResponseType
            if isinstance(request, CodeExecutionRequest):
                response = await execute_code(
                    request,
                    self.current_session,
                    working_directory=self.working_directory,
                    should_halt=self.get_halt_check(request.correlation_id),
                )
            elif isinstance(request, FileWriteRequest):
                response = execute_file_write(
                    request,
                    working_directory=self.working_directory,
                )
            elif isinstance(request, ListFilesRequest):
                response = await files.list_files(request)
            elif isinstance(request, GetFileAttachmentRequest):
                response = await files.get_file_attachment(
                    request, self.working_directory
                )
            elif isinstance(request, GetFileAttachmentsRequest):
                response = await files.get_file_attachments(
                    request, self.working_directory
                )
            elif isinstance(request, GetMatchingFilesRequest):
                response = await files.get_matching_files(request, self.file_cache)
            elif isinstance(request, SystemContextRequest):
                response = system_context.get_system_context(
                    request, self.working_directory
                )
            elif isinstance(request, GetAllTrackedFilesRequest):
                response = await files.get_all_tracked_files(
                    request, self.working_directory
                )
            elif isinstance(request, CommandRequest):
                response = await execute_command(
                    request,
                    self.working_directory,
                )
            elif isinstance(request, StreamingCodeExecutionRequest):
                assert False, "CodeExecutionStreamingRequest should be sent to handle_streaming_request"
            elif isinstance(request, HaltRequest):
                assert False, "HaltRequest should be handled in the main loop"
            elif isinstance(request, SwitchCLIChatRequest):
                assert False, "SwitchCLIChatRequest should be handled in the main loop"
            else:
                logger.error(f"Unhandled request type: {type(request)}")
                response = ErrorResponse(
                    error_type="unknown_request_type",
                    correlation_id=request.correlation_id,
                    request_namespace=request.namespace,
                )
            return response
        finally:
            # Clean up halt state after request is complete
            if isinstance(request, CodeExecutionRequest) or isinstance(
                request, StreamingCodeExecutionRequest
            ):
                await self.clear_halt_state(request.correlation_id)

    async def handle_streaming_request(
        self, request: StreamingCodeExecutionRequest
    ) -> AsyncGenerator[RemoteExecutionResponseType, None]:
        if not isinstance(request, StreamingCodeExecutionRequest):
            assert False, f"{type(request)} should be sent to handle_streaming_request"

        async for output in execute_code_streaming(
            request,
            self.current_session,
            working_directory=self.working_directory,
            should_halt=self.get_halt_check(request.correlation_id),
        ):
            yield output

    def ws_connect(self, path: str) -> websockets.client.connect:
        base_url = (
            str(self.ws_client.base_url)
            .replace("http://", "ws://")
            .replace("https://", "wss://")
        )

        url = f"{base_url}{path}"
        headers = {"api-key": self.api_client.headers["api-key"]}

        return websockets.client.connect(
            url, extra_headers=headers, timeout=10, ping_timeout=10
        )

    @staticmethod
    @asynccontextmanager
    async def session(
        api_key: str, base_url: str, base_ws_url: str, working_directory: str
    ) -> AsyncGenerator[RemoteExecutionClient, None]:
        async with get_session(
            working_directory, base_url, base_ws_url, api_key
        ) as session:
            yield RemoteExecutionClient(session)
