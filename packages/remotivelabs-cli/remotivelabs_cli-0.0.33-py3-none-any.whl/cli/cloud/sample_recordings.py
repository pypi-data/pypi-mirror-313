import json

import typer

from .rest_helper import RestHelper as Rest

app = typer.Typer()


@app.command(name="import", help="Import sample recording into project")
def do_import(
    recording_session: str = typer.Argument(..., help="Recording session id"),
    project: str = typer.Option(..., help="Project to import sample recording into", envvar="REMOTIVE_CLOUD_PROJECT"),
) -> None:
    Rest.handle_post(url=f"/api/samples/files/recording/{recording_session}/copy", body=json.dumps({"projectUid": project}))


@app.command("list")
def list() -> None:  # pylint: disable=W0622
    """
    List available sample recordings
    """

    Rest.handle_get("/api/samples/files/recording")
