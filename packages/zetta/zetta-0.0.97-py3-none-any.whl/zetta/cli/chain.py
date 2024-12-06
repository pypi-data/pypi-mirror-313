# Copyright ZettaBlock Labs 2024
import typer
import os
import threading
import configparser
import requests
import itertools
import time
from zetta._utils.async_utils import synchronizer

chain_cli = typer.Typer(
    name="chain", help="Chain interaction", no_args_is_help=True
)

SERVICE_CHAIN_USER_REGISTER_URL = "https://neo-dev.prod.zettablock.com/v1/api/chain/user/register"

@chain_cli.command(name="user-registration", help="Register user on chain.")
@synchronizer.create_blocking
async def register_user(json: bool = False):
    zetta_root = os.path.expanduser("~")
    secrets_path = os.path.join(zetta_root, ".zetta/secrets")
    config = configparser.ConfigParser()
    config.read(secrets_path)
    token = config.get('default', 'token', fallback=None)
    register_user_on_chain(token)
    pass


def register_user_on_chain(token):
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=('Waiting for registering user on chain', stop_event))
    spinner_thread.start()
    headers = {
        "Authorization": token
    }
    body = {}
    response = requests.post(SERVICE_CHAIN_USER_REGISTER_URL, headers=headers, json=body)
    data = response.json()
    stop_event.set()
    spinner_thread.join()
    if response.status_code == 200:
        print("\nUser is registered!")
    else:
        if data['error'] != "user is already registered":
            raise ValueError(f"{data['error']}")
        else:
            print("\nUser is already registered")


def spinner(message: str, stop_event: threading.Event):
    for symbol in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        print(f'\r{message} {symbol}', end='', flush=True)  # Ensure the output is flushed
        time.sleep(1)
