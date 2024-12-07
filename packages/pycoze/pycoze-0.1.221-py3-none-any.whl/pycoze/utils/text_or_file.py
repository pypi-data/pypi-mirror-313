import os
import chardet


def to_text(text_or_file: str):
    if os.path.exists(text_or_file) and os.path.isfile(text_or_file):
        # 自动检测文件编码
        with open(text_or_file, "rb") as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]

        # 读取文件内容
        with open(text_or_file, "r", encoding=encoding) as f:
            input_text = f.read()
    else:
        input_text = text_or_file  # 直接使用传入的文本
    return input_text
