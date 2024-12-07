import getpass

import petlja_api

from . import logger
from . import config

def _get_consent_to_store_password():
    consent = input(f"SECURITY WARNING: In the current version, the password to the petlja.org account is stored as plain text in the configuration file {config.config_file_path()}. Anyone having access to this file can read your password. If at any time you want to remove the login info, run \"petljapub remove-login-info\". Are you sure you want to continue? (yes/no)")
    return consent.lower() == "yes"

def set_petlja_login_info():
    if not _get_consent_to_store_password():
        logger.error("Login information not stored")
        return

    username = input("Enter Petlja username: ")
    password = getpass.getpass("Enter Petlja password: ")

    try:
        petlja_api.login(username, password)
    except PermissionError:
        logger.error("Wrong username or password")
        return

    config.add_configs({"username": username, "password": password})

def remove_petlja_login_info():
    config.remove_configs(["username", "password"])
    logger.info("Login information removed")

def get_petlja_session():
    username = config.read_config("username")
    password = config.read_config("password")
    if username is None or password is None:
        logger.info("To avoid entering your password every time, run \"petljapub set-login-info\" to remember your login information.")
        return petlja_api.login()
    return petlja_api.login(username, password)
