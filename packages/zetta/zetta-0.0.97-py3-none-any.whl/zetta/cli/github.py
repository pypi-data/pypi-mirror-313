# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

github_cli = typer.Typer(
    name="github",
    help="Integration with github.",
    no_args_is_help=True,
)


@github_cli.command(name="import-token", help="import a new github token")
@synchronizer.create_blocking
async def import_token(json: bool = False):
    pass


@github_cli.command(name="auth", help="Authorize the github access.")
@synchronizer.create_blocking
async def auth(json: bool = False):
    pass
