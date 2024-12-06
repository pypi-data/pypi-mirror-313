import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Optional

import httpx
from httpx import AsyncClient, Request, Response

from exponent.core.remote_execution.exceptions import ExponentError
from exponent.core.remote_execution.languages.python_execution import Kernel
from exponent.core.remote_execution.utils import format_error_log

logger = logging.getLogger(__name__)


class SessionLog:
    def __init__(self) -> None:
        self.log_buffer: list[str] = []
        self.max_size = 5

    def append_log(self, log: str) -> None:
        self.log_buffer.append(log)
        self.log_buffer = self.log_buffer[-self.max_size :]

    def get_logs(self) -> list[str]:
        return self.log_buffer

    async def log_request(self, request: Request) -> None:
        self.append_log(f"Request: {request.method} {request.url}")

    async def log_response(self, response: Response) -> None:
        request = response.request
        await response.aread()
        self.append_log(
            f"Response for request: {request.method} {request.url}\n"
            f"Response: {response.status_code}, {response.text}"
        )


class RemoteExecutionClientSession:
    def __init__(
        self, working_directory: str, base_url: str, base_ws_url: str, api_key: str
    ):
        self.chat_uuid: Optional[str] = None

        self.working_directory = working_directory
        self.kernel = Kernel(working_directory=working_directory)
        self.api_log = SessionLog()

        self.api_client = AsyncClient(
            base_url=base_url,
            headers={"API-KEY": api_key},
            event_hooks={
                "request": [self.api_log.log_request],
                "response": [self.api_log.log_response],
            },
        )

        self.ws_client = AsyncClient(
            base_url=base_ws_url,
            headers={"API-KEY": api_key},
            event_hooks={
                "request": [self.api_log.log_request],
                "response": [self.api_log.log_response],
            },
        )

    def set_chat_uuid(self, chat_uuid: str) -> None:
        self.chat_uuid = chat_uuid

    async def send_exception_log(self, exc: Exception) -> None:
        error_log = format_error_log(
            exc=exc,
            chat_uuid=self.chat_uuid,
            attachment_lines=self.api_log.get_logs(),
        )

        if not error_log:
            return
        try:
            await self.api_client.post(
                "/api/remote_execution/log_error",
                content=error_log.model_dump_json(),
                timeout=60,
            )
        except httpx.ConnectError:
            logger.error("Failed to send error log")


@asynccontextmanager
async def get_session(
    working_directory: str,
    base_url: str,
    base_ws_url: str,
    api_key: str,
) -> AsyncGenerator[RemoteExecutionClientSession, None]:
    session = RemoteExecutionClientSession(
        working_directory, base_url, base_ws_url, api_key
    )
    try:
        yield session
    except Exception as exc:  # noqa: BLE001
        await session.send_exception_log(exc)
        raise ExponentError(str(exc))
    finally:
        session.kernel.close()
        await session.api_client.aclose()
