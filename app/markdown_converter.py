# markdown_converter.py
import markdown

def markdown_to_html(markdown_text: str) -> str:
    """
    将Markdown文本转换为HTML
    :param markdown_text: 输入的Markdown字符串
    :return: 转换后的HTML字符串
    """
    return markdown.markdown(markdown_text)
