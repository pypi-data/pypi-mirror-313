# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

async_cli = typer.Typer(
    name="example", help="Internal example for async/RPC calls.", no_args_is_help=True
)


@async_cli.command("get-block-number")
@synchronizer.create_blocking
async def get_block_number(json: bool = False):
    """Get the latest block number from ethereum, mainly display a standard async call pattern for reference."""
    # TODO
    pass
