import typer
from rich import print

import anylearn.cli.jupload as jupload
from anylearn.cli._utils import HostArgument
from anylearn.sdk.auth import authenticate, disauthenticate
from anylearn.__about__ import __version__ as anylearn_version


app = typer.Typer(name="anyctl")
app.add_typer(jupload.app, name="jupload")


@app.command()
def login(host: str = HostArgument):
    if authenticate(host) is not None:
        print("[green]Login OK[/green]")
    else:
        print("[red]Login Failed[/red]")


@app.command()
def logout(host: str = HostArgument):
    disauthenticate(host)
    print("[green]Logout OK[/green]")


def version_callback(value: bool):
    if value:
        print(f"[green]{anylearn_version}")
        raise typer.Exit()


@app.callback()
def common(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version and exit.",
        is_eager=True,
        callback=version_callback,
    ),
):
    pass
