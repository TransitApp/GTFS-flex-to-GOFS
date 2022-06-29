import json

def save_file(filepath, json_data):
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(json.dumps(json_data, indent=4))
