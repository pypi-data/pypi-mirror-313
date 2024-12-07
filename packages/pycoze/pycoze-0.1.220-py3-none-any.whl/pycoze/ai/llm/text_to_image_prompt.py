import re
from .. import yes_or_no
from .. import extract


def contains_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')  # Regular expression to match Chinese characters
    return bool(re.search(pattern, text))


requirement = """
Please reflect the scene content as prompts for the drawing AI.

## Prompt Concept
- A prompt is used to describe the image content, composed of common words, using English commas (",") as separators. For example, a prompt like "woman" indicates that the image should include a woman.

## Tag Restrictions
- Tags should be described using English words or phrases, avoiding Chinese.
- Tags can only contain keywords or key phrases, and should not include personal names, place names, etc.
- Tags should try to preserve physical characteristics of people, like body shape and hairstyle, but not use personal names, instead using terms like "man" to refer to people.
- The number of tags in a prompt is limited to 40, and the number of words is limited to 60.

## Incorrect Examples of Prompts
"In the bustling Shanghai Bund, there is a young man named Li Yang."
The prompt includes non-keywords like "there is", as well as the personal name "Li Yang" and the place name "Shanghai."
It should be modified to "a young man, in the bustling Bund"

"""

# As the LLM used is not very effective, negative prompts are not suitable for generation by LLM at this stage
# - Negative prompts describe content that should not appear in the image, for example if "bird, man" appears in the negative prompt, it means the image should not include "birds and men".


def text_to_image_prompt(query, style, negative_style, with_prompt="best quality,4k,", with_negative_prompt=""):
    query = query.replace("{", "【").replace("}", "】")
    needed = f"The scene I need: {query}"
    style = style.replace(",", " ").replace("，", " ")
    if len(style) > 0:
        needed += f"\nThe style I need: {style}"
    # if len(negative_style) > 0:
    #     needed += f"\nStyles to avoid: {negative_style}"

    for i in range(15):
        try:
            print("doing")
            output_obj = extract([("prompt", "Describe the image content with keywords")], needed + "\n" + requirement)
            print("done")
            if contains_chinese(output_obj["prompt"]):
                print("Contains Chinese, regenerating")
                continue
            if yes_or_no("Does it include personal names:\n"+output_obj["prompt"]):
                print(output_obj["prompt"]+" contains personal names, correcting")
                output_obj["prompt"] = extract(
                    [("text without personal names", "Modified result (personal names can be changed to man, woman, he, she, etc.)")],
                    "Modify the following text, personal names can be changed to man, woman, he, she, etc.: \n"+output_obj["prompt"])["text without personal names"]
            break
        except Exception as e:
            print(e)
    output_obj["prompt"] = with_prompt + output_obj["prompt"].replace(" and ", ",")
    output_obj["negative_prompt"] = with_negative_prompt
    output_obj["with_prompt"] = with_prompt
    output_obj["with_negative_prompt"] = with_negative_prompt
    output_obj["query"] = query
    output_obj["style"] = style
    output_obj["negative_style"] = negative_style
    return output_obj
