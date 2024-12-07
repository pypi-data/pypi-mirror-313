import sys
import os
import importlib
from langchain.agents import tool as to_agent_tool
import types
import langchain_core
from .lib import ChangeDirectoryAndPath, ModuleManager, wrapped_func
from pycoze import utils


params = utils.read_params_file()

def ref_tools(tool_id, as_agent_tool=False, workspace_path=None):
    if workspace_path is None:
        workspace_path = params["workspacePath"]
    tool_base_path = os.path.join(workspace_path, "User/Local/tool")
    module_path = os.path.join(tool_base_path, tool_id)
    module_path = os.path.normpath(os.path.abspath(module_path))

    if not os.path.exists(module_path):
        print(f"Tool {tool_id} not found")
        return []

    try:
        with ModuleManager(module_path) as manager:
            module = importlib.import_module("tool")
            export_tools = getattr(module, "export_tools")
            valid_tools = []
            for tool in export_tools:
                assert isinstance(tool, langchain_core.tools.StructuredTool) or isinstance(
                    tool, types.FunctionType
                ), f"Tool is not a StructuredTool or function: {tool}"
                if not isinstance(tool, langchain_core.tools.StructuredTool):
                    tool = to_agent_tool(tool)
                valid_tools.append(tool)
            export_tools = valid_tools

    except Exception as e:
        print(f"Error loading tool {tool_id}: {e}")
        return []

    for tool in export_tools:
        tool.func = wrapped_func(tool, module_path)
        if tool.description is None:
            tool.description = "This tool is used to " + tool.name + "."

    return export_tools if as_agent_tool else [tool.func for tool in export_tools]
