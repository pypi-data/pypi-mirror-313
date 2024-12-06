from rich import print


def console_error(message: str) -> None:
    print(f"[red]Error: {message}[/red]")


def console_warning(message: str) -> None:
    print(f"[yellow]Warining: {message}[/yellow]")


def console_success(message: str) -> None:
    print(f"[green]{message}[/green]")
