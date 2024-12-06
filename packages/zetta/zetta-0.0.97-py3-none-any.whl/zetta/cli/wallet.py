# Copyright ZettaBlock Labs 2024
import os
import io
import requests
import typer
import json as j
from rich import print_json
import configparser
from zetta._utils.async_utils import synchronizer

wallet_cli = typer.Typer(
    name="wallet", help="Manage your wallets in Zetta AI Network.", no_args_is_help=True
)

HOST = "https://neo-dev.prod.zettablock.com"
#  HOST = "http://127.0.0.1:8099"

@wallet_cli.command(name="create", help="Create a new wallet for current user.")
@synchronizer.create_blocking
async def create(
    name: str = "",
    is_default: bool = False,
):
    headers = {
        "Authorization": getToken()
    }
    body = {
        "name": name,
        "default": is_default,
    }
    print(body)
    response = requests.post(f"{HOST}/v1/api/user/wallet", headers=headers, json=body)
    data = response.json()
    if response.status_code == 200:
        if is_default:
            config = configparser.ConfigParser()
            zetta_root = os.path.expanduser("~")
            profile_path = os.path.join(zetta_root, ".zetta/profile")
            config.read(profile_path)
            config.set('default', 'wallet_address', data["data"]["id"])
            with io.StringIO() as config_string:
                config.write(config_string)
                content = config_string.getvalue()
                content = content.rstrip('\n')
            with open(profile_path, "w") as configfile:
                configfile.write(content)
        print_json(j.dumps(data["data"], indent=4))
    else:
        raise ValueError(data['error'])
    pass


@wallet_cli.command(name="list", help="Import a new wallet for current user.")
@synchronizer.create_blocking
async def list_wallets(json: bool = False):
    headers = {
        "Authorization": getToken()
    }
    response = requests.get(f"{HOST}/v1/api/user/wallets", headers=headers)
    data = response.json()
    if response.status_code == 200:
        print_json(j.dumps(data["data"], indent=4))
    else:
        raise ValueError(data['error'])
    pass


@wallet_cli.command(name="import", help="Import a new wallet for current user.")
@synchronizer.create_blocking
async def import_wallet(
    name: str = "",
    private_key: str = "",
    is_default: bool = False,
):
    if private_key == "" or private_key is None:
        raise ValueError("Invalid private key")
    headers = {
        "Authorization": getToken()
    }
    body = {
        "name": name,
        "default": is_default,
        "import": {
            "private_key": private_key
        }
    }
    response = requests.post(f"{HOST}/v1/api/user/wallet", headers=headers, json=body)
    data = response.json()
    if response.status_code == 200:
        if is_default:
            config = configparser.ConfigParser()
            zetta_root = os.path.expanduser("~")
            profile_path = os.path.join(zetta_root, ".zetta/profile")
            config.read(profile_path)
            config.set('default', 'wallet_address', data["data"]["id"])
            with io.StringIO() as config_string:
                config.write(config_string)
                content = config_string.getvalue()
                content = content.rstrip('\n')
            with open(profile_path, "w") as configfile:
                configfile.write(content)
        print_json(j.dumps(data["data"], indent=4))
    else:
        raise ValueError(data['error'])
    pass


@wallet_cli.command(name="bind", help="bind to a wallet for current user.")
@synchronizer.create_blocking
async def bind(id):
    headers = {
        "Authorization": getToken()
    }
    body = {
        "id": id,
        "default": True,
    }
    response = requests.put(f"{HOST}/v1/api/user/wallet", headers=headers, json=body)
    data = response.json()
    if response.status_code == 200:
        print_json(j.dumps(data["data"], indent=4))
    else:
        raise ValueError(data['error'])
    pass


@wallet_cli.command(name="balance", help="get balance for the current wallet")
@synchronizer.create_blocking
async def balance(id: str = ""):
    headers = {
        "Authorization": getToken()
    }
    response = requests.get(f"{HOST}/v1/api/user/wallet/balance?id={id}", headers=headers)
    data = response.json()
    if response.status_code == 200:
        print_json(j.dumps(data["data"], indent=4))
    else:
        raise ValueError(data['error'])
    pass


def getToken():
    zetta_root = os.path.expanduser("~")
    secrets_path = os.path.join(zetta_root, ".zetta/secrets")
    config = configparser.ConfigParser()
    config.read(secrets_path)
    token = config.get('default', 'token', fallback=None)
    return token
