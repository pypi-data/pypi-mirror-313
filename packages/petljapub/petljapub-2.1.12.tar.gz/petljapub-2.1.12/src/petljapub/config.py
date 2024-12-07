import appdirs
import json
import os
from . import logger

def config_dir():
    return os.path.join(appdirs.user_config_dir(), "petljapub")
    
def config_file_path():
    return os.path.join(config_dir(), "conf.json")

def write_config(config):
    try:        
        if not os.path.isdir(config_dir()):
            os.makedirs(config_dir())
        with open(config_file_path(), "w") as config_file:
            print(json.dumps(config), file=config_file)
        logger.info("Configuration writen in", config_file_path())
    except:
        logger.error("Error writing configuration file", config_file_path())

def read_config(key):
    try: 
        with open(config_file_path()) as config_file:
            json_content = config_file.read()
            config = json.loads(json_content)
            return config.get(key, None)
    except:
        return None

def add_configs(configs):
    try:
        if os.path.isfile(config_file_path()):
            with open(config_file_path()) as config_file:
                json_content = config_file.read()
                config = json.loads(json_content)
        else:
            config = dict()
            
        for key, value in configs.items():
            config[key] = value
        write_config(config)
        return True
    except:
        logger.error("Error adding configuration option", key, "=", value)
        return False
    
def add_config(key, value):
    return add_configs({key: value})

def remove_configs(keys):
    try:
        if os.path.isfile(config_file_path()):
            with open(config_file_path()) as config_file:
                json_content = config_file.read()
                config = json.loads(json_content)
        else:
            config = dict()

        for key in keys:
            config.pop(key, None)
        write_config(config)
        return True
    except:
        logger.error("Error removing configuration options", keys)
        return False

def remove_config(key):
    return remove_configs([key])
