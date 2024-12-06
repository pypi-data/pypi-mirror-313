import json
from pathlib import Path

import typer

from cli import settings

from .rest_helper import RestHelper as Rest

app = typer.Typer()


@app.command(name="create", help="Create new access token")
def create(
    expire_in_days: int = typer.Option(default=365, help="Number of this token is valid"),
    service_account: str = typer.Option(..., help="Service account name"),
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
) -> None:
    response = Rest.handle_post(
        url=f"/api/project/{project}/admin/accounts/{service_account}/keys",
        return_response=True,
        body=json.dumps({"daysUntilExpiry": expire_in_days}),
    )

    if response is None:
        return

    if response.status_code == 200:
        name = response.json()["name"]
        write_sa_token(service_account, name, response.text)
    else:
        print(f"Got status code: {response.status_code}")
        print(response.text)


@app.command(name="list", help="List service-account access tokens")
def list_keys(
    service_account: str = typer.Option(..., help="Service account name"),
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
) -> None:
    Rest.handle_get(f"/api/project/{project}/admin/accounts/{service_account}/keys")


@app.command(name="list-files")
def list_files() -> None:
    """
    List personal access token files in remotivelabs config directory
    """
    sa_files = settings.list_service_account_token_files()
    for file in sa_files:
        print(file)


@app.command(name="revoke", help="Revoke service account access token")
def revoke(
    name: str = typer.Argument(..., help="Access token name"),
    service_account: str = typer.Option(..., help="Service account name"),
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
) -> None:
    Rest.handle_delete(f"/api/project/{project}/admin/accounts/{service_account}/keys/{name}")


# TODO: Move to settings # pylint: disable=W0511
def write_sa_token(service_account: str, name: str, token: str) -> Path:
    file = f"service-account-{service_account}-{name}-token.json"
    path = settings.CONFIG_DIR_PATH / file
    return settings._write_settings_file(path, token)  # pylint: disable=W0212
