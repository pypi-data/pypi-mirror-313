# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

git_cli = typer.Typer(
    name="storage",
    help="[coming soon] in Zetta AI Network.",
    no_args_is_help=True,
)


@git_cli.command(name="clone", help="clone repo.")
@synchronizer.create_blocking
async def clone(json: bool = False):
    pass


@git_cli.command(name="add", help="add files for AI network.")
@synchronizer.create_blocking
async def add(json: bool = False):
    pass


@git_cli.command(name="commit", help="commit to the repo.")
@synchronizer.create_blocking
async def commit(json: bool = False):
    pass
