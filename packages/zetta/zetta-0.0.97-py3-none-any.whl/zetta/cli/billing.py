# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

billing_cli = typer.Typer(
    name="billing", help="billing logs & history.", no_args_is_help=True
)


@billing_cli.command(name="history", help="Check the billing history.")
@synchronizer.create_blocking
async def get_balance(json: bool = False):
    pass
