"""
创建HTML版本的Markdown文档
"""
import re

def create_html():
    with open('1.6_学习要点详解.md', 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 简单的Markdown转HTML
    html = md_content
    
    # 标题
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # 代码块
    html = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    # 行内代码
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # 粗体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # 分隔线
    html = html.replace('---', '<hr>')
    
    # 列表处理
    lines = html.split('\n')
    result = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{stripped[2:]}</li>')
        elif stripped.startswith(('|', '<', '```')):
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
        elif stripped == '':
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append('<br>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            if stripped and not stripped.startswith('<'):
                result.append(f'<p>{line}</p>')
            else:
                result.append(line)
    
    if in_list:
        result.append('</ul>')
    
    html_content = '\n'.join(result)
    
    # HTML模板
    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>1.6章学习要点详解</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
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
        p { margin: 15px 0; text-align: justify; }
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
        tr:nth-child(even) { background: #f8f9fa; }
        tr:hover { background: #e3f2fd; }
        ul, ol { padding-left: 30px; margin: 15px 0; }
        li { margin: 10px 0; }
        strong { color: #2c3e50; font-weight: 600; }
        hr {
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        CONTENT_PLACEHOLDER
    </div>
</body>
</html>'''
    
    final_html = html_template.replace('CONTENT_PLACEHOLDER', html_content)
    
    with open('1.6_学习要点详解.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("Success! HTML file created.")
    print("Open the HTML file in your browser to view!")

if __name__ == "__main__":
    create_html()
