# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

secret_cli = typer.Typer(
    name="secret", help="Manage secrets.", no_args_is_help=True
)

@secret_cli.command(name="list", help="")
@synchronizer.create_blocking
async def list(json: bool = False):
    pass

@secret_cli.command(name="get", help="Get the value of a secret.")
@synchronizer.create_blocking
async def get(key: str):
    pass

@secret_cli.command(name="set", help="Create a new secret.")
@synchronizer.create_blocking
async def set(key: str, value: str):
    pass
