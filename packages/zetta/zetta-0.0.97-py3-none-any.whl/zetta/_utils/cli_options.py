# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.connections import ai_network_endpoints

app = typer.Typer()

# Function to validate the environment
# Set default to devnet for now to avoid breaking changes
# TODO, Switch to testnet when ready
def common_env_option(default: str = "devnet"):
    # Define the option with a default value and help message
    def validate_env(env: str):
        valid_envs = ai_network_endpoints.keys()
        if env not in valid_envs:
            raise typer.BadParameter(f"Invalid environment '{env}'. Must be one of: {', '.join(valid_envs)}.")
        return env
    return typer.Option(default, help="Environment to use: 'devnet', 'testnet', or 'mainnet'", callback=validate_env)
