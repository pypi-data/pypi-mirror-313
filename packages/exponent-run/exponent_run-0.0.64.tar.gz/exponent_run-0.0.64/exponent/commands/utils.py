import asyncio
import os
import sys
import threading
import time
from typing import Optional

import click

from exponent.core.config import Environment, Settings
from exponent.utils.version import get_installed_version


def print_editable_install_forced_prod_warning(settings: Settings) -> None:
    click.secho(
        "Detected local editable install, but this command only works against prod.",
        fg="red",
        bold=True,
    )
    click.secho("Using prod settings:", fg="red", bold=True)
    click.secho("- base_url=", fg="yellow", bold=True, nl=False)
    click.secho(f"{settings.base_url}", fg=(100, 200, 255), bold=False)
    click.secho("- base_api_url=", fg="yellow", bold=True, nl=False)
    click.secho(f"{settings.base_api_url}", fg=(100, 200, 255), bold=False)
    click.secho()


def print_editable_install_warning(settings: Settings) -> None:
    click.secho(
        "Detected local editable install, using local URLs", fg="yellow", bold=True
    )
    click.secho("- base_url=", fg="yellow", bold=True, nl=False)
    click.secho(f"{settings.base_url}", fg=(100, 200, 255), bold=False)
    click.secho("- base_api_url=", fg="yellow", bold=True, nl=False)
    click.secho(f"{settings.base_api_url}", fg=(100, 200, 255), bold=False)
    click.secho()


def print_exponent_message(base_url: str, chat_uuid: str) -> None:
    version = get_installed_version()
    shell = os.environ.get("SHELL")

    click.echo()
    click.secho(f"△ Exponent v{version}", fg=(180, 150, 255), bold=True)
    click.echo()
    click.echo(
        " - Link: " + click.style(f"{base_url}/chats/{chat_uuid}", fg=(100, 200, 255))
    )

    if shell is not None:
        click.echo(f" - Shell: {shell}")


def is_exponent_app_installed() -> bool:
    if sys.platform == "darwin":  # macOS
        return os.path.exists("/Applications/Exponent.app")

    # TODO: Add support for Windows and Linux
    return False


def launch_exponent_browser(
    environment: Environment, base_url: str, chat_uuid: str
) -> None:
    if is_exponent_app_installed() and environment == Environment.production:
        url = f"exponent://chats/{chat_uuid}"
    else:
        url = f"{base_url}/chats/{chat_uuid}"
    click.launch(url)


def start_background_event_loop() -> asyncio.AbstractEventLoop:
    def run_event_loop(loop: asyncio.AbstractEventLoop) -> None:
        asyncio.set_event_loop(loop)
        loop.run_forever()

    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=run_event_loop, args=(loop,), daemon=True)
    thread.start()
    return loop


def read_input(prompt: str) -> str:
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return sys.stdin.readline()


def ask_for_quit_confirmation(program_name: str = "Exponent") -> bool:
    while True:
        try:
            answer = (
                input(f"Do you want to quit {program_name}? [y/N] ").strip().lower()
            )
            if answer in {"y", "yes"}:
                return True
            elif answer in {"n", "no", ""}:
                return False
        except KeyboardInterrupt:
            print()
            return True


class Spinner:
    def __init__(self, text: str) -> None:
        self.text = text
        self.task: Optional[asyncio.Task[None]] = None
        self.base_time = time.time()

    def show(self) -> None:
        if self.task is not None:
            return

        async def spinner(base_time: float) -> None:
            chars = "⣷⣯⣟⡿⢿⣻⣽⣾"

            while True:
                t = time.time() - base_time
                i = round(t * 10) % len(chars)
                print(f"\r{chars[i]} {self.text}", end="")
                await asyncio.sleep(0.1)

        self.task = asyncio.get_event_loop().create_task(spinner(self.base_time))

    def hide(self) -> None:
        if self.task is None:
            return

        self.task.cancel()
        self.task = None
        print("\r\x1b[0m\x1b[2K", end="")
        sys.stdout.flush()


class ConnectionTracker:
    def __init__(self) -> None:
        self.connected = True
        self.queue: asyncio.Queue[bool] = asyncio.Queue()

    def is_connected(self) -> bool:
        while True:
            try:
                self.connected = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                break

        return self.connected

    async def wait_for_reconnection(self) -> None:
        if not self.is_connected():
            assert await self.queue.get()
            self.connected = True

    async def set_connected(self, connected: bool) -> None:
        await self.queue.put(connected)

    async def next_change(self) -> bool:
        return await self.queue.get()
