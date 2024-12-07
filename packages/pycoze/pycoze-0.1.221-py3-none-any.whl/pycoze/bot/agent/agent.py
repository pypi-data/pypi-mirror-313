import asyncio
import json
from langchain_openai import ChatOpenAI
from .chat import info
from .assistant import Runnable
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    AIMessageChunk,
    SystemMessage,
)
from langchain_core.agents import AgentFinish
from .agent_types.const import HumanToolString


async def run_agent(agent, inputs: list, tool_compatibility_mode: bool):
    exist_ids = set()
    content_list = []
    async for event in agent.astream_events(inputs, version="v2"):
        kind = event["event"]
        if kind == "on_chain_end":
            if "data" in event:
                if (
                    "output" in event["data"]
                    and event["data"]["output"] == "end"
                    and "input" in event["data"]
                    and isinstance(event["data"]["input"], list)
                ):
                    input_list = event["data"]["input"]
                    for msg in input_list:
                        if isinstance(msg, HumanMessage) or isinstance(msg, SystemMessage):
                            if not tool_compatibility_mode or not msg.content.startswith(HumanToolString):
                                content_list = []  # 防止内容重复
                        if isinstance(msg, AIMessage) and not isinstance(
                            msg, AIMessageChunk
                        ):
                            content = msg.content
                            if content:
                                content_list.append(content)
        elif kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                info("assistant", content)
        elif kind == "on_chain_start":
            data = event["data"]
            if "input" in data:
                input_list = (
                    data["input"]
                    if isinstance(data["input"], list)
                    else [data["input"]]
                )
                if len(input_list) == 0:
                    continue
                msg = input_list[-1]
                if isinstance(msg, AIMessage) and not isinstance(msg, AIMessageChunk):
                    if "tool_calls" in msg.additional_kwargs:
                        tool_calls = msg.additional_kwargs["tool_calls"]
                        for t in tool_calls:
                            if t["id"] in exist_ids:
                                continue
                            exist_ids.add(t["id"])
                            tool = t["function"]["name"]
                            info("assistant", f"\n[调用工具:{tool}]\n\n")

    return "\n".join(content_list)


if __name__ == "__main__":
    from langchain_experimental.tools import PythonREPLTool
    import threading

    llm_file = r"C:\Users\aiqqq\AppData\Roaming\pycoze\JsonStorage\llm.json"
    with open(llm_file, "r", encoding="utf-8") as f:
        cfg = json.load(f)
        chat = ChatOpenAI(
            api_key=cfg["apiKey"],
            base_url=cfg["baseURL"],
            model=cfg["model"],
            temperature=0,
        )
    python_tool = PythonREPLTool()
    agent = Runnable(
        agent_execution_mode="FuncCall",
        tools=[python_tool],
        llm=chat,
        assistant_message="请以女友的口吻回答，输出不小于100字，可以随便说点其他的",
        tool_compatibility_mode=False,
    )

    inputs = [HumanMessage(content="计算根号7+根号88")]
    print(asyncio.run(run_agent(agent, inputs, True, threading.Event())))