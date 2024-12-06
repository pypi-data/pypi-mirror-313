# Copyright ZettaBlock Labs 2024
import os
import io
import pyfiglet
import requests
import configparser
import webbrowser
import itertools
import time
import threading
from zetta._utils.async_utils import synchronizer

SERVICE_SIGNIN_URL = "https://stage-app.zettablock.dev/aiweb/tokens"
SERVICE_GET_USER_URL = "https://neo-dev.prod.zettablock.com/v1/api/user"
SERVICE_REGISTER_ADDRESS_URL = "https://neo-dev.prod.zettablock.com/v1/api/user/address"
SERVICE_CHAIN_DEPOSIT_URL = "https://neo-dev.prod.zettablock.com/v1/api/chain/deposit"
CHAIN_ENDPOINT = "https://sepolia.base.org"

@synchronizer.create_blocking
async def setup():
    try:
        block_text = pyfiglet.figlet_format("ZETTA", font="block")
        block_text = block_text.rstrip()
        print(f"{block_text}\n")
        zetta_root = os.path.expanduser("~")
        zetta_dir = setup_zettadir(zetta_root)
        webbrowser.open(SERVICE_SIGNIN_URL)
        token = input("To finish the setup, `zetta` requires a token generated from https://stage-app.zettablock.dev/aiweb/tokens: ")
        profile_data = get_user_profile(token)
        #  choice = click.prompt(
        #      "To finish the setup, `zetta` requires your wallet private key, create or import?",
        #      type=click.Choice(['create', 'import'], case_sensitive=False)
        #  )
        #  wallet_private_key = secrets.token_hex(32)
        #  if choice == 'import':
        #      wallet_private_key = input("Please input your private key: ")
        #      if wallet_private_key.startswith('0x'):
        #          wallet_private_key = wallet_private_key[2:]
        #      if is_valid_token_hex(wallet_private_key) is False:
        #          raise ValueError("Invalid wallet private key: the key must be a valid 64-character hexadecimal string (32 length).")
        #  if not wallet_private_key.startswith('0x'):
        #      wallet_private_key = '0x' + wallet_private_key
        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=spinner, args=('Generating your local `zetta` config', stop_event))
        spinner_thread.start()
        #  account: LocalAccount = Account.from_key(wallet_private_key)
        #  w3 = Web3(Web3.HTTPProvider(CHAIN_ENDPOINT))
        #  w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
        #  register_address(account.address, token)
        #  amount= input("How much do you want to deposit from your wallet to AI network contract: ")
        #  deposit_to_contract(amount, token, wallet_private_key)
        generate_profile_file(zetta_dir, profile_data)
        stop_event.set()
        spinner_thread.join()
        print("\n")
        print_directory_structure(zetta_dir)
        print("\nYour are all set to use AI network!")
    except Exception as e:
        print(f"An error occurred: {e}")
    pass


def spinner(message: str, stop_event: threading.Event):
    for symbol in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        print(f'\r{message} {symbol}', end='', flush=True)  # Ensure the output is flushed
        time.sleep(1)


def deposit_to_contract(amount, token):
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=('Waiting for deposit to be finished', stop_event))
    spinner_thread.start()
    headers = {
        "Authorization": token
    }
    body = {
        "amount": int(amount),
    }
    response = requests.post(SERVICE_CHAIN_DEPOSIT_URL, headers=headers, json=body)
    data = response.json()
    stop_event.set()
    spinner_thread.join()
    if response.status_code == 200:
        print("\nDeposit is successful!")
    else:
        raise ValueError(data['error'])


def register_address(address, token):
    headers = {
        "Authorization": token
    }
    body = {
        "user_address": address
    }
    response = requests.put(SERVICE_REGISTER_ADDRESS_URL, headers=headers, json=body)

    data = response.json()
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(data['error'])


def is_valid_token_hex(key, length=32):
    try:
        int(key, 16)
    except ValueError:
        return False
    expected_length = length * 2
    return len(key) == expected_length


def get_value_from_file(zetta_dir, key):
    file_path = os.path.join(zetta_dir, "secrets")
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None
    config = configparser.ConfigParser()
    config.read(file_path)
    value = config.get('default', key, fallback=None)
    if value is None or value == "":
        return None
    return value


def get_user_profile(token):
    headers = {
        "Authorization": token
    }
    response = requests.get(SERVICE_GET_USER_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def existed(d, key):
    if d[key] != "" and d[key] is not None:
        return True
    return False


def generate_profile_file(zetta_dir, profile_data, profile_name="default"):
    config = configparser.ConfigParser()
    config[profile_name] = {}
    if existed(profile_data["data"]["profile"], "tokens"):
        for token in profile_data["data"]["profile"]["tokens"]:
            if token.get("is_default"):
                config[profile_name]["token"] = token["id"]
                break
    if existed(profile_data["data"]["profile"], "api_keys"):
        for api_key in profile_data["data"]["profile"]["api_keys"]:
            if api_key.get("is_default"):
                config[profile_name]["api_key"] = api_key["id"]
                break
    if existed(profile_data["data"]["profile"], "git_token"):
        config[profile_name]["git_token"] = profile_data["data"]["profile"]["git_token"]
    if existed(profile_data["data"]["profile"], "hf_token"):
        config[profile_name]["hf_token"] = profile_data["data"]["profile"]["hf_token"]
    #  if existed(profile_data["data"]["profile"], "github_token"):
        #  config[profile_name]["github_token"] = profile_data["data"]["profile"]["github_token"]

    file_path = os.path.join(zetta_dir, "secrets")
    with io.StringIO() as config_string:
        config.write(config_string)
        content = config_string.getvalue()
        content = content.rstrip('\n')
    with open(file_path, "w") as configfile:
        configfile.write(content)

    config.clear()
    config[profile_name] = {}
    if existed(profile_data["data"]["user"], "tenant"):
        config[profile_name]["tenant"] = profile_data["data"]["user"]["tenant"]
    if existed(profile_data["data"]["user"], "user_name"):
        config[profile_name]["user_name"] = profile_data["data"]["user"]["user_name"]
    if existed(profile_data["data"]["user"], "email"):
        config[profile_name]["email"] = profile_data["data"]["user"]["email"]
    if existed(profile_data["data"]["profile"], "wallets"):
        for wallet in profile_data["data"]["profile"]["wallets"]:
            if wallet.get("is_default"):
                config[profile_name]["wallet_address"] = wallet["address"]
                break
    file_path = os.path.join(zetta_dir, "profile")
    with io.StringIO() as config_string:
        config.write(config_string)
        content = config_string.getvalue()
        content = content.rstrip('\n')
    with open(file_path, "w") as configfile:
        configfile.write(content)


def print_directory_structure(root_dir):
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = '│   ' * level + '├── ' if level > 0 else ''
        if os.path.basename(root) == ".zetta":
            print(f"{indent}{root}/")
        else:
            print(f"{indent}{os.path.basename(root)}/")
        sub_indent = '│   ' * (level + 1) + '├── '
        for f in files:
            print(f"{sub_indent}{f}")


def setup_zettadir(zetta_root):
    zetta_dir = os.path.join(zetta_root, ".zetta")
    if not os.path.exists(zetta_dir):
        os.makedirs(zetta_dir)
    return zetta_dir
