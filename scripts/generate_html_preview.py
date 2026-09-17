"""
Converts Markdown to standalone, beautiful HTML with embedded CSS for browser preview.
"""
import markdown

with open("DARUKAA_EARTH_Hackathon_Submission.md", "r", encoding="utf-8") as f:
    md_text = f.read()

html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])

html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DARUKAA.EARTH — Hackathon Submission Document</title>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: #1e293b;
        background-color: #f8fafc;
        margin: 0;
        padding: 40px 20px;
    }}
    .container {{
        max-width: 900px;
        margin: 0 auto;
        background: #ffffff;
        padding: 60px 80px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }}
    h1 {{
        color: #1b4332;
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
        border-bottom: 2px solid #2d6a4f;
        padding-bottom: 12px;
    }}
    h2 {{
        color: #2d6a4f;
        font-size: 1.4rem;
        margin-top: 2rem;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 6px;
    }}
    h3 {{
        color: #40916c;
        font-size: 1.15rem;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 0.95rem;
    }}
    th {{
        background-color: #1b4332;
        color: #ffffff;
        font-weight: 600;
        padding: 12px;
        text-align: left;
    }}
    td {{
        padding: 10px 12px;
        border-bottom: 1px solid #e2e8f0;
    }}
    tr:nth-child(even) {{
        background-color: #f8fafc;
    }}
    pre {{
        background-color: #0f172a;
        color: #38bdf8;
        padding: 16px;
        border-radius: 8px;
        overflow-x: auto;
        font-family: "JetBrains Mono", Consolas, monospace;
        font-size: 0.85rem;
    }}
    code {{
        background-color: #f1f5f9;
        color: #0f172a;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: Consolas, monospace;
    }}
    .callout {{
        background: #e8f5e9;
        border-left: 4px solid #2d6a4f;
        padding: 16px 20px;
        border-radius: 0 8px 8px 0;
        margin: 20px 0;
    }}
    img {{
        max-width: 100%;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
</style>
</head>
<body>
<div class="container">
{html_body}
</div>
</body>
</html>"""

with open("DARUKAA_EARTH_Hackathon_Submission.html", "w", encoding="utf-8") as f:
    f.write(html_doc)

print("Generated DARUKAA_EARTH_Hackathon_Submission.html")
