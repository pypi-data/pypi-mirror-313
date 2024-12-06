# Copyright ZettaBlock Labs 2024
import typer
import os
import io
import configparser
import json
import requests
from termcolor import colored
from zetta._utils.async_utils import synchronizer
from rich import print_json

SERVICE_GET_USER_URL = "https://neo-dev.prod.zettablock.com/v1/api/user"
SERVICE_TOKEN_URL = "https://neo-dev.prod.zettablock.com/v1/api/user/token"

profile_cli = typer.Typer(
    name="profile",
    help="Manage your profile, only 1 profile could be active in Zetta AI Network.",
    no_args_is_help=True,
)


@profile_cli.command(name="logout", help="logout the current user")
@synchronizer.create_blocking
async def logout(json: bool = False):
    pass


@profile_cli.command(
    name="list", help="List all tokens and wallet for the current profile"
)
@synchronizer.create_blocking
async def list():
    try:
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get('default', 'token', fallback=None)
        headers = {
            "Authorization": token
        }
        response = requests.get(SERVICE_GET_USER_URL, headers=headers)
        data = response.json()
        if response.status_code == 200:
            print_array_info(data['data']['profile']['tokens'], "tokens")
            print_array_info(data['data']['profile']['api_keys'], "api keys")
            if 'hf_token' in data['data']['profile'] and data['data']['profile']['hf_token'] != "":
                print_info(data['data']['profile']['hf_token'], "hugging face token")
        else:
            response.raise_for_status()
    except Exception:
        print(f"An unexpected error occurred: {data['error']}")
    pass


def print_info(info, text_title):
    title = colored(text_title, "blue")
    box_width = max(70, len(text_title)+2)
    print(f"┌{'─' * 4} {title} {'─' * (box_width - len(text_title) - 8)}┐")
    print(f"│ {info}{' ' * (box_width-len(info)-4)} │")
    print(f"└{'─' * (box_width - 2)}┘")


def print_array_info(array, text_title):
    title = colored(text_title, "blue")
    line_length = 0
    for ele in array:
        lll = len(f"{ele['name']} {ele['id']}")
        if ele['is_default']:
            lll += 11
        line_length = max(lll, line_length)
    box_width = max(70, line_length+4)
    print(f"┌{'─' * 4} {title} {'─' * (box_width - len(text_title) - 8)}┐")
    for ele in array:
        name = ele['name']
        id = ele['id']
        ele_name = colored(name, "yellow")
        ele_info = f"{ele_name} {id}"
        ll = len(name) + len(id) + 1
        if ele['is_default']:
            ele_info += colored(" <- default", "green")
            ll += 11
        print(f"│ {ele_info}{' ' * (box_width-ll-4)} │")
    print(f"└{'─' * (box_width - 2)}┘")


@profile_cli.command(name="token-add", help="Add a token for the current profile")
@synchronizer.create_blocking
async def add_token(
    name: str = "",
    is_default: bool = False,
):
    try:
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get('default', 'token', fallback=None)
        headers = {
            "Authorization": token
        }
        body = {
            "name": name,
            "is_default": is_default
        }
        response = requests.post(SERVICE_TOKEN_URL, headers=headers, json=body)
        data = response.json()
        if response.status_code == 200:
            if data["data"]["is_default"] is True:
                config.clear()
                config.read(secrets_path)
                config.set('default', 'token', data["data"]["id"])
                with io.StringIO() as config_string:
                    config.write(config_string)
                    content = config_string.getvalue()
                    content = content.rstrip('\n')
                with open(secrets_path, "w") as configfile:
                    configfile.write(content)
            print("token added")
            print_json(json.dumps(data["data"], indent=4))
        else:
            response.raise_for_status()
    except Exception as e:
        print(f"An unexpected error occurred: {data['error'], {e}}")
    pass


@profile_cli.command(name="token-remove", help="remove a token for the current profile")
@synchronizer.create_blocking
async def remove_token(token_id: str):
    try:
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get('default', 'token', fallback=None)
        headers = {
            "Authorization": token
        }
        url = f"{SERVICE_TOKEN_URL}?id={token_id}"
        response = requests.delete(url, headers=headers)
        data = response.json()
        if response.status_code == 200:
            print("token removed")
            print_json(json.dumps(data["data"], indent=4))
        else:
            response.raise_for_status()
    except Exception:
        print(f"An unexpected error occurred: {data['error']}")
        pass


@profile_cli.command(name="token-update", help="update a token")
@synchronizer.create_blocking
async def update_token(
        token_id: str,
        name: str = "",
        is_default: bool = False,
        refresh: bool = False,
):
    try:
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get('default', 'token', fallback=None)
        headers = {
            "Authorization": token
        }
        body = {
            "name": name,
            "is_default": is_default,
            "refresh": refresh,
        }
        url = f"{SERVICE_TOKEN_URL}?id={token_id}"
        response = requests.put(url, headers=headers, json=body)
        data = response.json()
        if response.status_code == 200:
            if data["data"]["is_default"] is True:
                config.clear()
                config.read(secrets_path)
                config.set('default', 'token', data["data"]["id"])
                with io.StringIO() as config_string:
                    config.write(config_string)
                    content = config_string.getvalue()
                    content = content.rstrip('\n')
                with open(secrets_path, "w") as configfile:
                    configfile.write(content)
            print("token updated")
            print_json(json.dumps(data["data"], indent=4))
        else:
            response.raise_for_status()
    except Exception:
        print(f"An unexpected error occurred: {data['error']}")
        pass


@profile_cli.command(name="info", help="The current profile info")
@synchronizer.create_blocking
async def info(json: bool = False):
    try:
        zetta_root = os.path.expanduser("~")
        profile_path = os.path.join(zetta_root, ".zetta/profile")
        with open(profile_path, 'r') as file:
            content = file.read()
            lines = content.splitlines()
            for line in lines:
                if '=' in line:
                    key, value = line.split('=', 1)
                    print_info(value, key.strip().replace("_", ""))
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    pass
