import os

import yaml
from fastapi_utils.tasks import *

CONFIG = None

class SubConfig:
    def __init__(self, **entries):
        for key, value in entries.items():
            setattr(self, key, value)

class AppConfig:
    def __init__(self, **entries):
        self.dict_config = entries
        for key, value in entries.items():
            # print('NLPBRIDGE Config loaded: ', key)
            setattr(self, key, SubConfig(**value))


# @repeat_every(seconds=10)
def reload_config():
    global CONFIG
    YAML_PATH = os.getenv("CONFIG_PATH")
    with open(YAML_PATH, 'r') as file:
        CONFIG = yaml.safe_load(file)
        CONFIG = AppConfig(**CONFIG)

        if CONFIG is None:
            raise Exception("Config file is empty")

reload_config()