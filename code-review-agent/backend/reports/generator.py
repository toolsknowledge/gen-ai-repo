"""Report Generator — converts CodeReviewResult dict into a styled HTML report."""

from pathlib import Path
from jinja2 import Environment, BaseLoader

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Code Review — {{ result.file_name }}</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f1f5f9;color:#1e293b;line-height:1.6}
  .wrap{max-width:960px;margin:40px auto;padding:0 20px 60px}
  header{background:linear-gradient(135deg,#1e293b,#0f172a);color:white;padding:32px;border-radius:12px;margin-bottom:20px}
  header h1{font-size:22px;font-weight:700;margin-bottom:4px}
  header .meta{color:#94a3b8;font-size:14px}
  .score-row{background:white;border-radius:12px;padding:28px 32px;margin-bottom:20px;display:flex;align-items:center;gap:28px;box-shadow:0 2px 8px rgba(0,0,0,.07)}
  .score-num{font-size:72px;font-weight:900;line-height:1;color:{{ score_color }}}
  .summary{color:#475569;font-size:15px;margin-top:8px;line-height:1.7}
  .stats{display:flex;gap:14px;margin-bottom:20px;flex-wrap:wrap}
  .stat{background:white;border-radius:10px;padding:16px 20px;flex:1;min-width:100px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.06)}
  .stat .n{font-size:30px;font-weight:800}
  .stat .l{font-size:11px;color:#94a3b8;text-transform:uppercase;letter-spacing:.05em}
  .p1c{color:#ef4444}.p2c{color:#f97316}.p3c{color:#ca8a04}.p4c{color:#3b82f6}.p5c{color:#6b7280}
  h2{font-size:16px;font-weight:700;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
  .issue{background:white;border-radius:10px;padding:20px 24px;margin-bottom:12px;border-left:5px solid #e2e8f0;box-shadow:0 1px 4px rgba(0,0,0,.05)}
  .issue.P1{border-color:#ef4444}.issue.P2{border-color:#f97316}.issue.P3{border-color:#ca8a04}.issue.P4{border-color:#3b82f6}.issue.P5{border-color:#6b7280}
  .badges{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}
  .badge{display:inline-block;padding:3px 10px;border-radius:5px;font-size:12px;font-weight:700;color:white}
  .bP1{background:#ef4444}.bP2{background:#f97316}.bP3{background:#ca8a04}.bP4{background:#3b82f6}.bP5{background:#6b7280}
  .bcat{background:#f1f5f9;color:#475569;font-weight:400}
  .bcwe{background:#fef3c7;color:#92400e;font-weight:600}
  .bline{background:#ede9fe;color:#5b21b6}
  .ititle{font-size:15px;font-weight:600;color:#1e293b;margin-bottom:6px}
  .idesc{color:#475569;font-size:14px;margin-bottom:10px}
  pre{background:#1e293b;color:#e2e8f0;padding:14px 16px;border-radius:7px;font-size:13px;overflow-x:auto;margin:10px 0;font-family:"Fira Code",monospace}
  .fix{background:#f0fdf4;border:1px solid #86efac;border-radius:7px;padding:12px 16px;margin-top:10px}
  .fix strong{color:#15803d;font-size:13px;display:block;margin-bottom:6px}
  .fix code{color:#166534;font-size:13px;white-space:pre-wrap;font-family:monospace}
  footer{text-align:center;color:#94a3b8;font-size:12px;margin-top:40px}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Code Review Report</h1>
    <div class="meta">
      File: <strong style="color:white">{{ result.file_name }}</strong> &nbsp;·&nbsp;
      Language: {{ result.language }} &nbsp;·&nbsp;
      {{ result.total_lines }} lines &nbsp;·&nbsp;
      ID: {{ review_id }}
    </div>
  </header>

  <div class="score-row">
    <div>
      <div class="score-num">{{ result.overall_score }}</div>
      <div style="color:#94a3b8;font-size:13px">/ 100</div>
    </div>
    <div>
      <div style="font-weight:700;font-size:17px;margin-bottom:6px">Overall Score</div>
      <div class="summary">{{ result.review_summary }}</div>
    </div>
  </div>

  {% set p1 = result.issues | selectattr('priority','equalto','P1') | list | length %}
  {% set p2 = result.issues | selectattr('priority','equalto','P2') | list | length %}
  {% set p3 = result.issues | selectattr('priority','equalto','P3') | list | length %}
  {% set p4 = result.issues | selectattr('priority','equalto','P4') | list | length %}
  {% set p5 = result.issues | selectattr('priority','equalto','P5') | list | length %}
  <div class="stats">
    <div class="stat"><div class="n p1c">{{ p1 }}</div><div class="l">P1 Critical</div></div>
    <div class="stat"><div class="n p2c">{{ p2 }}</div><div class="l">P2 High</div></div>
    <div class="stat"><div class="n p3c">{{ p3 }}</div><div class="l">P3 Medium</div></div>
    <div class="stat"><div class="n p4c">{{ p4 }}</div><div class="l">P4 Low</div></div>
    <div class="stat"><div class="n p5c">{{ p5 }}</div><div class="l">P5 Info</div></div>
    <div class="stat"><div class="n" style="color:#6366f1">{{ result.issues | length }}</div><div class="l">Total</div></div>
  </div>

  <h2>Issues Found ({{ result.issues | length }})</h2>
  {% for issue in result.issues %}
  <div class="issue {{ issue.priority }}">
    <div class="badges">
      <span class="badge b{{ issue.priority }}">{{ issue.priority }}</span>
      <span class="badge bcat">{{ issue.category }}</span>
      {% if issue.cwe_reference %}<span class="badge bcwe">{{ issue.cwe_reference }}</span>{% endif %}
      {% if issue.line_number %}<span class="badge bline">Line {{ issue.line_number }}</span>{% endif %}
    </div>
    <div class="ititle">{{ issue.title }}</div>
    <div class="idesc">{{ issue.description }}</div>
    {% if issue.code_snippet %}<pre>{{ issue.code_snippet }}</pre>{% endif %}
    {% if issue.suggested_fix %}
    <div class="fix">
      <strong>✅ Suggested Fix</strong>
      <code>{{ issue.suggested_fix }}</code>
    </div>
    {% endif %}
  </div>
  {% endfor %}

  <footer>Generated by Code Review Agent &nbsp;·&nbsp; {{ review_id }}</footer>
</div>
</body>
</html>"""


class ReportGenerator:
    def __init__(self):
        self.env = Environment(loader=BaseLoader())

    def generate_html(self, result: dict, review_id: str, output_dir: Path) -> Path:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        score = result.get("overall_score", 0)
        color = "#ef4444" if score < 40 else "#f97316" if score < 70 else "#22c55e"
        html = self.env.from_string(HTML_TEMPLATE).render(
            result=result, review_id=review_id, score_color=color
        )
        out = output_dir / f"{review_id}.html"
        out.write_text(html, encoding="utf-8")
        return out