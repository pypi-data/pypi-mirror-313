import sys
import os
import importlib
from langchain.agents import tool as to_agent_tool
import types
import langchain_core
from .lib import ChangeDirectoryAndPath, ModuleManager, wrapped_func
import json
from pycoze import utils

bot_index  = 0

params = utils.read_params_file()

def ref_bot(bot_id, as_agent_tool=False, workspace_path=None):
    global bot_index
    if workspace_path is None:
        workspace_path = params["workspacePath"]
    tool_base_path = os.path.join(workspace_path, "User/Local/bot")
    module_path = os.path.join(tool_base_path, bot_id)
    module_path = os.path.normpath(os.path.abspath(module_path))
    
    if not os.path.exists(module_path):
        print(f"Bot {bot_id} not found in:"+ module_path)
        return None
    
    try:
        with ModuleManager(module_path) as manager:
            info = module_path + "/info.json"
            with open(info, "r", encoding="utf-8") as f:
                info = json.load(f)
            name = info["name"]
            random_name = "bot_" + str(bot_index)
            bot_index += 1
            function_code = f"""
def {random_name}(command:str) -> str:
    \"\"\"接收任意指令字符串，并返回AI角色（{name}专家）深入思考和执行指令后的字符串结果。
    AI角色（{name}专家）擅长使用各种工具，并会给出专业且更为准确的结果。

    Args:
        command (str): AI角色（{name}专家）需要执行的指令字符串。

    Returns:
        str: AI角色（{name}专家）执行指令后的结果。
    \"\"\"
    from pycoze import bot
    from pycoze import utils
    import tempfile
    
    with tempfile.NamedTemporaryFile(delete=True, mode='w+t') as temp_file:
        sys.stdout = temp_file  # 将输出重定向到临时文件，防止影响AI结果
        result = bot.get_chat_response("botSetting.json", command)
        sys.stdout = sys.__stdout__  # 恢复标准输出
    return result
"""
            exec(function_code)
            tool = to_agent_tool(eval(random_name))
            tool.func = wrapped_func(tool, module_path)
            if tool.description is None:
                tool.description = "This tool is used to " + tool.name + "."
            return tool if as_agent_tool else tool.func
    except Exception as e:
        print(f"Error loading bot {bot_id}: {e}")
        return None