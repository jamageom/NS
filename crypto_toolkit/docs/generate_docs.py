"""
Generate documentation artifacts for the Classical Cryptography Toolkit.
This script:
  1. Produces an HTML version of the mini-project report (printable as PDF via browser).
  2. Generates a system-flow PNG using turtle (stdlib) or ASCII art to a text file.

Run from crypto_toolkit/:
    python docs/generate_docs.py
"""

import os
import sys
import time

REPORT_MD = os.path.join(os.path.dirname(__file__), "mini_project_report.md")
OUT_HTML  = os.path.join(os.path.dirname(__file__), "mini_project_report.html")
OUT_FLOW  = os.path.join(os.path.dirname(__file__), "system_flowchart.txt")


# ──────────────────────────────────────────────────────────────────
# 1. Markdown → HTML conversion (no third-party needed)
# ──────────────────────────────────────────────────────────────────

def _md_to_html_simple(md: str) -> str:
    """Very simple Markdown→HTML converter for headings, tables, bold, code."""
    import re
    lines = md.split('\n')
    html_lines = []
    in_table = False
    in_code  = False
    code_buf = []

    for i, line in enumerate(lines):
        # Fenced code blocks
        if line.strip().startswith('```'):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                html_lines.append('<pre><code>' + '\n'.join(code_buf) + '</code></pre>')
            continue
        if in_code:
            code_buf.append(line)
            continue

        # Headings
        m = re.match(r'^(#{1,4})\s+(.*)', line)
        if m:
            lvl = len(m.group(1))
            html_lines.append(f'<h{lvl}>{m.group(2)}</h{lvl}>')
            continue

        # Horizontal rule
        if re.match(r'^---+$', line.strip()):
            html_lines.append('<hr>')
            continue

        # Tables
        if '|' in line:
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if re.match(r'^[\s|:-]+$', line):   # separator row
                continue
            row = ''.join(f'<td><b>{c}</b></td>' if i == 0 else f'<td>{c}</td>'
                          for c in cells)
            if not in_table:
                html_lines.append('<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;">')
                in_table = True
            html_lines.append(f'<tr>{row}</tr>')
            # peek next line
            if i + 1 >= len(lines) or '|' not in lines[i + 1]:
                html_lines.append('</table>')
                in_table = False
            continue
        else:
            if in_table:
                html_lines.append('</table>')
                in_table = False

        # Bold, inline code
        line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
        line = re.sub(r'`(.+?)`', r'<code>\1</code>', line)
        # Bullet lists
        if re.match(r'^\s*[-*]\s', line):
            line = '<li>' + re.sub(r'^\s*[-*]\s', '', line) + '</li>'
        elif line.strip():
            line = '<p>' + line + '</p>'
        else:
            line = '<br>'

        html_lines.append(line)

    return '\n'.join(html_lines)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Mini Project Report – Classical Cryptography Toolkit</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 900px;
          margin: 40px auto; padding: 20px; color: #222; line-height: 1.6; }}
  h1 {{ color: #003366; border-bottom: 3px solid #003366; padding-bottom: 8px; }}
  h2 {{ color: #003366; border-bottom: 1px solid #aaa; }}
  h3 {{ color: #004488; }}
  h4 {{ color: #333; }}
  table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
  th, td {{ border: 1px solid #aaa; padding: 8px 12px; text-align: left; }}
  th {{ background: #003366; color: white; }}
  tr:nth-child(even) {{ background: #f2f6ff; }}
  pre {{ background: #1e1e2e; color: #cdd6f4; padding: 16px;
         border-radius: 6px; overflow-x: auto; font-size: 13px; }}
  code {{ background: #eef; padding: 2px 4px; border-radius: 3px; font-size: 13px; }}
  pre code {{ background: transparent; color: inherit; padding: 0; }}
  hr {{ border: none; border-top: 1px solid #ccc; margin: 24px 0; }}
  li {{ margin: 4px 0; }}
  .title-block {{ background: #003366; color: white; padding: 30px;
                  border-radius: 8px; margin-bottom: 30px; text-align: center; }}
  .title-block h1 {{ color: white; border: none; }}
  .title-block p {{ color: #cdd6f4; margin: 4px 0; }}
</style>
</head>
<body>
<div class="title-block">
  <h1>Classical Cryptography Toolkit</h1>
  <p>Mini Project Report &nbsp;|&nbsp; Network Security</p>
  <p>Final Year ECM 2026-27</p>
</div>
{body}
<hr>
<p style="text-align:center;color:#666;font-size:12px;">
  Generated on {date} &nbsp;|&nbsp; Classical Cryptography Toolkit
</p>
</body>
</html>
"""


def generate_html_report() -> None:
    with open(REPORT_MD, 'r', encoding='utf-8') as f:
        md = f.read()
    body = _md_to_html_simple(md)
    html = HTML_TEMPLATE.format(body=body, date=time.strftime('%Y-%m-%d %H:%M'))
    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  [OK] HTML report written to: {OUT_HTML}")
    print(f"    Open in a browser and use Ctrl+P -> Save as PDF")


# ──────────────────────────────────────────────────────────────────
# 2. ASCII Flowchart to Text File
# ──────────────────────────────────────────────────────────────────

FLOWCHART = r"""
╔══════════════════════════════════════════════════════════════════╗
║          CLASSICAL CRYPTOGRAPHY TOOLKIT — SYSTEM FLOWCHART       ║
╚══════════════════════════════════════════════════════════════════╝

  ┌────────────────────┐
  │       START        │
  └─────────┬──────────┘
            │
            ▼
  ┌────────────────────────────────────┐
  │   Display Password Prompt          │
  │   (up to 3 attempts)               │
  └─────────┬──────────────────────────┘
            │
            ▼
  ┌────────────────────────┐     Wrong ×3
  │  Valid Password?        ├─────────────► EXIT
  └─────────┬──────────────┘
            │ Yes
            ▼
  ┌────────────────────────────────────┐
  │          Display Main Menu         │
  └─────────┬──────────────────────────┘
            │
            ▼
  ┌────────────────────────────────────┐
  │     Read User Choice [1-13]        │
  └─────────┬──────────────────────────┘
            │
     ┌──────┴────────────────────────────────────────────┐
     │                                                    │
  Choice 1-8                                       Choice 9-13
  (Cipher ops)                                     (Utilities)
     │                                                    │
     ▼                                                    ▼
  ┌──────────────────┐    ┌────────────────────────────────────┐
  │ Accept Plaintext │    │  9: Compare All   10: Encrypt File │
  │ + Key            │    │ 11: Decrypt File  12: Help          │
  └────────┬─────────┘    │ 13: Exit          ← loop ends      │
           │              └────────────────────────────────────┘
           ▼
  ┌──────────────────────────┐
  │  Validate Input & Key    │
  └────────┬─────────────────┘
           │        ▼ Error
           │    ┌───────────────────┐
           │    │ Display Error Msg │
           │    └─────────┬─────────┘
           │              │ Return to menu
           ▼
  ┌──────────────────────────┐
  │  Encrypt / Decrypt       │
  │  (measure perf_counter)  │
  └────────┬─────────────────┘
           │
           ▼
  ┌──────────────────────────┐
  │  Display Result + Time   │
  └────────┬─────────────────┘
           │
           ▼
  ┌────────────────────────────────────┐
  │    Return to Main Menu             │
  └────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════╗
║       ENCRYPTION / DECRYPTION FLOW (Per Cipher)                  ║
╚══════════════════════════════════════════════════════════════════╝

  Input: Plaintext / Ciphertext + Key
         │
         ▼
  ┌──────────────────────────┐
  │  Validate Key Format     │──── Error ──► ValueError raised
  └────────┬─────────────────┘              (caught in handler)
           │
           ▼
  ┌──────────────────────────┐
  │  Prepare Text            │ (uppercase, strip spaces for some,
  │  (cipher-specific)       │  I/J merge for Playfair, pad for Hill)
  └────────┬─────────────────┘
           │
           ▼
  ┌──────────────────────────┐
  │  Apply Cipher Algorithm  │
  │  Caesar: C = (P+k) mod26 │
  │  Hill:   C = K×P mod 26  │
  │  etc.                    │
  └────────┬─────────────────┘
           │
           ▼
  ┌──────────────────────────┐
  │  Return Result String    │
  └────────┬─────────────────┘
           │
           ▼
       Output + Time Displayed
"""


def generate_flowchart() -> None:
    with open(OUT_FLOW, 'w', encoding='utf-8') as f:
        f.write(FLOWCHART)
    print(f"  [OK] Flowchart written to: {OUT_FLOW}")


# ──────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("\n  Generating documentation...\n")
    generate_html_report()
    generate_flowchart()
    print("\n  Done! Deliverables:")
    print(f"    - HTML Report : docs/mini_project_report.html")
    print(f"    - Flowchart   : docs/system_flowchart.txt")
    print()
    print("  To create PDF: Open mini_project_report.html in browser -> Ctrl+P -> Save as PDF")
