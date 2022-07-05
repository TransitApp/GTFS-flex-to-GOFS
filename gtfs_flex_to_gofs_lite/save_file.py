import json

from numpy import var


def save_file(filepath, json_data):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_data, indent=4, default=vars))
