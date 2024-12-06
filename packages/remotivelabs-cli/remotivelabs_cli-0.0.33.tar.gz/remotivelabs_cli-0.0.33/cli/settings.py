from __future__ import annotations

import sys
from pathlib import Path

from rich.console import Console

err_console = Console(stderr=True)

# pylint: disable-next=W0511
# TODO: We probably want this to be both configurable, and testable. The best solution would probably be to refactor this module into a
# proper class, and configure it similar to logging.
CONFIG_DIR_PATH = Path.home() / ".config" / ".remotive/"
TOKEN_SECRET_FILE_PATH = CONFIG_DIR_PATH / "cloud.secret.token"


class InvalidSettingsFileError(Exception):
    """Raised when trying to access an invalid settings file or file path"""


def read_secret_token() -> str:
    if not TOKEN_SECRET_FILE_PATH.exists():
        err_console.print(":boom: [bold red]Access failed[/bold red] - No access token found")
        err_console.print("Login with [italic]remotive cloud auth login[/italic]")
        err_console.print(
            "If you have downloaded a personal access token, you can activate "
            "it with [italic]remotive cloud auth tokens activate [FILE_NAME][/italic]"
        )
        sys.exit(1)

    return _read_file(TOKEN_SECRET_FILE_PATH)


def list_personal_token_files() -> list[Path]:
    return [f for f in CONFIG_DIR_PATH.iterdir() if f.is_file() and f.name.startswith("personal-")]


def list_service_account_token_files() -> list[Path]:
    return [f for f in CONFIG_DIR_PATH.iterdir() if f.is_file() and f.name.startswith("service-account-")]


def write_secret_token(secret: str) -> Path:
    return _write_settings_file(TOKEN_SECRET_FILE_PATH, secret)


def clear_secret_token() -> None:
    TOKEN_SECRET_FILE_PATH.unlink()


def _read_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write_settings_file(path: Path, data: str) -> Path:
    if CONFIG_DIR_PATH not in path.parents:
        raise InvalidSettingsFileError(f"file {path} not in settings dir {CONFIG_DIR_PATH}")

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf8") as f:
        f.write(data)

    return path
