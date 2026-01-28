"""
将Markdown文件转换为美观的HTML文件
"""
import re

def markdown_to_html(md_file, html_file):
    """将Markdown转换为HTML"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # HTML模板
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>学习要点详解</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 30px 20px;
            line-height: 1.8;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #333;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 4px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
            font-size: 2.2em;
        }
        h2 {
            color: #34495e;
            margin-top: 40px;
            margin-bottom: 20px;
            border-left: 5px solid #3498db;
            padding-left: 15px;
            font-size: 1.6em;
        }
        h3 {
            color: #555;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        p {
            margin: 15px 0;
            text-align: justify;
        }
        code {
            background: #f4f4f4;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: "Consolas", "Monaco", monospace;
            font-size: 0.9em;
            color: #e74c3c;
        }
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            font-family: "Consolas", "Monaco", monospace;
            line-height: 1.5;
        }
        pre code {
            background: transparent;
            color: inherit;
            padding: 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: left;
        }
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background: #f8f9fa;
        }
        tr:hover {
            background: #e3f2fd;
        }
        ul, ol {
            padding-left: 30px;
            margin: 15px 0;
        }
        li {
            margin: 10px 0;
        }
        strong {
            color: #2c3e50;
            font-weight: 600;
        }
        hr {
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 15px 20px;
            background: #f8f9fa;
            color: #555;
            border-radius: 4px;
        }
        .emoji {
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>"""
    
    # 简单的Markdown到HTML转换
    html_content = content
    
    # 标题转换
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    
    # 代码块
    html_content = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', html_content, flags=re.DOTALL)
    
    # 行内代码
    html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)
    
    # 粗体
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    
    # 列表
    lines = html_content.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            result_lines.append(f'<li>{line.strip()[2:]}</li>')
        elif line.strip().startswith(('|', '```', '<')):
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)
        elif line.strip() == '':
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append('<p></p>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            if line.strip() and not line.strip().startswith('<'):
                result_lines.append(f'<p>{line}</p>')
            else:
                result_lines.append(line)
    
    if in_list:
        result_lines.append('</ul>')
    
    html_content = '\n'.join(result_lines)
    
    # 分隔线
    html_content = html_content.replace('---', '<hr>')
    
    # 表格处理（简单版本）
    html_content = re.sub(r'\|(.+)\|', lambda m: '<tr>' + ''.join(f'<td>{cell.strip()}</td>' for cell in m.group(1).split('|') if cell.strip()) + '</tr>', html_content)
    
    # 写入HTML文件
    final_html = html_template.replace('{content}', html_content)
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    try:
        print(f"Successfully generated HTML file: {html_file}")
    except:
        pass  # Suppress print errors

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        md_file = sys.argv[1]
        html_file = sys.argv[2] if len(sys.argv) > 2 else md_file.replace('.md', '.html')
        markdown_to_html(md_file, html_file)
    else:
        # Default: convert 1.7
        markdown_to_html("1.7_学习要点详解.md", "1.7_学习要点详解.html")
