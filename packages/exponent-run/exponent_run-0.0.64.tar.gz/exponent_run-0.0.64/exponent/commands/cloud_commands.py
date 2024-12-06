import time
from typing import Any, cast

import click

from exponent.commands.common import create_chat, redirect_to_login, run_until_complete
from exponent.commands.settings import use_settings
from exponent.commands.types import exponent_cli_group
from exponent.commands.utils import (
    launch_exponent_browser,
    print_exponent_message,
)
from exponent.core.config import Environment, Settings
from exponent.core.graphql.client import GraphQLClient
from exponent.core.graphql.get_cloud_chat_state_query import GET_CLOUD_CHAT_STATE_QUERY
from exponent.core.graphql.mutations import MOVE_CHAT_TO_CLOUD_MUTATION
from exponent.core.remote_execution.types import DevboxConnectedState


@exponent_cli_group()
def cloud_cli() -> None:
    pass


@cloud_cli.command()
@use_settings
def cloud(
    settings: Settings,
) -> None:
    """Start an Exponent session in the cloud."""
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        start_cloud(
            settings.environment,
            settings.api_key,
            settings.base_url,
            settings.base_api_url,
            settings.base_ws_url,
        )
    )


async def start_cloud(
    environment: Environment,
    api_key: str,
    base_url: str,
    base_api_url: str,
    base_ws_url: str,
) -> None:
    chat_uuid = await create_chat(api_key, base_api_url, base_ws_url)

    if chat_uuid is None:
        return

    graphql_client = GraphQLClient(
        api_key=api_key, base_api_url=base_api_url, base_ws_url=base_ws_url
    )
    response = await graphql_client.execute(
        MOVE_CHAT_TO_CLOUD_MUTATION, {"chatUuid": chat_uuid}, "MoveChatToCloud"
    )

    if response["moveChatToCloud"]["chatUuid"] != chat_uuid:
        click.secho(
            f"Failed to initalize cloud chat: {response['moveChatToCloud']}",
            fg="red",
            bold=True,
        )
        return

    click.secho(
        "Chat created. Waiting for cloud container to spin up...", fg="green", bold=True
    )

    while True:
        chatState = await fetch_cloud_chat_state(
            api_key,
            base_api_url,
            base_ws_url,
            chat_uuid,
        )
        connectedState = chatState["cloudChatState"]["connectedState"]
        if connectedState == DevboxConnectedState.CONNECTED.value:
            break

        time.sleep(1)

    print_exponent_message(base_url, chat_uuid)
    launch_exponent_browser(environment, base_url, chat_uuid)


async def fetch_cloud_chat_state(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
    chat_uuid: str,
) -> dict[str, Any]:
    graphql_client = GraphQLClient(
        api_key=api_key, base_api_url=base_api_url, base_ws_url=base_ws_url
    )
    return cast(
        dict[str, Any],
        await graphql_client.execute(
            GET_CLOUD_CHAT_STATE_QUERY, {"chatUuid": chat_uuid}, "GetCloudChatState"
        ),
    )
