import re
from typing import List


def split_at_unquoted_spaces(line: str):
    result = []
    buffer = []
    symbols = {'"', "'", "(", ")", "[", "]", "{", "}"}
    matching = {")": "(", "]": "[", "}": "{"}
    stack = []
    in_quotes = False
    quote_char = ""

    for char in str(line):
        if char in symbols:
            if in_quotes:
                if char == quote_char:
                    in_quotes = False
            else:
                if char == '"' or char == "'":
                    in_quotes = True
                    quote_char = char
                elif char in matching and stack and stack[-1] == matching[char]:
                    stack.pop()
                else:
                    stack.append(char)
        if char == " " and not stack and not in_quotes:
            result.append("".join(buffer))
            buffer = []
        else:
            buffer.append(char)

    # 如果缓冲区还有字符，则将它们加入到结果列表中。
    if buffer:
        result.append("".join(buffer))

    return result


def unquote_text(s: str):
    """删除字符串前后的成对引号以及多余的空格"""
    pattern = r'^("|\')((?:(?=(\\?))\3.)*?)\1$'
    text = s.strip()
    match = re.match(pattern, text)
    if match:
        text = match.group(2)
    return text.strip()


def quote_text(s: str, quote='"'):
    """阔起字符串，默认使用引号。如果给定的quote包含多个字符，则会使用前两个分别阔起，例如使用括号"""
    left = quote[0]
    right = quote[1] if len(quote) > 1 else left
    return left + str(s) + right


def is_quoted(s: str, quotes="\"'"):
    """判断字符串是否包含引号"""
    s = s.strip()
    for q in quotes:
        if s.startswith(q) and s.endswith(q):
            return True
    return False


def contains_invisible_char(s: str):
    regex = re.compile(r"\s")
    return regex.search(s)


def extract_numbers(input_string) -> List[float]:
    if not input_string:
        return []
    # 使用正则表达式匹配字符串中的所有数字，包括小数
    numbers = re.findall(r"-?\d+\.?\d*", input_string)
    # 将匹配到的数字从字符串转换为浮点数或整数
    numbers = [float(num) if "." in num else int(num) for num in numbers]
    return numbers
