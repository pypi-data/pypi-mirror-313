import logging
import sys

import rich_click as click

from truefoundry import logger
from truefoundry.deploy.cli.commands import (
    get_apply_command,
    get_build_command,
    get_delete_command,
    get_deploy_command,
    get_login_command,
    get_logout_command,
    get_patch_application_command,
    get_patch_command,
    get_terminate_command,
    get_trigger_command,
)
from truefoundry.deploy.cli.config import CliConfig
from truefoundry.deploy.cli.const import GROUP_CLS
from truefoundry.deploy.cli.util import setup_rich_click
from truefoundry.deploy.lib.util import is_debug_env_set, is_internal_env_set
from truefoundry.version import __version__

click.rich_click.USE_RICH_MARKUP = True


def create_truefoundry_cli() -> click.MultiCommand:
    """Generates CLI by combining all subcommands into a main CLI and returns in

    Returns:
        function: main CLI functions will all added sub-commands
    """
    cli = truefoundry_cli
    cli.add_command(get_login_command())
    cli.add_command(get_logout_command())
    cli.add_command(get_apply_command())
    cli.add_command(get_deploy_command())
    cli.add_command(get_patch_application_command())
    cli.add_command(get_delete_command())
    cli.add_command(get_trigger_command())
    cli.add_command(get_terminate_command())

    if not (sys.platform.startswith("win32") or sys.platform.startswith("cygwin")):
        cli.add_command(get_patch_command())

    if is_internal_env_set():
        cli.add_command(get_build_command())
    return cli


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])  # noqa: C408


@click.group(
    cls=GROUP_CLS, context_settings=CONTEXT_SETTINGS, invoke_without_command=True
)
@click.option(
    "--json",
    is_flag=True,
    help="Output entities in json format instead of formatted tables",
)
@click.option(
    "--debug",
    is_flag=True,
    default=is_debug_env_set,
    help="Set logging level to Debug. Can also be set using environment variable. E.g. SFY_DEBUG=1",
)
@click.version_option(__version__)
@click.pass_context
def truefoundry_cli(ctx, json, debug):
    """
    TrueFoundry provides an easy way to deploy your Services, Jobs and Models.
    \b

    To start, login to your TrueFoundry account with [b]tfy login[/]

    Then start deploying with [b]tfy deploy[/]

    And more: [link=https://docs.truefoundry.com/docs]https://docs.truefoundry.com/docs[/]

    """
    setup_rich_click()
    # TODO (chiragjn): Change this to -o json|yaml|table|pager
    CliConfig.set("json", json)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    log_level = logging.INFO
    # no info logs while outputting json
    if json:
        log_level = logging.ERROR
    if debug:
        log_level = logging.DEBUG
    logger.add_cli_handler(level=log_level)
