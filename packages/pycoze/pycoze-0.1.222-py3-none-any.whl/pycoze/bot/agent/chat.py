import json
from langchain_core.messages import AIMessage


INPUT_MESSAGE = "INPUT_MESSAGE=>"
INTERRUPT_MESSAGE = "INTERRUPT_MESSAGE=>"
_OUTPUT_MESSAGE = "OUTPUT_MESSAGE=>"
_INFOMATION_MESSAGE = "INFOMATION_MESSAGE=>"
_LOG = "LOG=>"


CHAT_DATA = {"output":"", "info": ""}


def log(content, *args, end="\n", **kwargs):
    print(_LOG + content, *args, end=end, **kwargs)


def clear_chat_data():
    # 注意不能写为CHAT_DATA = {"output":"", "info": ""}，这样不会清空原本的内容
    CHAT_DATA["output"] = ""
    CHAT_DATA["info"] = ""


def output(role, content):
    assert role == "assistant"
    CHAT_DATA["output"] = content
    print(_OUTPUT_MESSAGE + json.dumps({"role": role, "content": content}))

def info(role, content):
    CHAT_DATA["info"] += content
    print(_INFOMATION_MESSAGE + json.dumps({"role": role, "content": content}))
