from __future__ import annotations

import json
from typing import List

import typer

from . import service_account_tokens
from .rest_helper import RestHelper as Rest

app = typer.Typer()


@app.command(name="list", help="List service-accounts")
def list_service_accounts(project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT")) -> None:
    Rest.handle_get(f"/api/project/{project}/admin/accounts")


@app.command(name="create", help="Create service account")
def create_service_account(
    name: str,
    role: List[str] = typer.Option(..., help="Roles to apply"),
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
) -> None:
    data = {"name": name, "roles": role}
    Rest.handle_post(url=f"/api/project/{project}/admin/accounts", body=json.dumps(data))


@app.command(name="update", help="Update service account")
def update_service_account(
    service_account: str = typer.Option(..., help="Service account name"),
    role: List[str] = typer.Option(..., help="Roles to apply"),
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
) -> None:
    Rest.handle_put(url=f"/api/project/{project}/admin/accounts/{service_account}", body=json.dumps({"roles": role}))


@app.command(name="delete", help="Delete service account")
def delete_service_account(name: str, project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT")) -> None:
    Rest.handle_delete(url=f"/api/project/{project}/admin/accounts/{name}")


app.add_typer(service_account_tokens.app, name="tokens", help="Manage project service account access tokens")
