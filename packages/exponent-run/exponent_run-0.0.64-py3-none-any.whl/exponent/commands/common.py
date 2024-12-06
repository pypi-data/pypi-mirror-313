import asyncio
import logging
import os
import platform
import ssl

import os.path
import stat
import sys
import certifi
from collections.abc import Coroutine
from typing import Any, Optional, cast

import click
from exponent.core.graphql.client import GraphQLClient
from exponent.core.graphql.mutations import SET_LOGIN_COMPLETE_MUTATION
from exponent.core.remote_execution.git import get_git_info
import httpx
from dotenv import load_dotenv

from exponent.commands.utils import ConnectionTracker
from exponent.core.config import (
    Settings,
    get_settings,
)
from exponent.core.remote_execution.client import (
    REMOTE_EXECUTION_CLIENT_EXIT_INFO,
    RemoteExecutionClient,
)
from exponent.core.remote_execution.exceptions import (
    ExponentError,
    HandledExponentError,
)
from exponent.core.remote_execution.types import UseToolsConfig

load_dotenv()


def set_log_level() -> None:
    settings = get_settings()
    logging.basicConfig(level=getattr(logging, settings.log_level), stream=sys.stdout)


def redirect_to_login(settings: Settings, cause: str = "detected") -> None:
    if inside_ssh_session():
        click.echo(f"No API Key {cause}, run 'exponent login --key <API-KEY>'")
    else:
        click.echo("No API Key detected, redirecting to login...")
        click.launch(f"{settings.base_url}/cli")


def inside_ssh_session() -> bool:
    return (os.environ.get("SSH_TTY") or os.environ.get("SSH_TTY")) is not None


def inside_git_repo() -> bool:
    git_info = get_git_info(os.getcwd())

    return git_info is not None


def missing_ssl_certs() -> bool:
    if platform.system().lower() != "darwin":
        return False

    openssl_dir, openssl_cafile = os.path.split(
        ssl.get_default_verify_paths().openssl_cafile
    )

    return not os.path.exists(os.path.join(openssl_dir, openssl_cafile))


def install_ssl_certs() -> None:
    STAT_0o775 = (
        stat.S_IRUSR
        | stat.S_IWUSR
        | stat.S_IXUSR
        | stat.S_IRGRP
        | stat.S_IWGRP
        | stat.S_IXGRP
        | stat.S_IROTH
        | stat.S_IXOTH
    )

    openssl_dir, openssl_cafile = os.path.split(
        ssl.get_default_verify_paths().openssl_cafile
    )

    cwd = os.getcwd()
    # change working directory to the default SSL directory
    os.chdir(openssl_dir)
    relpath_to_certifi_cafile = os.path.relpath(certifi.where())

    try:
        os.remove(openssl_cafile)
    except FileNotFoundError:
        pass

    click.echo(" -- creating symlink to certifi certificate bundle")
    os.symlink(relpath_to_certifi_cafile, openssl_cafile)
    click.echo(" -- setting permissions")
    os.chmod(openssl_cafile, STAT_0o775)
    click.echo(" -- update complete")
    os.chdir(cwd)


def check_ssl() -> None:
    if missing_ssl_certs():
        click.confirm(
            "Missing root SSL certs required for python to make HTTP requests, "
            "install certifi certificates now?",
            abort=True,
            default=True,
        )

        install_ssl_certs()


def check_inside_git_repo(settings: Settings) -> None:
    if not inside_git_repo() and not settings.options.git_warning_disabled:
        click.echo(
            click.style(
                "\nWarning: Running from a folder that is not a git repository",
                fg="yellow",
                bold=True,
            )
        )
        click.echo(
            "This is a check to make sure you are running Exponent from the root of your project."
        )

        click.echo(f"\nCurrent directory: {click.style(os.getcwd(), fg='cyan')}")

        click.echo("\nRecommendation:")
        click.echo("  Run Exponent from the root directory of your codebase.")
        click.echo("\nExample:")
        click.echo(
            f"  If your project is in {click.style('~/my-project', fg='cyan')}, run:"
        )
        click.echo(f"  {click.style('cd ~/my-project && exponent run', fg='green')}")

        # Tell the user they can run exponent config --no-git-warning to disable this check
        click.echo(
            f"\nYou can run {click.style('exponent config --set-git-warning-disabled', fg='green')} to disable this check."
        )

        if not click.confirm(
            click.style(
                f"\nDo you want to continue running Exponent from {os.getcwd()}?",
                fg="yellow",
            ),
            default=True,
        ):
            click.echo(click.style("\nOperation aborted.", fg="red"))
            raise click.Abort()


def check_running_from_home_directory(require_confirmation: bool = True) -> bool:
    if os.path.expanduser("~") == os.getcwd():
        click.echo(
            click.style(
                "\nWarning: Running Exponent from Home Directory",
                fg="yellow",
                bold=True,
            )
        )
        click.echo(
            "Running Exponent from your home directory can cause unexpected issues."
        )
        click.echo("\nRecommendation:")
        click.echo("  Run Exponent from the root directory of your codebase.")
        click.echo("\nExample:")
        click.echo(
            f"  If your project is in {click.style('~/my-project', fg='cyan')}, run:"
        )
        click.echo(f"  {click.style('cd ~/my-project && exponent run', fg='green')}")

        if require_confirmation:
            if not click.confirm(
                click.style(
                    f"\nDo you want to continue running Exponent from {os.getcwd()}?",
                    fg="yellow",
                ),
                default=True,
            ):
                click.echo(click.style("\nOperation aborted.", fg="red"))
                raise click.Abort()
        else:
            click.echo("\n")  # Newline to separate from next command

        return True

    return False


def run_until_complete(coro: Coroutine[Any, Any, Any]) -> Any:
    loop = asyncio.get_event_loop()
    task = loop.create_task(coro)

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        task.cancel()
        try:
            loop.run_until_complete(task)
        except asyncio.CancelledError:
            pass
    except ExponentError as e:
        click.secho(f"Encountered error: {e}", fg="red")
        click.secho(
            "The Exponent team has been notified, "
            "please try again and reach out if the problem persists.",
            fg="yellow",
        )
        sys.exit(1)
    except HandledExponentError as e:
        click.secho(str(e), fg="red")
        sys.exit(1)


async def benchmark_mode_exit(client: RemoteExecutionClient, chat_uuid: str) -> None:
    while True:
        await asyncio.sleep(5)
        if await client.check_remote_end_event(chat_uuid):
            sys.exit(0)


async def run_client_connection(
    client: RemoteExecutionClient,
    chat_uuid: str,
    connection_tracker: Optional[ConnectionTracker] = None,
) -> REMOTE_EXECUTION_CLIENT_EXIT_INFO:
    return await client.run_connection(chat_uuid, connection_tracker)


async def start_chat(
    client: RemoteExecutionClient,
    chat_uuid: str,
    prompt: str,
) -> None:
    click.secho("Starting chat...")
    await client.start_chat(chat_uuid, prompt, use_tools_config=UseToolsConfig())
    click.secho("Chat started. Open the link to join the chat.")


async def run_workflow(
    client: RemoteExecutionClient,
    chat_uuid: str,
    workflow_id: str,
) -> None:
    click.secho("Running workflow...")
    await client.run_workflow(chat_uuid, workflow_id)
    click.secho("Workflow started.")


async def start_client(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
    chat_uuid: str,
    prompt: Optional[str] = None,
    workflow_id: Optional[str] = None,
    connection_tracker: Optional[ConnectionTracker] = None,
) -> REMOTE_EXECUTION_CLIENT_EXIT_INFO:
    async with RemoteExecutionClient.session(
        api_key=api_key,
        base_url=base_api_url,
        base_ws_url=base_ws_url,
        working_directory=os.getcwd(),
    ) as client:
        main_coro = run_client_connection(client, chat_uuid, connection_tracker)
        aux_coros: list[Coroutine[Any, Any, None]] = []

        if prompt:
            # If given a prompt, we also need to send a request
            # to kick off the initial turn loop for the chat
            aux_coros.append(start_chat(client, chat_uuid, prompt))
        elif workflow_id:
            # Similarly, if given a workflow ID, we need to send
            # a request to kick off the workflow
            aux_coros.append(run_workflow(client, chat_uuid, workflow_id))

        client_result, *_ = await asyncio.gather(main_coro, *aux_coros)
        return cast(REMOTE_EXECUTION_CLIENT_EXIT_INFO, client_result)


# Helper functions
async def create_chat(
    api_key: str, base_api_url: str, base_ws_url: str
) -> Optional[str]:
    try:
        async with RemoteExecutionClient.session(
            api_key, base_api_url, base_ws_url, os.getcwd()
        ) as client:
            chat = await client.create_chat()
            return chat.chat_uuid
    except (httpx.ConnectError, ExponentError) as e:
        click.secho(f"Error: {e}", fg="red")
        return None


async def set_login_complete(api_key: str, base_api_url: str, base_ws_url: str) -> None:
    graphql_client = GraphQLClient(
        api_key=api_key, base_api_url=base_api_url, base_ws_url=base_ws_url
    )
    result = await graphql_client.execute(
        SET_LOGIN_COMPLETE_MUTATION, {}, "SetLoginComplete"
    )

    data = result["setLoginComplete"]

    if data["__typename"] == "UnauthenticatedError":
        raise HandledExponentError(f"Verification failed: {data['message']}")

    if data["userApiKey"] != api_key:
        # We got a user object back, but the api_key is different
        # than the one used in the user's request...
        # This should never happen
        raise HandledExponentError(
            "Invalid API key, login to https://exponent.run to find your API key."
        )
