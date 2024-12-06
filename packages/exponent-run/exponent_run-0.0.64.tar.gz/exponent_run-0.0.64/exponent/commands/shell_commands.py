import asyncio
import difflib
import sys
from collections.abc import Callable, Coroutine, Iterable
from concurrent.futures import Future
from typing import Any, Optional, Union
from .utils import ask_for_quit_confirmation
import click
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.syntax import Syntax

from exponent.commands.common import (
    check_inside_git_repo,
    check_running_from_home_directory,
    check_ssl,
    create_chat,
    inside_ssh_session,
    redirect_to_login,
    start_client,
)
from exponent.commands.settings import use_settings
from exponent.commands.types import (
    StrategyChoice,
    StrategyOption,
    exponent_cli_group,
)
from exponent.commands.utils import (
    ConnectionTracker,
    Spinner,
    start_background_event_loop,
)
from exponent.core.config import Settings
from exponent.core.graphql.client import GraphQLClient
from exponent.core.graphql.mutations import HALT_CHAT_STREAM_MUTATION
from exponent.core.graphql.queries import EVENTS_FOR_CHAT_QUERY
from exponent.core.graphql.subscriptions import CHAT_EVENTS_SUBSCRIPTION
from exponent.core.remote_execution.exceptions import ExponentError
from exponent.core.types.generated.strategy_info import (
    ENABLED_STRATEGY_INFO_LIST,
)

SLASH_COMMANDS = {
    "/help": "Show available commands",
    "/autorun": "Toggle autorun mode",
    "/web": "Move chat to a web browser",
    "/cmd": "Execute a terminal command directly and give the result as context",
}


@exponent_cli_group()
def shell_cli() -> None:
    pass


@shell_cli.command()
@click.option(
    "--model",
    help="LLM model",
    required=True,
    default="CLAUDE_3_POINT_5_SONNET",
)
@click.option(
    "--strategy",
    prompt=True,
    prompt_required=False,
    type=StrategyChoice(ENABLED_STRATEGY_INFO_LIST),
    cls=StrategyOption,
)
@click.option(
    "--autorun",
    is_flag=True,
    help="Enable autorun mode",
)
@click.option(
    "--depth",
    type=click.IntRange(1, 30, clamp=True),
    help="Depth limit of the chat if autorun mode is enabled",
    default=5,
)
@click.option(
    "--chat-id",
    help="ID of an existing chat session to reconnect",
    required=False,
)
@click.option(
    "--prompt",
    help="Initial prompt",
)
@click.option(
    "--headless",
    is_flag=True,
    help="Run single prompt in headless mode",
)
@use_settings
def shell(
    settings: Settings,
    model: str,
    strategy: str,
    chat_id: Optional[str] = None,
    autorun: bool = False,
    depth: int = 0,
    prompt: Optional[str] = None,
    headless: bool = False,
) -> None:
    """Start an Exponent session in your current shell."""

    if not headless and not sys.stdin.isatty():
        print("Terminal not available, running in headless mode")
        headless = True

    if headless and not prompt:
        print("Error: --prompt option is required with headless mode")
        sys.exit(1)

    if not settings.api_key:
        redirect_to_login(settings)
        return

    is_running_from_home_directory = check_running_from_home_directory(
        # We don't require a confirmation for exponent shell because it's more likely
        # there's a legitimate reason for running Exponent from home directory when using shell
        require_confirmation=False
    )

    if not is_running_from_home_directory:  # Prevent double warnings from being shown
        check_inside_git_repo(settings)

    check_ssl()

    api_key = settings.api_key
    base_api_url = settings.base_api_url
    base_ws_url = settings.base_ws_url
    gql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    loop = start_background_event_loop()
    parent_event_uuid: Optional[str] = None

    if chat_id is None:
        chat_uuid = asyncio.run_coroutine_threadsafe(
            create_chat(api_key, base_api_url, base_ws_url), loop
        ).result()
    else:
        chat_uuid = chat_id

        parent_event_uuid = asyncio.run_coroutine_threadsafe(
            get_parent_event_uuid(gql_client, chat_uuid), loop
        ).result()

    if chat_uuid is None:
        sys.exit(1)

    connection_tracker = ConnectionTracker()

    client_coro = start_client(
        api_key,
        base_api_url,
        base_ws_url,
        chat_uuid,
        connection_tracker=connection_tracker,
    )

    if headless:
        assert prompt is not None

        chat = Chat(
            chat_uuid,
            parent_event_uuid,
            settings.base_url,
            gql_client,
            model,
            strategy,
            autorun,
            depth,
            StaticView(),
        )

        client_task = loop.create_task(client_coro)
        turn_task = loop.create_task(chat.send_prompt(prompt))

        asyncio.run_coroutine_threadsafe(
            asyncio.wait({client_task, turn_task}, return_when=asyncio.FIRST_COMPLETED),
            loop,
        ).result()
    else:
        chat = Chat(
            chat_uuid,
            parent_event_uuid,
            settings.base_url,
            gql_client,
            model,
            strategy,
            autorun,
            depth,
            LiveView(),
        )

        client_fut = asyncio.run_coroutine_threadsafe(client_coro, loop)
        input_handler = InputHandler()
        shell = Shell(prompt, loop, input_handler, chat, connection_tracker)
        shell.run()
        client_fut.cancel()

    print("Jump back into this chat by running:")
    print(f"  exponent shell --chat-id {chat_uuid}")
    print()
    print("Or continue in a web browser at:")
    print(f"  {chat.url()}")
    print()
    print("Bye!")


async def get_parent_event_uuid(
    gql_client: GraphQLClient, chat_uuid: str
) -> Optional[str]:
    result = await gql_client.execute(EVENTS_FOR_CHAT_QUERY, {"chatUuid": chat_uuid})
    events = result.get("eventsForChat", {}).get("events", [])

    if len(events) > 0:
        uuid = events[-1]["eventUuid"]
        assert isinstance(uuid, str)

        return uuid

    return None


def pause_spinner(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(self: "LiveView", *args: Any, **kwargs: Any) -> Any:
        self.spinner.hide()
        self.spinner = self.default_spinner
        result = func(self, *args, **kwargs)
        self.spinner.show()
        return result

    return wrapper


def stop_spinner(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(self: "LiveView", *args: Any, **kwargs: Any) -> Any:
        self.spinner.hide()
        self.spinner = self.default_spinner
        result = func(self, *args, **kwargs)
        return result

    return wrapper


class BaseView:
    def _render_block_header(self, text: str) -> list[str]:
        return [
            block_header_bg_seq(),
            block_header_fg_seq(),
            erase_line_seq(),
            " " + text,
            reset_attrs_seq(),
            "\n",
        ]

    def _render_block_padding(self) -> list[str]:
        return [
            block_body_bg_seq(),
            erase_line_seq(),
            reset_attrs_seq(),
            "\n",
        ]

    def _render_block_footer(
        self, text: str, status: Optional[str] = None
    ) -> list[str]:
        seqs: list[Any] = [
            block_header_bg_seq(),
            block_header_fg_seq(),
            erase_line_seq(),
            " ",
        ]

        if status == "completed":
            seqs.append(
                [
                    fg_color_seq(2),
                    bold_seq(),
                    "✓ ",
                    not_bold_seq(),
                    block_header_fg_seq(),
                ]
            )
        elif status == "rejected":
            seqs.append(
                [
                    fg_color_seq(1),
                    bold_seq(),
                    "𐄂 ",
                    not_bold_seq(),
                    block_header_fg_seq(),
                ]
            )
        elif status == "running":
            seqs.append(["⚙️ "])

        seqs.append([text, reset_attrs_seq(), "\n"])

        return seqs

    def _render_natural_edit_diff(self, write: dict[str, Any]) -> list[Any]:
        diff = generate_diff(write.get("originalFile") or "", write["newFile"]).strip()

        highlighted_diff = highlight_code(
            diff, "udiff", line_numbers=False, padding=(0, 2)
        )

        return [
            self._render_block_header("diff"),
            self._render_block_padding(),
            highlighted_diff,
            self._render_block_padding(),
        ]

    def _render_natural_edit_error(self, error: str) -> list[str]:
        return [
            fg_color_seq(1),
            f"\nError: {error.strip()}\n\n",
            reset_attrs_seq(),
        ]

    def _render_code_block_start(self, lang: str) -> list[Any]:
        return [
            self._render_block_header(lang),
            self._render_block_padding(),
        ]

    def _render_code_block_content(self, content: str, lang: str) -> str:
        return highlight_code(content.strip(), lang, line_numbers=False, padding=(0, 2))

    def _render_code_block_output(self, content: str) -> list[Any]:
        lines = pad_left(content, "  ").split("\n")
        output = [[block_body_bg_seq(), erase_line_seq(), line, "\n"] for line in lines]

        return [
            self._render_block_header("output"),
            self._render_block_padding(),
            output,
            self._render_block_padding(),
        ]

    def _render_file_write_block_start(self, path: str) -> list[Any]:
        return [
            self._render_block_header(f"Editing file {path}"),
            self._render_block_padding(),
        ]

    def _render_file_write_block_content(self, content: str, lang: str) -> str:
        return highlight_code(content.strip(), lang, line_numbers=False, padding=(0, 2))

    def _render_file_write_block_result(self, result: Optional[str]) -> list[Any]:
        result = result or "Edit applied"
        return [self._render_block_footer(f"{result}", status="completed")]

    def _render_command_block_start(self, type_: str) -> list[Any]:
        return [
            self._render_block_header(type_.lower()),
            self._render_block_padding(),
        ]

    def _render_command_block_content(self, data: dict[str, Any]) -> list[Any]:
        if data["type"] == "PROTOTYPE":
            content = data["contentRendered"]
        else:
            content = data["filePath"].strip()

        lines = pad_left(content, "  ").split("\n")
        return [[block_body_bg_seq(), erase_line_seq(), line, "\n"] for line in lines]

    def _render_command_block_output(
        self, content: str, type_: str, lang: str
    ) -> list[Any]:
        highlighted_result = highlight_code(
            content.strip(),
            lang,
            line_numbers=False,
            padding=(0, 2),
        )

        return [
            self._render_block_header("output"),
            self._render_block_padding(),
            highlighted_result,
            self._render_block_padding(),
            self._render_block_footer(
                f"{type_.lower()} command executed", status="completed"
            ),
        ]


class LiveView(BaseView):
    def __init__(self) -> None:
        self.buffer: Buffer = NullBuffer()
        self.command_data: Optional[dict[str, Any]] = None
        self.confirmation_required: bool = True
        self.default_spinner = Spinner("Exponent is working...")
        self.msg_gen_spinner = Spinner("Exponent is thinking real hard...")
        self.exec_spinner = Spinner(
            "Exponent is waiting for the code to finish running..."
        )
        self.diff_spinner = Spinner("Exponent is generating file diff...")
        self.spinner = self.default_spinner

    def render_event(self, kind: str, event: dict[str, Any]) -> None:  # noqa: PLR0912
        if kind == "MessageStart":
            self._handle_message_start_event(event)
        elif kind == "MessageChunkEvent":
            if event["role"] == "assistant":
                self._handle_message_chunk_event(event)
        elif kind == "MessageEvent":
            if event["role"] == "assistant":
                self._handle_message_event(event)
        elif kind == "FileWriteChunkEvent":
            self._handle_file_write_chunk_event(event)
        elif kind == "FileWriteEvent":
            self._handle_file_write_event(event)
        elif kind == "FileWriteConfirmationEvent":
            self._handle_file_write_confirmation_event(event)
        elif kind == "FileWriteStartEvent":
            self._handle_file_write_start_event(event)
        elif kind == "FileWriteResultEvent":
            self._handle_file_write_result_event(event)
        elif kind == "CodeBlockChunkEvent":
            self._handle_code_block_chunk_event(event)
        elif kind == "CodeBlockEvent":
            self._handle_code_block_event(event)
        elif kind == "CodeBlockConfirmationEvent":
            self._handle_code_block_confirmation_event(event)
        elif kind == "CodeExecutionStartEvent":
            self._handle_code_execution_start_event(event)
        elif kind == "CodeExecutionEvent":
            self._handle_code_execution_event(event)
        elif kind == "CommandChunkEvent":
            if event["data"]["type"] in ["FILE_READ", "FILE_OPEN", "PROTOTYPE"]:
                self._handle_command_chunk_event(event)
        elif kind == "CommandEvent":
            if event["data"]["type"] in ["FILE_READ", "FILE_OPEN", "PROTOTYPE"]:
                self._handle_command_event(event)
        elif kind == "CommandConfirmationEvent":
            self._handle_command_confirmation_event(event)
        elif kind == "CommandStartEvent":
            self._handle_command_start_event(event)
        elif kind == "CommandResultEvent":
            self._handle_command_result_event(event)
        elif kind == "Error":
            raise ExponentError(event["message"])

    def start_turn(self) -> None:
        self.spinner.show()

    def end_turn(self) -> None:
        self.spinner.hide()

    @pause_spinner
    def _handle_message_start_event(self, event: dict[str, Any]) -> None:
        self.spinner = self.msg_gen_spinner

    @stop_spinner
    def _handle_message_chunk_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]
        seqs = []

        if self.buffer.event_uuid != event_uuid:
            self.buffer = CharBuffer(event_uuid)

        assert isinstance(self.buffer, CharBuffer)

        seqs.append(self.buffer.render_new_chars(event["content"]))
        render(seqs)

    @pause_spinner
    def _handle_message_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]
        seqs = []

        if self.buffer.event_uuid != event_uuid:
            self.buffer = CharBuffer(event_uuid)

        assert isinstance(self.buffer, CharBuffer)

        seqs.append(self.buffer.render_new_chars(event["content"]))
        seqs.append(["\n\n"])
        render(seqs)

    @stop_spinner
    def _handle_file_write_chunk_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]
        seqs: list[Any] = []

        if self.buffer.event_uuid != event_uuid:
            self.buffer = LineBuffer(event_uuid)

            seqs.append(
                [
                    self._render_block_header(f"Editing file {event['filePath']}"),
                    self._render_block_padding(),
                ]
            )

        assert isinstance(self.buffer, LineBuffer)

        write = event["writeContent"]
        content = write.get("naturalEdit") or write.get("content") or event["content"]

        formatted_content = self._render_file_write_block_content(
            content, event["language"]
        )

        seqs.append(self.buffer.render_new_lines(formatted_content))

        if "newFile" in write and write["newFile"] is None:  # natural edit
            # when newFile is present in writeContent dict but is None
            # it indicates the server is generating original/new file pair

            seqs.append([self._render_block_padding(), "\n"])
            render(seqs)
            self.spinner = self.diff_spinner
            self.spinner.show()
        else:
            render(seqs)

    @pause_spinner
    def _handle_file_write_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]
        seqs: list[Any] = []

        if self.buffer.event_uuid != event_uuid:
            self.buffer = LineBuffer(event_uuid)
            seqs.append(self._render_file_write_block_start(event["filePath"]))

        assert isinstance(self.buffer, LineBuffer)

        write = event["writeContent"]

        if "newFile" in write:  # natural edit
            seqs.append(
                [
                    "\r",
                    move_cursor_up_seq(2),
                    erase_display_seq(),
                ]
            )

        content = write.get("naturalEdit") or write.get("content") or event["content"]

        formatted_content = self._render_file_write_block_content(
            content, event["language"]
        )

        seqs.append(
            [
                self.buffer.render_new_lines(formatted_content),
                self._render_block_padding(),
            ]
        )

        error = write.get("errorContent")

        if error is None:
            if write.get("newFile") is not None:
                seqs.append(self._render_natural_edit_diff(write))

            if event["requireConfirmation"]:
                seqs.append(
                    [
                        self._render_block_footer(
                            "Confirm edit with <C+y>. Sending a new message will dismiss code changes."
                        ),
                        "\n",
                    ]
                )
        else:
            seqs.append(self._render_natural_edit_error(error))

        render(seqs)
        self.confirmation_required = event["requireConfirmation"]

    @pause_spinner
    def _handle_file_write_confirmation_event(self, event: dict[str, Any]) -> None:
        if self.buffer.event_uuid != event["fileWriteUuid"]:
            return

        seqs = []

        if event["accepted"]:
            seqs.append(
                [
                    move_cursor_up_seq(2),
                    self._render_block_footer("Applying edit...", status="running"),
                    "\n",
                ]
            )
        elif self.confirmation_required:
            # user entered new prompt, cursor moved down
            # therefore we need to move it up, redraw status, and move it
            # back where it was

            seqs.append(
                [
                    move_cursor_up_seq(4),
                    self._render_block_footer("Edit dismissed", status="rejected"),
                    "\n\n\n",
                ]
            )

        render(seqs)

    @pause_spinner
    def _handle_file_write_start_event(self, event: dict[str, Any]) -> None:
        return

    @pause_spinner
    def _handle_file_write_result_event(self, event: dict[str, Any]) -> None:
        if self.buffer.event_uuid != event["fileWriteUuid"]:
            return

        seqs: list[Any] = []

        if self.confirmation_required:
            seqs.append([move_cursor_up_seq(2)])

        seqs.append([self._render_file_write_block_result(event["content"]), "\n"])

        render(seqs)

    @stop_spinner
    def _handle_command_chunk_event(self, event: dict[str, Any]) -> None:
        type_ = self._get_command_type(event["data"])

        event_uuid = event["eventUuid"]
        seqs = []

        if self.buffer.event_uuid != event_uuid:
            self.buffer = CommandBuffer(event_uuid)

            seqs.append(
                [
                    self._render_block_header(type_),
                    self._render_block_padding(),
                ]
            )

        assert isinstance(self.buffer, CommandBuffer)

        formatted_content = self._render_command_block_content(event["data"])
        seqs.append(self.buffer.render_new_lines(formatted_content))
        render(seqs)

    @pause_spinner
    def _handle_command_event(self, event: dict[str, Any]) -> None:
        type_ = self._get_command_type(event["data"])
        event_uuid = event["eventUuid"]
        seqs: list[Any] = []

        if self.buffer.event_uuid != event_uuid:
            self.buffer = CommandBuffer(event_uuid)
            seqs.append(self._render_command_block_start(type_))

        assert isinstance(self.buffer, CommandBuffer)

        formatted_content = self._render_command_block_content(event["data"])
        seqs.append(self.buffer.render_new_lines(formatted_content))
        seqs.append(self._render_block_padding())

        if event["requireConfirmation"]:
            seqs.append(
                [
                    self._render_block_footer(
                        f"Confirm {type_} command with <C+y>. "
                        "Sending a new message will cancel this command."
                    ),
                    "\n",
                ]
            )

        render(seqs)
        self.command_data = event["data"]
        self.confirmation_required = event["requireConfirmation"]

    @pause_spinner
    def _handle_command_confirmation_event(self, event: dict[str, Any]) -> None:
        if self.buffer.event_uuid != event["commandUuid"]:
            return

        seqs = []

        if event["accepted"]:
            seqs.append(
                [
                    move_cursor_up_seq(2),
                    self._render_block_footer("Executing command...", status="running"),
                    "\n",
                ]
            )
        else:
            # user entered new prompt, cursor moved down
            # therefore we need to move it up, redraw status, and move it
            # back where it was

            seqs.append(
                [
                    move_cursor_up_seq(4),
                    self._render_block_footer(
                        "Command did not execute", status="rejected"
                    ),
                    "\n\n\n",
                ]
            )

        render(seqs)

    def _handle_command_start_event(self, event: dict[str, Any]) -> None:
        return

    @pause_spinner
    def _handle_command_result_event(self, event: dict[str, Any]) -> None:
        if self.buffer.event_uuid != event["commandUuid"] or self.command_data is None:
            return

        seqs: list[Any] = []

        if self.confirmation_required:
            seqs.append([move_cursor_up_seq(2)])

        seqs.append(
            [
                self._render_command_block_output(
                    event["content"],
                    self._get_command_type(self.command_data),
                    self.command_data.get("language", "txt"),
                ),
                "\n",
            ]
        )

        render(seqs)
        self.command_data = None

    @stop_spinner
    def _handle_code_block_chunk_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]
        seqs = []

        if self.buffer.event_uuid != event_uuid:
            self.buffer = LineBuffer(event_uuid)

            seqs.append(
                [
                    self._render_block_header(event["language"]),
                    self._render_block_padding(),
                ]
            )

        assert isinstance(self.buffer, LineBuffer)

        formatted_content = self._render_code_block_content(
            event["content"], event["language"]
        )

        seqs.append(self.buffer.render_new_lines(formatted_content))
        render(seqs)

    @pause_spinner
    def _handle_code_block_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]
        seqs: list[Any] = []

        if self.buffer.event_uuid != event_uuid:
            self.buffer = LineBuffer(event_uuid)
            seqs.append(self._render_code_block_start(event["language"]))

        assert isinstance(self.buffer, LineBuffer)

        formatted_content = self._render_code_block_content(
            event["content"], event["language"]
        )

        seqs.append(self.buffer.render_new_lines(formatted_content))
        seqs.append(self._render_block_padding())

        if event["requireConfirmation"]:
            seqs.append(
                [
                    self._render_block_footer(
                        "Run this code now with <C+y>. Sending a new message will cancel this request."
                    ),
                    "\n",
                ]
            )

        render(seqs)
        self.confirmation_required = event["requireConfirmation"]

    @pause_spinner
    def _handle_code_block_confirmation_event(self, event: dict[str, Any]) -> None:
        if self.buffer.event_uuid != event["codeBlockUuid"]:
            return

        seqs = []

        if event["accepted"]:
            seqs.append(
                [
                    move_cursor_up_seq(2),
                    self._render_block_footer("Running code...", status="running"),
                    "\n",
                ]
            )
        else:
            # user entered new prompt, cursor moved down
            # therefore we need to move it up, redraw status, and move it
            # back where it was

            seqs.append(
                [
                    move_cursor_up_seq(4),
                    self._render_block_footer(
                        "Code did not execute", status="rejected"
                    ),
                    "\n\n\n",
                ]
            )

        render(seqs)

    @pause_spinner
    def _handle_code_execution_start_event(self, event: dict[str, Any]) -> None:
        self.spinner = self.exec_spinner

    @pause_spinner
    def _handle_code_execution_event(self, event: dict[str, Any]) -> None:
        if self.buffer.event_uuid != event["codeBlockUuid"]:
            return

        seqs: list[Any] = []

        if self.confirmation_required:
            seqs.append([move_cursor_up_seq(2)])

        seqs.append([self._render_code_block_output(event["content"]), "\n"])

        render(seqs)

    def _get_command_type(self, data: dict[str, Any]) -> str:
        if data["type"] == "PROTOTYPE":
            return str(data["commandName"])
        else:
            return str(data["type"]).lower()


class StaticView(BaseView):
    def __init__(self) -> None:
        self.command_data: Optional[dict[str, Any]] = None

    def render_event(self, kind: str, event: dict[str, Any]) -> None:  # noqa: PLR0912
        if kind == "MessageEvent":
            if event["role"] == "assistant":
                print(event["content"].strip())
                print()

        elif kind == "FileWriteEvent":
            write = event["writeContent"]

            content = (
                write.get("naturalEdit") or write.get("content") or event["content"]
            )

            seqs = [
                self._render_file_write_block_start(event["filePath"]),
                self._render_file_write_block_content(content, event["language"]),
                self._render_block_padding(),
            ]

            error = write.get("errorContent")

            if error is None:
                if write.get("newFile") is not None:
                    seqs.append(self._render_natural_edit_diff(write))
            else:
                seqs.append(self._render_natural_edit_error(error))

            render(seqs)

        elif kind == "FileWriteResultEvent":
            seqs = [self._render_file_write_block_result(event["content"]), "\n"]
            render(seqs)

        elif kind == "CodeBlockEvent":
            seqs = [
                self._render_code_block_start(event["language"]),
                self._render_code_block_content(event["content"], event["language"]),
                self._render_block_padding(),
            ]

            render(seqs)

        elif kind == "CodeExecutionEvent":
            render([self._render_code_block_output(event["content"]), "\n"])

        elif kind == "CommandEvent":
            if event["data"]["type"] not in ["FILE_READ", "FILE_OPEN"]:
                return

            seqs = [
                self._render_command_block_start(event["data"]["type"]),
                self._render_command_block_content(event["data"]),
                self._render_block_padding(),
            ]

            render(seqs)
            self.command_data = event["data"]

        elif kind == "CommandResultEvent":
            if self.command_data is not None:
                seqs = [
                    self._render_command_block_output(
                        event["content"],
                        self.command_data["type"],
                        self.command_data["language"],
                    ),
                    "\n",
                ]

                render(seqs)
                self.command_data = None

        elif kind == "Error":
            print(f"Error: {event['message']}")
            print()

    def start_turn(self) -> None:
        pass

    def end_turn(self) -> None:
        pass


class Chat:
    def __init__(
        self,
        chat_uuid: str,
        parent_event_uuid: Optional[str],
        base_url: str,
        gql_client: GraphQLClient,
        model: str,
        strategy: str,
        autorun: bool,
        depth: int,
        view: Union[StaticView, LiveView],
    ) -> None:
        self.chat_uuid = chat_uuid
        self.base_url = base_url
        self.gql_client = gql_client
        self.model = model
        self.strategy = strategy
        self.autorun = autorun
        self.depth = depth
        self.view = view
        self.parent_uuid: Optional[str] = parent_event_uuid
        self.block_row_offset = 0
        self.console = Console()
        self.code_block_uuid = None
        self.file_write_uuid = None
        self.command_uuid = None

    async def send_prompt(self, prompt: str) -> None:
        self.view.start_turn()

        await self.process_chat_subscription(
            {"prompt": {"message": prompt, "attachments": []}}
        )

    async def send_confirmation(self) -> None:
        if self.code_block_uuid is not None:
            await self.process_chat_subscription(
                {
                    "codeBlockConfirmation": {
                        "accepted": True,
                        "codeBlockUuid": self.code_block_uuid,
                    }
                }
            )
        elif self.file_write_uuid is not None:
            await self.process_chat_subscription(
                {
                    "fileWriteConfirmation": {
                        "accepted": True,
                        "fileWriteUuid": self.file_write_uuid,
                    }
                }
            )
        elif self.command_uuid is not None:
            await self.process_chat_subscription(
                {
                    "commandConfirmation": {
                        "accepted": True,
                        "commandUuid": self.command_uuid,
                    }
                }
            )

    async def send_direct_action(self, action_type: str, command: str) -> None:
        self.view.start_turn()

        if action_type == "shell":
            await self.process_chat_subscription(
                {"directAction": {"shellDirectAction": {"command": command}}}
            )
        else:
            raise ValueError(f"Unsupported direct action type: {action_type}")

    def toggle_autorun(self) -> bool:
        self.autorun = not self.autorun
        return self.autorun

    async def halt_stream(self) -> None:
        await self.gql_client.execute(
            HALT_CHAT_STREAM_MUTATION, {"chatUuid": self.chat_uuid}, "HaltChatStream"
        )

    def url(self) -> str:
        return f"{self.base_url}/chats/{self.chat_uuid}"

    async def process_chat_subscription(self, extra_vars: dict[str, Any]) -> None:
        vars = {
            "chatUuid": self.chat_uuid,
            "parentUuid": self.parent_uuid,
            "model": self.model,
            "strategyNameOverride": self.strategy,
            "useToolsConfig": "read_write",
            "requireConfirmation": not self.autorun,
            "depthLimit": self.depth,
        }

        vars.update(extra_vars)
        self.code_block_uuid = None
        self.file_write_uuid = None
        self.command_uuid = None

        try:
            async for response in self.gql_client.subscribe(
                CHAT_EVENTS_SUBSCRIPTION, vars
            ):
                event = response["authenticatedChat"]
                kind = event["__typename"]
                self.view.render_event(kind, event)
                self.parent_uuid = event.get("eventUuid") or self.parent_uuid

                if kind == "CodeBlockEvent" and event["requireConfirmation"]:
                    self.code_block_uuid = event["eventUuid"]
                elif kind == "FileWriteEvent" and event["requireConfirmation"]:
                    self.file_write_uuid = event["eventUuid"]
                elif kind == "CommandEvent" and event.get("requireConfirmation"):
                    self.command_uuid = event["eventUuid"]
        finally:
            self.view.end_turn()


class InputHandler:
    def __init__(self) -> None:
        self.kb = KeyBindings()
        self.shortcut_pressed = None
        self.session: PromptSession[Any] = PromptSession(
            completer=SlashCommandCompleter(),
            complete_while_typing=False,
            key_bindings=self.kb,
        )

        @self.kb.add("c-y")
        def _(event: Any) -> None:
            self.shortcut_pressed = "<c-y>"
            event.app.exit()

        @self.kb.add("c-d")
        def _(event: Any) -> None:
            self.shortcut_pressed = "<c-d>"
            event.app.exit()

    def prompt(self) -> str:
        self.shortcut_pressed = None
        user_input = self.session.prompt(HTML("<b><ansigreen>></ansigreen></b> "))

        if self.shortcut_pressed:
            return self.shortcut_pressed
        else:
            assert isinstance(user_input, str)
            return user_input


class Shell:
    def __init__(
        self,
        prompt: Optional[str],
        loop: asyncio.AbstractEventLoop,
        input_handler: InputHandler,
        chat: Chat,
        connection_tracker: ConnectionTracker,
    ) -> None:
        self.prompt = prompt
        self.loop = loop
        self.input_handler = input_handler
        self.chat = chat
        self.stream_fut: Optional[Future[Any]] = None
        self.connection_tracker = connection_tracker

    def run(self) -> None:
        self._print_welcome_message()
        self._send_initial_prompt()

        while True:
            try:
                self._wait_for_stream_completion()
                text = self.input_handler.prompt()

                if text.startswith("/"):
                    self._run_command(text[1:].strip())
                elif text == "<c-y>":
                    self._confirm_execution()
                elif text in {"q", "exit"}:
                    print()
                    break
                elif text == "<c-d>":
                    print()
                    do_quit = ask_for_quit_confirmation()
                    print()

                    if do_quit:
                        break
                elif text:
                    print()
                    self._send_prompt(text)

            except KeyboardInterrupt:
                if self._handle_keyboard_interrupt():
                    break

            except ExponentError as e:
                self._print_error_message(e)
                break

    def _handle_keyboard_interrupt(self) -> bool:
        try:
            if self.stream_fut is not None:
                self._run_coroutine(self.chat.halt_stream()).result()
                return True
            return ask_for_quit_confirmation()
        except KeyboardInterrupt:
            return True

    def _ensure_connected(self) -> None:
        if not self.connection_tracker.is_connected():
            self._run_coroutine(self._wait_for_reconnection()).result()

    async def _wait_for_reconnection(self) -> None:
        render([clear_line_seq(), "Disconnected..."])
        await asyncio.sleep(1)
        spinner = Spinner("Reconnecting...")
        spinner.show()
        await self.connection_tracker.wait_for_reconnection()
        spinner.hide()
        render([fg_color_seq(2), bold_seq(), "✓ Reconnected"])
        await asyncio.sleep(1)
        render([clear_line_seq()])

    def _print_welcome_message(self) -> None:
        print("Welcome to ✨ \x1b[1;32mExponent \x1b[4:3mSHELL\x1b[0m ✨")
        print()
        print("Type 'q', 'exit' or press <C-c> to exit")
        print("Enter '/help' to see a list of available commands")
        print()

    def _print_error_message(self, e: ExponentError) -> None:
        print(f"\n\n\x1b[1;31m{e}\x1b[0m")
        print("\x1b[3;33m")
        print("Please try again and reach out if the problem persists.")
        print("\x1b[0m")

    def _show_help(self) -> None:
        print()

        for command, description in SLASH_COMMANDS.items():
            print(f"{command} - {description}")

        print()

    def _run_command(self, command: str) -> None:
        parts = command.split(maxsplit=1)
        cmd = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        if cmd == "cmd":
            self._execute_shell_command(args)
        elif cmd == "help":
            self._show_help()
        elif cmd == "autorun":
            self._toggle_autorun()
        elif cmd == "web":
            self._switch_cli_chat_to_web()
        else:
            print(f"\nUnknown command: /{command}\n")

    def _execute_shell_command(self, shell_command: str) -> None:
        if not shell_command:
            click.echo("\nError: Command command is empty. Usage: /cmd <command>\n")
            return

        self._ensure_connected()
        self.stream_fut = self._run_coroutine(
            self.chat.send_direct_action("shell", shell_command)
        )

    def _toggle_autorun(self) -> None:
        if self.chat.toggle_autorun():
            print("\nAutorun mode enabled\n")
        else:
            print("\nAutorun mode disabled\n")

    def _switch_cli_chat_to_web(self) -> None:
        url = self.chat.url()
        print(f"\nThis chat has been moved to {url}\n")

        if not inside_ssh_session():
            click.launch(url)

        while True:
            input()

    def _confirm_execution(self) -> None:
        render(
            [
                "\r",
                move_cursor_up_seq(1),
                clear_line_seq(),
            ]
        )

        self._ensure_connected()
        self.stream_fut = self._run_coroutine(self.chat.send_confirmation())

    def _send_initial_prompt(self) -> None:
        if self.prompt is not None:
            self._send_prompt(self.prompt)

    def _send_prompt(self, text: str) -> None:
        self._ensure_connected()
        self.stream_fut = self._run_coroutine(self.chat.send_prompt(text))

    def _wait_for_stream_completion(self) -> None:
        if self.stream_fut is not None:
            self.stream_fut.result()
            self.stream_fut = None

    def _run_coroutine(self, coro: Coroutine[Any, Any, Any]) -> Future[Any]:
        return asyncio.run_coroutine_threadsafe(coro, self.loop)


class SlashCommandCompleter(Completer):
    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        text = document.text
        if text.startswith("/"):
            for command in SLASH_COMMANDS:
                if command.startswith(text):
                    yield Completion(command, start_position=-len(text))


class Buffer:
    def __init__(self, event_uuid: str) -> None:
        self.event_uuid = event_uuid


class NullBuffer(Buffer):
    def __init__(self) -> None:
        super().__init__("")


class CharBuffer(Buffer):
    def __init__(self, event_uuid: str) -> None:
        super().__init__(event_uuid)
        self.content_len = 0

    def render_new_chars(self, message: str) -> list[Any]:
        message = message.strip()
        chunk = message[self.content_len :]
        self.content_len = len(message)

        return [chunk]


class LineBuffer(Buffer):
    def __init__(self, event_uuid: str) -> None:
        super().__init__(event_uuid)
        self.line_count = 0

    def render_new_lines(
        self,
        code: str,
    ) -> list[Any]:
        seqs: list[Any] = []
        lines = code.split("\n")
        lines = lines[0 : len(lines) - 1]
        new_line_count = len(lines)

        if self.line_count > 0:
            seqs.append([move_cursor_up_seq(1), "\r"])
            lines = lines[self.line_count - 1 :]

        lines = [line + "\n" for line in lines]
        seqs.append(lines)
        self.line_count = new_line_count

        return seqs


# TODO maybe unify with LineBuffer?
class CommandBuffer(Buffer):
    def __init__(self, event_uuid: str) -> None:
        super().__init__(event_uuid)
        self.line_count = 0

    def render_new_lines(self, paths: list[Any]) -> list[Any]:
        seqs: list[Any] = []
        new_line_count = len(paths)

        if self.line_count > 0:
            seqs.append([move_cursor_up_seq(1), "\r"])
            paths = paths[self.line_count - 1 :]

        seqs.append(paths)
        self.line_count = new_line_count

        return seqs


def highlight_code(
    code: str, lang: str, line_numbers: bool = True, padding: tuple[int, int] = (0, 0)
) -> str:
    syntax = Syntax(
        code,
        lang,
        theme="monokai",
        line_numbers=line_numbers,
        word_wrap=True,
        padding=padding,
    )

    console = Console()

    with console.capture() as capture:
        console.print(syntax)

    return capture.get()


def generate_diff(before_lines: str, after_lines: str) -> str:
    diff = difflib.unified_diff(
        before_lines.split("\n"),
        after_lines.split("\n"),
        fromfile="before",
        tofile="after",
        lineterm="",
    )

    return "\n".join(list(diff)[2:])


def pad_left(text: str, padding: str) -> str:
    return "\n".join([padding + line for line in text.strip().split("\n")])


def fg_color_seq(c: int) -> str:
    return f"\x1b[{30 + c}m"


def bold_seq() -> str:
    return "\x1b[1m"


def not_bold_seq() -> str:
    return "\x1b[22m"


def block_header_bg_seq() -> str:
    return "\x1b[48;2;29;30;24m"


def block_header_fg_seq() -> str:
    return "\x1b[38;5;246m"


def block_body_bg_seq() -> str:
    return "\x1b[48;5;235m"


def erase_line_seq() -> str:
    return "\x1b[2K"


def erase_display_seq() -> str:
    return "\x1b[0J"


def reset_attrs_seq() -> str:
    return "\x1b[0m"


def clear_line_seq() -> str:
    return f"\r{reset_attrs_seq()}{erase_line_seq()}"


def move_cursor_up_seq(n: int) -> str:
    if n > 0:
        return f"\x1b[{n}A"
    else:
        return ""


def move_cursor_down_seq(n: int) -> str:
    if n > 0:
        return f"\x1b[{n}B"
    else:
        return ""


def render(seqs: Union[str, list[Any], None]) -> None:
    print(collect(seqs), end="")
    sys.stdout.flush()


def collect(seqs: Union[str, list[Any], None]) -> str:
    if seqs is None:
        return ""

    if isinstance(seqs, str):
        return seqs

    assert isinstance(seqs, list)

    text = ""

    for seq in seqs:
        text += collect(seq)

    return text
