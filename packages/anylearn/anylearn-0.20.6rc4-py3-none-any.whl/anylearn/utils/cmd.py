import logging

import click


def _fmt_msg(msg: str, level: int=logging.INFO):
    return f"[ANYLEARN] [{logging.getLevelName(level)}] {msg}"


def cmd_error(msg: str):
    click.echo(click.style(_fmt_msg(msg, logging.ERROR), fg="red"))


def cmd_warning(msg: str):
    click.echo(click.style(_fmt_msg(msg, logging.WARNING), fg="yellow"))


def cmd_success(msg: str):
    click.echo(click.style(_fmt_msg(msg, logging.INFO), fg="green"))


def cmd_info(msg: str):
    click.echo(_fmt_msg(msg, logging.INFO))
