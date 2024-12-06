import json
import sys
from json.decoder import JSONDecodeError
from pathlib import Path

import typer

from cli import settings

from .rest_helper import RestHelper as Rest

app = typer.Typer()


@app.command(name="create", help="Create and download a new personal access token")
def get_personal_access_token(activate: bool = typer.Option(False, help="Activate the token for use after download")) -> None:  # pylint: disable=W0621
    Rest.ensure_auth_token()
    response = Rest.handle_post(url="/api/me/keys", return_response=True)

    if response is None:
        return

    if response.status_code == 200:
        name = response.json()["name"]
        pat_path = write_personal_token(name, response.text)
        print(f"Personal access token written to {pat_path}")
        if not activate:
            print(f"Use 'remotive cloud auth tokens activate {pat_path.name}' to use this access token from cli")
        else:
            do_activate(str(pat_path))
            print("Token file activated and ready for use")
        print("\033[93m This file contains secrets and must be kept safe")
    else:
        print(f"Got status code: {response.status_code}")
        print(response.text)


@app.command(name="list", help="List personal access tokens")
def list_personal_access_tokens() -> None:
    Rest.ensure_auth_token()
    Rest.handle_get("/api/me/keys")


@app.command(name="revoke")
def revoke(name_or_file: str = typer.Argument(help="Name or file path of the access token to revoke")) -> None:
    """
    Revoke an access token by token name or path to a file containing that token

    Name is found in the json file
    ```
    {
        "expires": "2034-07-31",
        "token": "xxx",
        "created": "2024-07-31T09:18:50.406+02:00",
        "name": "token_name"
    }
    ```
    """
    name = name_or_file
    if "." in name_or_file:
        json_str = read_file(name_or_file)
        try:
            name = json.loads(json_str)["name"]
        except JSONDecodeError:
            sys.stderr.write("Failed to parse json, make sure its a correct access token file\n")
            sys.exit(1)
        except KeyError:
            sys.stderr.write("Json does not contain a name property, make sure its a correct access token file\n")
            sys.exit(1)
    Rest.ensure_auth_token()
    Rest.handle_delete(f"/api/me/keys/{name}")


@app.command()
def describe(file: str = typer.Argument(help="File name")) -> None:
    """
    Show contents of specified access token file
    """
    print(read_file(file))


@app.command()
def activate(file: str = typer.Argument(..., help="File name")) -> None:
    """
    Activate a access token file to be used for authentication.

    --file

    This will be used as the current access token in all subsequent requests. This would
    be the same as login with a browser.
    """
    do_activate(file)


# TODO: Move parts of this to settings # pylint: disable=W0511
def do_activate(file: str) -> None:
    # Best effort to read file
    if Path(file).exists():
        token_file = json.loads(read_file_with_path(Path(file)))
        settings.write_secret_token(token_file["token"])
    elif (settings.CONFIG_DIR_PATH / file).exists():
        token_file = json.loads(read_file(file))
        settings.write_secret_token(token_file["token"])
    else:
        sys.stderr.write("File could not be found \n")


@app.command(name="list-files")
def list_files() -> None:
    """
    List personal access token files in remotivelabs config directory
    """
    personal_files = settings.list_personal_token_files()
    for file in personal_files:
        print(file)


# TODO: Move to settings # pylint: disable=W0511
def read_file(file: str) -> str:
    """
    Reads a file using file path or if that does not exist check in config directory
    """
    path = Path(file)
    if not path.exists():
        path = settings.CONFIG_DIR_PATH / file
        if not path.exists():
            sys.stderr.write(f"Failed to find file using {file} or {path}\n")
            sys.exit(1)

    return read_file_with_path(path)


# TODO: Move to settings # pylint: disable=W0511
def read_file_with_path(path: Path) -> str:
    with open(path, "r", encoding="utf8") as f:
        return f.read()


# TODO: Move to settings # pylint: disable=W0511
def write_personal_token(name: str, token: str) -> Path:
    file = f"personal-token-{name}.json"
    path = settings.CONFIG_DIR_PATH / file
    return settings._write_settings_file(path, token)  # pylint: disable=W0212
