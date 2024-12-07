from typing import Sequence
from langchain.tools import BaseTool
from langchain_core.language_models.base import LanguageModelLike
from langchain_core.runnables import RunnableBinding
from .agent_types import create_openai_func_call_agent_executor


class Runnable(RunnableBinding):
    agent_execution_mode: str
    tools: Sequence[BaseTool]
    llm: LanguageModelLike
    assistant_message: str

    def __init__(
        self,
        *,
        agent_execution_mode: str,
        tools: Sequence[BaseTool],
        llm: LanguageModelLike,
        assistant_message: str,
        tool_compatibility_mode: bool
    ) -> None:

        agent_executor = create_openai_func_call_agent_executor(
            tools, llm, assistant_message, tool_compatibility_mode
        )
        agent_executor = agent_executor.with_config({"recursion_limit": 50})
        super().__init__(
            tools=tools,
            llm=llm,
            agent_execution_mode=agent_execution_mode,
            assistant_message=assistant_message,
            bound=agent_executor,
            return_intermediate_steps=True,
        )
