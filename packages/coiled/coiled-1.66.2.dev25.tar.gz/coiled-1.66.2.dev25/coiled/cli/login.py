import asyncio

import click

from ..utils import login_if_required
from .utils import CONTEXT_SETTINGS


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-s", "--server", help="Coiled server to use", hidden=True)
@click.option("-t", "--token", multiple=True, help="Coiled user token")
@click.option(
    "-a",
    "--account",
    "--workspace",
    help=(
        "Coiled workspace (uses default workspace if not specified). "
        "Note: --account is deprecated, please use --workspace instead."
    ),
)
@click.option(
    "--retry/--no-retry",
    default=True,
    help="Whether or not to automatically ask for a new token if an invalid token is entered",
)
@click.option("--browser/--no-browser", default=True, help="Open browser with page where you grant access")
def login(server, token, account, retry, browser):
    """Configure your Coiled account credentials"""
    # allow token split across multiple --token args, so we can have shorter lines for cloudshell command
    token = "".join(token) if token else None
    asyncio.run(
        login_if_required(
            server=server, token=token, workspace=account, save=True, use_config=False, retry=retry, browser=browser
        )
    )
