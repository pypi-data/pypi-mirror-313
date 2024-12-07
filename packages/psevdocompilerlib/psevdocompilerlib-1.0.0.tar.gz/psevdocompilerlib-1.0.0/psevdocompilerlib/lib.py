import requests as r
import urllib.parse as up
prompt = "Я хочу, чтобы вы выступили в роли компилятора псевдокода для преобразования в Python3. Вы получите псевдокод в качестве входных данных и немедленно преобразуете его в чистый, исполняемый код на Python3 без какого-либо дополнительного форматирования или пояснительных комментариев. Когда я предоставлю псевдокод, вы ответите прямой, соответствующей реализацией на Python3, сосредоточив внимание исключительно на трансляции кода. Ваша цель - предоставить точный, функциональный скрипт на Python3, который точно представляет логику исходного псевдокода.Помни - В Python3 пишут по английски!"
import re

def extract_python_code(markdown_text):
    """
    Извлекает код из тега ````python``` в Markdown тексте.

    Аргументы:
        markdown_text (str): Markdown текст, из которого нужно извлечь код.

    Возвращает:
        str: Извлеченный Python код.
    """
    # Используем регулярное выражение для поиска блока кода в теге ````python```
    pattern = r'```python\n(.*?)\n```'
    match = re.search(pattern, markdown_text, re.DOTALL)

    if match:
        # Если блок кода найден, возвращаем его
        return match.group(1).strip()
    else:
        # Если блок кода не найден, возвращаем пустую строку
        return markdown_text

def compile_code(pesvdocode):
    res = r.get(f"https://text.pollinations.ai/{up.quote_plus(pesvdocode)}?system={up.quote_plus(prompt)}").text
    return extract_python_code(res)

__all__ = ["compile_code"]
