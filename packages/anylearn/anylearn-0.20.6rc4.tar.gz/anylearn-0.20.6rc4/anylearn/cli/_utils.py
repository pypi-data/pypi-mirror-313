import typer

from anylearn.sdk.utils import DEFAULT_ANYLEARN_HOST


HostArgument = typer.Argument(
    default=DEFAULT_ANYLEARN_HOST,
    help="The url (scheme included) of Anylearn to connect with.",
    show_default=True,
)


HostOption = typer.Option(
    DEFAULT_ANYLEARN_HOST,
    "--host",
    "-h",
    help="The url (scheme included) of Anylearn to connect with.",
    show_default=True,
)
