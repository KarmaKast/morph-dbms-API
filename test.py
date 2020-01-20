import json
import os

config = {
    'env': '/data'
}

with open('cli_config.json', 'w') as file:
    json.dump(config, file)