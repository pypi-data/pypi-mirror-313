import json
from pycoze import utils
import json
import inspect


params = utils.read_params_file()


def get_ui():
    if params is None or "uiData" not in params or "uiRecord" not in params["uiData"]:
        return {}
    stack = inspect.stack()
    stack_files = list(reversed([s.filename.replace("\\", "/") for s in stack]))
    match_ui_file = None
    for f in stack_files:
        for v in params["uiData"]["uiRecord"]:
            if v == f:
                match_ui_file = v
                break
        if match_ui_file is not None:
            break

    if match_ui_file is None:
        return {}

    by = params["uiData"]["by"]

    for i in range(10):
        try:
            if by == "file":
                json_file = params["uiData"]["uiRecord"][match_ui_file]
                with open(json_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                assert by == "workflow"
                return params["uiData"]["uiRecord"][match_ui_file]
        except Exception as e:
            if i == 9:
                raise e
