import sys
import os
import importlib
from langchain.agents import tool as to_agent_tool
import types
import langchain_core
from .lib import ChangeDirectoryAndPath, ModuleManager, wrapped_func
from pycoze import utils


params = utils.read_params_file()

def _ref_workflows(workflow_id, as_agent_tool=False, workspace_path=None):
    if workspace_path is None:
        workspace_path = params["workspacePath"]
    tool_base_path = os.path.join(workspace_path, "User/Local/workflow")
    module_path = os.path.join(tool_base_path, workflow_id)
    module_path = os.path.normpath(os.path.abspath(module_path))

    if not os.path.exists(module_path):
        print(f"Workflow {workflow_id} not found")
        return []

    try:
        with ModuleManager(module_path) as manager:
            module = importlib.import_module("workflow")
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
        print(f"Error loading workflow {workflow_id}: {e}")
        return []

    for tool in export_tools:
        tool.func = wrapped_func(tool, module_path)
        if tool.description is None:
            tool.description = "This tool is used to " + tool.name + "."

    return export_tools if as_agent_tool else [tool.func for tool in export_tools]


def ref_workflow(workflow_id, as_agent_tool=False, workspace_path=None):
    tools = _ref_workflows(workflow_id, as_agent_tool=as_agent_tool, workspace_path=workspace_path)
    if len(tools) > 0:
        return tools[0]
    else:
        return None

