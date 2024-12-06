import typer

from cli import settings
from cli.cloud.auth.login import login as do_login
from cli.cloud.rest_helper import RestHelper as Rest

from .. import auth_tokens

HELP = """
Manage how you authenticate with our cloud platform
"""
app = typer.Typer(help=HELP)
app.add_typer(auth_tokens.app, name="tokens", help="Manage users personal access tokens")


@app.command(name="login")
def login() -> None:
    """
    Login to the cli using browser

    This will be used as the current access token in all subsequent requests. This would
    be the same as activating a personal access key or service-account access key.
    """
    do_login()


@app.command()
def whoami() -> None:
    """
    Validates authentication and fetches your user information
    """
    Rest.handle_get("/api/whoami")


@app.command()
def print_access_token() -> None:
    """
    Print current active access token
    """
    print(settings.read_secret_token())


@app.command(help="Clear access token")
def logout() -> None:
    settings.clear_secret_token()
    print("Access token removed")
