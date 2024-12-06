import rich_click as click

from truefoundry.ml.cli.commands import download

click.rich_click.USE_RICH_MARKUP = True


@click.group()
def ml():
    """
    TrueFoundry ML CLI
    """
    pass


def get_ml_cli():
    ml.add_command(download)
    return ml
