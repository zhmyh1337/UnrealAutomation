import json


with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

with open('secrets.json', 'r', encoding='utf-8') as f:
    secrets = json.load(f)

class Context():
    pass

ctx = Context()
