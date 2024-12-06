import json
import sys
from typing import Optional

import click

from exponent.commands.common import (
    redirect_to_login,
    run_until_complete,
    set_login_complete,
)
from exponent.commands.settings import use_settings
from exponent.commands.types import exponent_cli_group
from exponent.core.config import Settings, get_settings
from exponent.core.graphql.client import GraphQLClient
from exponent.core.graphql.cloud_config_queries import (
    CREATE_CLOUD_CONFIG_MUTATION,
    GET_CLOUD_CONFIGS_QUERY,
    UPDATE_CLOUD_CONFIG_MUTATION,
)
from exponent.core.graphql.get_chats_query import GET_CHATS_QUERY
from exponent.core.graphql.github_config_queries import (
    CREATE_GITHUB_CONFIG_MUTATION,
    CHECK_GITHUB_CONFIG_VALIDITY_QUERY,
    REPOS_FOR_GITHUB_CONFIG_QUERY,
)
from exponent.core.graphql.mutations import (
    UPGRADE_USER_TO_TRUSTED_MUTATION,
)
from exponent.core.graphql.subscriptions import AUTHENTICATED_USER_SUBSCRIPTION
from exponent.utils.version import (
    get_installed_metadata,
    get_installed_version,
    get_installer,
    get_python_path,
    get_sys_executable,
)


@exponent_cli_group()
def config_cli() -> None:
    """Manage Exponent configuration settings."""
    pass


@config_cli.command()
@use_settings
def debug(
    settings: Settings,
) -> None:
    click.echo("Settings:")
    click.echo(settings)
    click.echo("\nInstalled Version:")
    click.echo(get_installed_version())
    click.echo("\nPython Version:")
    click.echo(sys.version)
    click.echo("\nPython Path:")
    click.echo(get_python_path())
    click.echo("\nSys Executable Path:")
    click.echo(get_sys_executable())
    click.echo("\nInstaller:")
    click.echo(get_installer())
    click.echo("\nInstalled Metadata:")
    click.echo(get_installed_metadata())


@config_cli.command()
@use_settings
def check_github_config_validity(
    settings: Settings,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        check_github_config_validity_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
            base_ws_url=settings.base_ws_url,
        )
    )


async def check_github_config_validity_task(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    result = await graphql_client.execute(CHECK_GITHUB_CONFIG_VALIDITY_QUERY)
    click.echo(result)


@config_cli.command()
@use_settings
def repos_for_github_config(
    settings: Settings,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        repos_for_github_config_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
            base_ws_url=settings.base_ws_url,
        )
    )


async def repos_for_github_config_task(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    try:
        click.echo("Sending request to fetch repos...")
        result = await graphql_client.execute(
            REPOS_FOR_GITHUB_CONFIG_QUERY, timeout=120
        )  # 120 seconds timeout
        click.echo("Request completed. Result:")
        click.echo(result)
    except Exception as e:
        click.echo(f"An error occurred while fetching repos: {str(e)}")
        click.echo(f"Error type: {type(e).__name__}")
        # Add more detailed error information if available
        if hasattr(e, "response"):
            click.echo(f"Response status: {e.response.status_code}")
            click.echo(f"Response content: {e.response.text}")


@config_cli.command()
@click.option(
    "--set-git-warning-disabled",
    is_flag=True,
    help="Disable the git warning for running Exponent from a non-git repository",
)
@click.option(
    "--set-git-warning-enabled",
    is_flag=True,
    help="Enable the git warning for running Exponent from a non-git repository",
)
def config(set_git_warning_disabled: bool, set_git_warning_enabled: bool) -> None:
    """Display current Exponent configuration."""
    config_file_settings = get_settings().get_config_file_settings()

    if set_git_warning_enabled and set_git_warning_disabled:
        click.secho(
            "Cannot enable and disable git warning at the same time.",
            fg="red",
        )
        return

    elif set_git_warning_enabled:
        if (
            "options" in config_file_settings
            and "git_warning_disabled" in config_file_settings["options"]
        ):
            del config_file_settings["options"]["git_warning_disabled"]

        click.secho(
            "Git warning enabled. Exponent will now check for a git repository.\n",
            fg="yellow",
        )

    elif set_git_warning_disabled:
        if "options" not in config_file_settings:
            config_file_settings["options"] = {}

        config_file_settings["options"]["git_warning_disabled"] = True

        click.secho(
            "Git warning disabled. Exponent will no longer check for a git repository.\n",
            fg="yellow",
        )
    else:
        click.secho(
            json.dumps(config_file_settings, indent=2),
            fg="green",
        )


@config_cli.command()
@click.option("--key", help="Your Exponent API Key")
@use_settings
def login(settings: Settings, key: str) -> None:
    """Log in to Exponent."""

    if not key:
        redirect_to_login(settings, "provided")
        return

    click.echo("Verifying API key...")
    run_until_complete(
        set_login_complete(key, settings.base_api_url, settings.base_ws_url)
    )
    click.secho("Success!", fg="green")

    click.echo(f"Saving API Key to {settings.config_file_path}")

    if settings.api_key and settings.api_key != key:
        click.confirm("Detected existing API Key, continue? ", default=True, abort=True)

    settings.update_api_key(key)
    settings.write_settings_to_config_file()

    click.echo("API Key saved.")


@config_cli.command(hidden=True)
@use_settings
def get_chats(
    settings: Settings,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        get_chats_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
            base_ws_url=settings.base_ws_url,
        )
    )


@config_cli.command(hidden=True)
@use_settings
def get_authenticated_user(
    settings: Settings,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        get_authenticated_user_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
            base_ws_url=settings.base_ws_url,
        )
    )


async def get_chats_task(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    result = await graphql_client.execute(GET_CHATS_QUERY)
    click.echo(result)


async def get_authenticated_user_task(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    async for it in graphql_client.subscribe(AUTHENTICATED_USER_SUBSCRIPTION):
        click.echo(it)


@config_cli.command(hidden=True)
@use_settings
def get_cloud_configs(
    settings: Settings,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        get_cloud_configs_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
            base_ws_url=settings.base_ws_url,
        )
    )


async def get_cloud_configs_task(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    result = await graphql_client.execute(GET_CLOUD_CONFIGS_QUERY)
    click.echo(result)


async def create_github_config_task(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
    github_pat: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    variables = {
        "githubPat": github_pat,
    }
    result = await graphql_client.execute(CREATE_GITHUB_CONFIG_MUTATION, variables)
    click.echo(result)


@config_cli.command(hidden=True)
@click.option("--github-pat", required=True, help="Github personal access token")
@use_settings
def create_github_config(
    settings: Settings,
    github_pat: str,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        create_github_config_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
            base_ws_url=settings.base_ws_url,
            github_pat=github_pat,
        )
    )


@config_cli.command(hidden=True)
@click.option("--github-org-name", required=True, help="GitHub organization name")
@click.option("--github-repo-name", required=True, help="GitHub repository name")
@click.option(
    "--setup_commands",
    required=False,
    help="List of commands to set up and build your repo",
    multiple=True,
)
@use_settings
def create_cloud_config(
    settings: Settings,
    github_org_name: str,
    github_repo_name: str,
    setup_commands: Optional[list[str]] = None,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        create_cloud_config_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
            base_ws_url=settings.base_ws_url,
            github_org_name=github_org_name,
            github_repo_name=github_repo_name,
            setup_commands=setup_commands,
        )
    )


async def create_cloud_config_task(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
    github_org_name: str,
    github_repo_name: str,
    setup_commands: Optional[list[str]],
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    variables = {
        "githubOrgName": github_org_name,
        "githubRepoName": github_repo_name,
        "setupCommands": setup_commands,
    }
    result = await graphql_client.execute(CREATE_CLOUD_CONFIG_MUTATION, variables)
    click.echo(result)


@config_cli.command(hidden=True)
@click.option("--cloud-config-uuid", required=True, help="Cloud config UUID")
@click.option("--github-org-name", required=True, help="GitHub organization name")
@click.option("--github-repo-name", required=True, help="GitHub repository name")
@click.option(
    "--setup_commands",
    required=False,
    help="List of commands to set up and build your repo",
    multiple=True,
)
@use_settings
def update_cloud_config(
    settings: Settings,
    cloud_config_uuid: str,
    github_org_name: str,
    github_repo_name: str,
    setup_commands: Optional[list[str]] = None,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        update_cloud_config_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
            base_ws_url=settings.base_ws_url,
            cloud_config_uuid=cloud_config_uuid,
            github_org_name=github_org_name,
            github_repo_name=github_repo_name,
            setup_commands=setup_commands,
        )
    )


async def update_cloud_config_task(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
    cloud_config_uuid: str,
    github_org_name: str,
    github_repo_name: str,
    setup_commands: Optional[list[str]],
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    variables = {
        "cloudConfigUuid": cloud_config_uuid,
        "githubOrgName": github_org_name,
        "githubRepoName": github_repo_name,
        "setupCommands": setup_commands,
    }

    result = await graphql_client.execute(UPDATE_CLOUD_CONFIG_MUTATION, variables)
    click.echo(result)


@config_cli.command(hidden=True)
@click.option(
    "--email", required=True, help="Email of the user to upgrade to paid plan"
)
@use_settings
def upgrade_user_to_paid(
    settings: Settings,
    email: str,
) -> None:
    """Upgrade a user to trusted plan. Only available to @exponent.run admins."""
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        upgrade_user_to_trusted_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
            base_ws_url=settings.base_ws_url,
            email=email,
        )
    )


async def upgrade_user_to_trusted_task(
    api_key: str,
    base_api_url: str,
    email: str,
    base_ws_url: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    variables = {
        "email": email,
    }
    result = await graphql_client.execute(UPGRADE_USER_TO_TRUSTED_MUTATION, variables)
    if "__typename" in result["upgradeUserToTrusted"]:
        if result["upgradeUserToTrusted"]["__typename"] == "Error":
            click.secho(f"Error: {result['upgradeUserToTrusted']['message']}", fg="red")
        else:
            click.secho(
                f"Successfully upgraded user {result['upgradeUserToTrusted']['email']} to {result['upgradeUserToTrusted']['plan']} plan",
                fg="green",
            )
    else:
        click.echo(result)
