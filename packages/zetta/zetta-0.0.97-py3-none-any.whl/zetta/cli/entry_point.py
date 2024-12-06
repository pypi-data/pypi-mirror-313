# Copyright ZettaBlock Labs 2024
import typer

from zetta.cli.billing import billing_cli
from zetta.cli.dataset import dataset_cli
from zetta.cli.datasets_v2 import datasetsv2_cli
from zetta.cli.huggingface import huggingface_cli
from zetta.cli.marketplace import marketplace_cli
from zetta.cli.model import model_cli
from zetta.cli.profile import profile_cli
from zetta.cli.github import github_cli
from zetta.cli.rewards import rewards_cli
from zetta.cli.secret import secret_cli
from zetta.cli.serving import serving_cli
from zetta.cli.wallet import wallet_cli
from zetta.cli.chain import chain_cli
from .job import job_cli
from .setup import setup


entrypoint_cli_typer = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="markdown",
    help="""
    Zetta stands for a better AI economics

    See the website at https://zettablock.com/ for documentation and more information
    about running code on ZettaBlock AI network.
    """,
)


def version_callback(value: bool):
    if value:
        from zetta_version import __version__

        typer.echo(f"zetta client version: {__version__}")
        raise typer.Exit()


@entrypoint_cli_typer.callback()
def zetta(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    pass


# Config
entrypoint_cli_typer.add_typer(profile_cli, rich_help_panel="Config")
entrypoint_cli_typer.add_typer(secret_cli, rich_help_panel="Config")
entrypoint_cli_typer.add_typer(wallet_cli, rich_help_panel="Config")

# Artifact
entrypoint_cli_typer.add_typer(model_cli, rich_help_panel="Artifact")
entrypoint_cli_typer.add_typer(dataset_cli, rich_help_panel="Artifact")
entrypoint_cli_typer.add_typer(datasetsv2_cli, rich_help_panel="Artifact")

# Integration
entrypoint_cli_typer.add_typer(github_cli, rich_help_panel="Integration")
entrypoint_cli_typer.add_typer(huggingface_cli, rich_help_panel="Integration")

# AI network
entrypoint_cli_typer.add_typer(job_cli, rich_help_panel="AI Network")
entrypoint_cli_typer.add_typer(serving_cli, rich_help_panel="AI Network")

# Marketplace
entrypoint_cli_typer.add_typer(marketplace_cli, rich_help_panel="Marketplace")

# Billing & Rewards
entrypoint_cli_typer.add_typer(billing_cli, rich_help_panel="Billing & Rewards")
entrypoint_cli_typer.add_typer(rewards_cli, rich_help_panel="Billing & Rewards")

# Chain
entrypoint_cli_typer.add_typer(chain_cli, rich_help_panel="Chain")

# Onboarding flow
entrypoint_cli_typer.command(
    "setup", help="Bootstrap Zetta's configuration.", rich_help_panel="Onboarding"
)(setup)


entrypoint_cli = typer.main.get_command(entrypoint_cli_typer)
entrypoint_cli.list_commands(None)  # type: ignore


if __name__ == "__main__":
    # this module is only called from tests, otherwise the parent package __main__.py is used as the entrypoint
    entrypoint_cli()
