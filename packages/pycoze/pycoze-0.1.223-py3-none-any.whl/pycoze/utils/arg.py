import sys
import json
import os


def read_arg(param, is_path=False, posix=True):
    while param.startswith("-"):
        param = param[1:]
    args = sys.argv[1:]
    value = None
    for i in range(len(args)):
        if args[i] == "-" + param or args[i] == "--" + param:
            value = args[i + 1]
            break
    if is_path and value:
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        if posix:
            value = value.replace("\\", "/")

    return value


