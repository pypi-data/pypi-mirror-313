import json
import sys

import typer

from cli.cloud.rest_helper import RestHelper

app = typer.Typer()


@app.command(name="list", help="List your available organisations")
def list_orgs() -> None:
    r = RestHelper.handle_get("/api/home", return_response=True)
    if r is None:
        return
    if r.status_code == 200:
        j = list(
            map(
                lambda x: {
                    "uid": x["billableUnitUser"]["billableUnit"]["uid"],
                    "displayName": x["billableUnitUser"]["billableUnit"]["displayName"],
                },
                r.json(),
            )
        )
        print(json.dumps(j))
    else:
        print(f"Got status code: {r.status_code}")
        print(r.text)
        sys.exit(1)
