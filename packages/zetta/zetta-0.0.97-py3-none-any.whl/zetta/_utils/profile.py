# Copyright ZettaBlock Labs 2024
import configparser
import os

def get_zetta_profile():
    try:
        zetta_root = os.path.expanduser("~")
        profile_path = os.path.join(zetta_root, ".zetta/profile")
        config = configparser.ConfigParser()
        config.read(profile_path)
        return config
    except FileNotFoundError:
        raise Exception(f"Zetta profile not found at {profile_path}")
    except IOError:
        raise Exception(f"An error occurred while reading Zetta profile {profile_path}")

def get_zetta_secrets():
    try:
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        return config
    except FileNotFoundError:
        raise Exception(f"Zetta secrets not found at {secrets_path}")
    except IOError:
        raise Exception(f"An error occurred while reading Zetta secrets {secrets_path}")
