import functools
import sys
import zipfile
from typing import Dict

import rich_click as click
from packaging.version import parse as parse_version
from requests.exceptions import ConnectionError
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table

from truefoundry.common.exceptions import BadRequestException
from truefoundry.deploy.cli.console import console
from truefoundry.deploy.lib.exceptions import (
    ConfigurationException,
)
from truefoundry.deploy.lib.util import is_debug_env_set


def setup_rich_click():
    click.rich_click.STYLE_ERRORS_SUGGESTION = "blue italic"
    click.rich_click.SHOW_ARGUMENTS = True
    click.rich_click.USE_RICH_MARKUP = True
    click.rich_click.STYLE_HELPTEXT = ""


def handle_exception(exception):
    if is_debug_env_set():
        console.print_exception(show_locals=True)
    if isinstance(exception, BadRequestException):
        print_dict_as_table_panel(
            {"Status Code": str(exception.status_code), "Error": exception.message},
            title="Command Failed",
            border_style="red",
        )
    elif isinstance(exception, ConnectionError):
        loc = ""
        if exception.request:
            loc = f" at {exception.request.url}"
        print_dict_as_table_panel(
            {
                "Error": f"Couldn't connect to TrueFoundry{loc}. Please make sure that the provided `--host` is correct."
            },
            title="Command Failed",
            border_style="red",
        )
    elif isinstance(exception, ConfigurationException):
        print_dict_as_table_panel(
            {"Error": exception.message},
            title="Command Failed",
            border_style="red",
        )
    else:
        print_dict_as_table_panel(
            {"Error": str(exception)},
            title="Command Failed",
            border_style="red",
        )


def handle_exception_wrapper(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            handle_exception(e)
            sys.exit(1)

    return inner


def print_error(message):
    text = Padding(message, (0, 1))
    console.print(
        Panel(
            text,
            border_style="red",
            title="Command failed",
            title_align="left",
            width=click.rich_click.MAX_WIDTH,
        )
    )


def print_message(message):
    text = Padding(message, (0, 1))
    console.print(
        Panel(
            text,
            border_style="cyan",
            title="Success",
            title_align="left",
            width=click.rich_click.MAX_WIDTH,
        )
    )


def print_dict_as_table_panel(
    dct: Dict[str, str],
    title: str,
    border_style: str = "cyan",
    key_color: str = "cyan",
):
    table = Table(show_header=False, box=None)
    table.add_column("Key", style=f"bold {key_color}", width=15)
    table.add_column("Value")
    for key, value in dct.items():
        table.add_row(key, value)
    console.print(
        Panel(
            table,
            border_style=border_style,
            title=title,
            title_align="left",
            width=click.rich_click.MAX_WIDTH,
        )
    )


def unzip_package(path_to_package, destination):
    with zipfile.ZipFile(path_to_package, "r") as zip_ref:
        zip_ref.extractall(destination)


def _prompt_if_no_value_and_supported(prompt: str, hide_input: bool = True):
    import click as _click

    kwargs = {}
    if parse_version(_click.__version__).major >= 8:
        kwargs = {"prompt": prompt, "hide_input": hide_input, "prompt_required": False}

    return kwargs
