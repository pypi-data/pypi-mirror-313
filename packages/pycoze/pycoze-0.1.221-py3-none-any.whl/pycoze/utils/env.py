import os
import json


def read_params_file():
    params_file = os.getenv("params_file", None)
    params = None
    if params_file:
        try:
            with open(params_file, "r", encoding="utf-8") as f:
                params = json.load(f)
        except Exception as e:
            print(e)
    return params

def read_json_file(filename):
    params = read_params_file()
    json_file = os.path.join(params['appPath'], 'JsonStorage', filename)
    with open(json_file, encoding='utf-8') as f:
        return json.load(f)
        