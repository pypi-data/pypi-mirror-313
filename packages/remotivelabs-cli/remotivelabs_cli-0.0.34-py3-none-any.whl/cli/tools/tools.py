import typer

from .can.can import app as can_app

HELP_TEXT = """
CLI tools unrelated to cloud or broker
"""

app = typer.Typer(help=HELP_TEXT)
app.add_typer(can_app, name="can", help="CAN tools")
