from __future__ import annotations
from typing import Optional
from jinja2 import Template
from .models import ScanResult
import json, pathlib

HTML_TMPL = Template('''
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>ReaperScanner AI Report</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 2rem; }
    .card { border: 1px solid #e5e7eb; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }
    .sev-high { border-left: 6px solid #ef4444; }
    .sev-medium { border-left: 6px solid #f59e0b; }
    .sev-low { border-left: 6px solid #10b981; }
    code, pre { background: #f3f4f6; padding: 0.2rem 0.4rem; border-radius: 6px; }
  </style>
</head>
<body>
  <h1>ReaperScanner AI — Report</h1>
  <p><b>Target:</b> {{ r.target }} | <b>Findings:</b> {{ r.stats.findings }} | <b>Exchanges:</b> {{ r.stats.exchanges }}</p>
  {% for f in r.findings %}
    <div class="card sev-{{ 'high' if f.severity=='high' else 'medium' if f.severity=='medium' else 'low' }}">
      <h3>{{ f.type }} ({{ f.severity|upper }}, {{ '%.0f'%(f.confidence*100) }}% confidence)</h3>
      <p><b>URL:</b> {{ f.target }}</p>
      {% if f.evidence.snippet %}
      <details><summary>Evidence snippet</summary><pre>{{ f.evidence.snippet }}</pre></details>
      {% endif %}
      {% if f.education %}
        <h4>Education</h4>
        <p>{{ f.education.summary }}</p>
        <ol>{% for s in f.education.steps %}<li>{{ s }}</li>{% endfor %}</ol>
      {% endif %}
    </div>
  {% endfor %}
</body>
</html>
''')

def write_reports(result: ScanResult, html_path: Optional[str], json_path: Optional[str]):
    if html_path:
        p = pathlib.Path(html_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(HTML_TMPL.render(r=result), encoding="utf-8")
    if json_path:
        p = pathlib.Path(json_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(result.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8")
