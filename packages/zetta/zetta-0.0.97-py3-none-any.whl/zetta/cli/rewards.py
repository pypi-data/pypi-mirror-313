# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

rewards_cli = typer.Typer(
    name="rewards", help="rewards history and dashboard.", no_args_is_help=True
)


@rewards_cli.command(name="history", help="Check rewards history.")
@synchronizer.create_blocking
async def history(json: bool = False):
    pass


@rewards_cli.command(
    name="dataset", help="Check rewards history for a particular dataset."
)
@synchronizer.create_blocking
async def dataset(json: bool = False):
    pass


@rewards_cli.command(name="model", help="Check rewards history for a particular model.")
@synchronizer.create_blocking
async def model(json: bool = False):
    pass
