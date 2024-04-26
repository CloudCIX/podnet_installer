# stdlib
import json
import os.path
# libs
from jinja2 import Environment, FileSystemLoader


__all__ = [
    'config_file_exists',
    'config_filepath',
    'directory',
    'JINJA_ENV',
    'read_config_file',
    'update_config_file',
    'write_config_file',
]

config_filepath = '/etc/cloudcix/pod/configs/config.json'
directory = os.path.dirname(os.path.abspath(__file__))
JINJA_ENV = Environment(
    loader=FileSystemLoader(f'{directory}/templates'),
    trim_blocks=True,
    lstrip_blocks=True,
)


def config_file_exists():
    if os.path.exists(config_filepath):
        return True
    else:
        return False


def read_config_file():
    with open(config_filepath, 'r') as config_file:
        config = json.load(config_file)
    return config


def write_config_file(config_data):
    with open(config_filepath, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)


def update_config_file(key, value):
    # read
    config_data = read_config_file()
    config_data[key] = value
    # write
    write_config_file(config_data)
