# Copyright ZettaBlock Labs 2024
import typer
import os
import io
import webbrowser
import configparser
import requests
from zetta._utils.async_utils import synchronizer

huggingface_cli = typer.Typer(
    name="hf",
    help="Integration with huggingface.",
    no_args_is_help=True,
)

HUGGINGFACE_TOKEN_URL = "https://huggingface.co/settings/tokens"
SERIVCE_UPDATE_PROFILE_URL = "https://neo-dev.prod.zettablock.com/v1/api/user/profile"

@huggingface_cli.command(name="import-token", help="import a new huggingface token")
@synchronizer.create_blocking
async def import_token(json: bool = False):
    try:
        webbrowser.open(HUGGINGFACE_TOKEN_URL)
        token = input("Please enter your huggingface token:")
        nospace = token.replace(" ", "")
        if nospace == "":
            raise ValueError("empty token entered")
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        config.set('default', 'hf_token', token)
        with io.StringIO() as config_string:
            config.write(config_string)
            content = config_string.getvalue()
            content = content.rstrip('\n')
        with open(secrets_path, "w") as configfile:
            configfile.write(content)

        authToken = config.get('default', 'token', fallback=None)
        headers = {
            "Authorization": authToken
        }
        body = {
            "hf_token": token
        }
        response = requests.put(SERIVCE_UPDATE_PROFILE_URL, headers=headers, json=body)
        if response.status_code == 200:
            with open(secrets_path, 'r') as file:
                content = file.read()
                print(content,end="")
        else:
            raise ValueError(f"{response.json()['error']}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        pass


@huggingface_cli.command(name="auth", help="Authorize the huggingface access.")
@synchronizer.create_blocking
async def auth(json: bool = False):
    pass


@huggingface_cli.command(
    name="import", help="Import the huggingface model or data repo."
)
@synchronizer.create_blocking
async def import_repo(json: bool = False):
    pass
