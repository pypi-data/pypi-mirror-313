from pycoze import utils
import json5
import re
from retrying import retry
from openai import OpenAI
import openai
import requests
import os


def never_retry_on_rate_limit_error(exception):
    """Return True if we should retry (in this case when it's NOT a RateLimitError), False otherwise"""
    return not isinstance(exception, openai.RateLimitError)

@retry(retry_on_exception=never_retry_on_rate_limit_error, wait_exponential_multiplier=500, stop_max_attempt_number=5)
def think(user_text, history, temperature=0.2, stop=None, **kwargs):
    user_msg = {"role": "user", "content": user_text}
    cfg = utils.read_json_file("llm.json")

    base_url = cfg["baseURL"]
    api_key = cfg["apiKey"]
    model = cfg["model"]

    base_url = base_url.replace("/chat/completions", "")

    client = OpenAI(api_key=api_key, base_url=base_url)

    response = client.chat.completions.create(model=model,
                                              messages=simple_history(history) + [user_msg],
                                              temperature=temperature,
                                              stop=stop)
    return response.choices[0].message.content


@retry(retry_on_exception=never_retry_on_rate_limit_error, wait_exponential_multiplier=500, stop_max_attempt_number=5)
def think_stream(user_text, history, temperature=0.2, stop=None, **kwargs):
    user_msg = {"role": "user", "content": user_text}
    cfg = utils.read_json_file("llm.json")

    base_url = cfg["baseURL"]
    api_key = cfg["apiKey"]
    model = cfg["model"]
    
    base_url = base_url.replace("/chat/completions", "")

    client = OpenAI(api_key=api_key, base_url=base_url)


    stream = client.chat.completions.create(model=model,
                                            messages=simple_history(history) + [user_msg],
                                            stream=True,
                                            temperature=temperature,
                                            stop=stop)
    for chunk in stream:
        yield chunk.choices[0].delta.content or ""


def simple_history(history):
    return [{"role": h["role"], "content": h["content"]} for h in history]


@retry(retry_on_exception=never_retry_on_rate_limit_error, wait_exponential_multiplier=500, stop_max_attempt_number=3)
def extract(response_data, text: str, temperature=0, **kwargs):
    """print(extract({"name": "lowercase"}, "hello XiaoMing"))"""
    if isinstance(response_data, dict):
        response_items = [[res, response_data[res]] for res in response_data]
    else:
        response_items = response_data

    json_text = ""
    for i, res in enumerate(response_items):
        comma = "," if i != len(response_items) - 1 else ""
        json_text += f'    "{res[0]}": {res[1]}{comma}\n'

    # Combine the provided text with the formatted JSON schema
    think_text = f"""
The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```" tags:
```json
{{
{json_text}
}}
```

Request:
{text}
"""
    # text放后面,当翻译等情况时,不会把"The output should"之类翻译了,导致错误
    markdown = think(think_text, [], temperature=temperature, **kwargs)
    pattern = r'```json(.*?)```'
    matches = re.findall(pattern, markdown, re.DOTALL)
    if matches:
        json_str = matches[0].strip() 
    # lines = [line.split("//")[0] for line in json_str.split("\n")]//这样当json中有//时会出错，例如https://
    json_dict = json5.loads(json_str)
    for item in response_items:
        if item[0] not in json_dict:
            raise "item:" + item + " not exists"
    return json_dict


def yes_or_no(question, temperature=0, **kwargs):
    result = extract([("Result", "Yes or No")], question, 
                     temperature=temperature, **kwargs)["Result"]
    if isinstance(result, bool):
        return result
    return result.upper() == "YES"


@retry(retry_on_exception=never_retry_on_rate_limit_error, wait_exponential_multiplier=500, stop_max_attempt_number=3)
def extract_code(text: str, temperature=0, language="python", markdown_word='python', **kwargs):
    """print(extract_code("sum 1~100"))"""
    think_text = text + f"""
The output should be a complete and usable {language} code snippet, including the leading and trailing "```{markdown_word}" and "```":
"""
    markdown = think(think_text, [], temperature=temperature, **kwargs)
    # 使用正则表达式匹配围绕在```{markdown_word} 和 ```之间的文本
    pattern = rf'```{markdown_word}(.*?)```'
    matches = re.findall(pattern, markdown, re.DOTALL)
    if matches:
        # 去除可能的前后空白字符
        return matches[0].strip()
    else:
        raise Exception("The string is not a valid python code.")


if __name__ == "__main__":
    print(think("你好", []))
    for chunk in think_stream("你好", []):
        print(chunk)
    print(extract({"name": "lowercase"}, "hello XiaoMing"))
    print(extract_code("sum 1~100"))