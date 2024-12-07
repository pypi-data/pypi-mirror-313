from langchain_core.messages import HumanMessage, AIMessage
import threading
import json
from .agent import INPUT_MESSAGE, output, CHAT_DATA, clear_chat_data
from .agent_chat import agent_chat
import asyncio


def chat(bot_setting_file: str):
    history = []
    while True:
        input_text = input()
        if not input_text.startswith(INPUT_MESSAGE):
            raise ValueError("Invalid message")
        message = json.loads(input_text[len(INPUT_MESSAGE) :])
        history.append(HumanMessage(message["content"]))
        result = asyncio.run(agent_chat(bot_setting_file, history))
        output("assistant", result)
        history.append(AIMessage(result))


def get_chat_response(bot_setting_file: str, input_text: str):
    result = asyncio.run(agent_chat(bot_setting_file, [HumanMessage(input_text)]))
    return result
