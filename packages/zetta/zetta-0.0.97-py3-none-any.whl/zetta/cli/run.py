# Copyright ZettaBlock Labs 2024
import click


@click.command()
@click.option("--profile", type=click.Path(exists=True))
def login(profile):
    """Login to Zetta Workspace."""
    print(f"Logging in as {profile}...")
