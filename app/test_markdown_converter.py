# test_markdown_converter.py
from markdown_converter import markdown_to_html

def test_basic_conversion():
    # 测试普通文本转换
    assert markdown_to_html("Hello **World**") == "<p>Hello <strong>World</strong></p>"

def test_heading_conversion():
    # 测试标题转换
    assert markdown_to_html("# Heading 1") == "<h1>Heading 1</h1>"

def test_list_conversion():
    # 测试列表转换
    markdown_text = """
- Item 1
- Item 2
"""
    expected_html = "<ul>\n<li>Item 1</li>\n<li>Item 2</li>\n</ul>"
    assert markdown_to_html(markdown_text).strip() == expected_html
