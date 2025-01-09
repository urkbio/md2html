import markdown
import os
from pathlib import Path
import sys
import argparse
import re

def get_first_h1_title(md_content):
    # 查找第一个一级标题
    h1_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    return h1_match.group(1) if h1_match else 'index page'

def create_html(md_content):
    # 获取一级标题作为页面标题
    page_title = get_first_h1_title(md_content)
    
    # HTML 模板
    html_template = '''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --text-color: #2c3e50;
            --bg-color: #ffffff;
            --code-bg: #f8f9fa;
            --border-color: #eaecef;
            --link-color: #3b82f6;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.7;
            color: var(--text-color);
            background-color: var(--bg-color);
            margin: 0;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 768px;
            margin: 0 auto;
            padding: 2rem;
            background: var(--bg-color);
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 2em;
            margin-bottom: 1em;
            font-weight: 600;
            line-height: 1.25;
        }}
        
        h1 {{ font-size: 2em; border-bottom: 1px solid var(--border-color); padding-bottom: 0.3em; }}
        h2 {{ font-size: 1.5em; border-bottom: 1px solid var(--border-color); padding-bottom: 0.3em; }}
        
        p {{
            margin: 1em 0;
            line-height: 1.7;
        }}
        
        a {{
            color: var(--link-color);
            text-decoration: none;
            transition: color 0.2s ease;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        pre {{
            background-color: var(--code-bg);
            padding: 1em;
            border-radius: 6px;
            overflow-x: auto;
            margin: 1.5em 0;
            border: 1px solid var(--border-color);
        }}
        
        code {{
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.9em;
            padding: 0.2em 0.4em;
            background-color: var(--code-bg);
            border-radius: 3px;
        }}
        
        pre code {{
            padding: 0;
            background-color: transparent;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            margin: 1em 0;
        }}
        
        blockquote {{
            margin: 1em 0;
            padding: 0.5em 1em;
            color: #666;
            border-left: 4px solid var(--link-color);
            background-color: var(--code-bg);
            border-radius: 0 4px 4px 0;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        
        th, td {{
            border: 1px solid var(--border-color);
            padding: 0.6em 1em;
            text-align: left;
        }}
        
        th {{
            background-color: var(--code-bg);
            font-weight: 600;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}
            
            .container {{
                padding: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>'''
    
    # 转换 Markdown 为 HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'tables', 'codehilite']
    )
    
    # 将 HTML 内容和标题插入模板
    return html_template.format(title=page_title, content=html_content)

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='将 Markdown 文件转换为 HTML 静态网页')
    parser.add_argument('input_file', help='输入的 Markdown 文件路径')
    parser.add_argument('-o', '--output', help='输出目录路径，默认为 output', default='output')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 获取输入文件路径
    input_file = Path(args.input_file)
    if not input_file.exists():
        print(f"错误：找不到文件 {input_file}")
        return
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # 读取 Markdown 文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return
    
    # 生成 HTML
    html_content = create_html(md_content)
    
    # 生成输出文件名（保持原文件名，仅改变扩展名）
    output_file = output_dir / input_file.with_suffix('.html').name
    
    # 写入 HTML 文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"成功生成静态网页：{output_file}")
    except Exception as e:
        print(f"写入文件时出错：{e}")

if __name__ == '__main__':
    main() 