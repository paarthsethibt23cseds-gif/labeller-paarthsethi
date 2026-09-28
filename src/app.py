"""Flask UI: summary table of ActivityNet videos with search and filters."""
import math
import os
from collections import Counter

from flask import Flask, jsonify, render_template_string, request, url_for

from dataset import find_dataset, load_records
from search import filter_records

PAGE_SIZE = 50
app = Flask(__name__)
RECORDS = load_records()
SUBSETS = sorted({r["subset"] for r in RECORDS})
CATEGORIES = sorted({c for r in RECORDS for c in r["categories"]})
N_LABELS = len({l for r in RECORDS for l in r["labels"]})
SUBSET_COUNTS = Counter(r["subset"] for r in RECORDS)
N_UNLABELED = sum(1 for r in RECORDS if not r["labels"])

PAGE = """<!doctype html><meta charset="utf-8"><title>ActivityNet label explorer</title>
<style>
body{font-family:system-ui,sans-serif;margin:24px;color:#222}
form{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
input,select,button{padding:6px 8px;font-size:14px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{border-bottom:1px solid #ddd;padding:6px 8px;text-align:left;vertical-align:top}
th{background:#f5f5f5}.muted{color:#777}.pager{margin:12px 0}
</style>
<h2>ActivityNet v1.3 label explorer</h2>
<p class="muted">{{ total }} videos loaded from {{ src }} &middot; {{ n_labels }} distinct labels &middot;
{{ n_unlabeled }} without labels &middot; {% for k, v in subset_counts.items() %}{{ k }}: {{ v }}{% if not loop.last %}, {% endif %}{% endfor %}</p>
<form method="get">
 <input name="q" placeholder="label keyword, e.g. surf" value="{{ a.get('q','') }}">
 <select name="subset"><option value="">any subset</option>
  {% for s in subsets %}<option {{ 'selected' if a.get('subset')==s }}>{{ s }}</option>{% endfor %}</select>
 <select name="category"><option value="">any category</option>
  {% for c in categories %}<option {{ 'selected' if a.get('category')==c }}>{{ c }}</option>{% endfor %}</select>
 <input name="min_duration" type="number" step="any" placeholder="min sec" style="width:90px" value="{{ a.get('min_duration','') }}">
 <input name="max_duration" type="number" step="any" placeholder="max sec" style="width:90px" value="{{ a.get('max_duration','') }}">
 <button>Filter</button> <a href="{{ url_for('index') }}">reset</a>
</form>
<p><b>{{ n }}</b> matching videos &middot; page {{ page }} of {{ pages }}</p>
<table><tr><th>Video</th><th>Labeled segments</th><th>Category</th><th>Subset</th><th>Duration (s)</th><th>Resolution</th></tr>
{% for r in rows %}<tr>
 <td><a href="{{ r.url }}" target="_blank">{{ r.id }}</a></td>
 <td>{% for s in r.segments %}{{ s.label }} <span class="muted">[{{ s.start }}&ndash;{{ s.end }}s]</span>{% if not loop.last %}<br>{% endif %}{% else %}<span class="muted">no labels</span>{% endfor %}</td>
 <td>{{ r.categories|join(', ') }}</td><td>{{ r.subset }}</td><td>{{ r.duration }}</td><td>{{ r.resolution }}</td>
</tr>{% else %}<tr><td colspan="6">No videos match these filters.</td></tr>{% endfor %}</table>
<div class="pager">{% if page > 1 %}<a href="{{ prev_url }}">&laquo; prev</a>{% endif %}
 {% if page < pages %} &nbsp; <a href="{{ next_url }}">next &raquo;</a>{% endif %}</div>"""


def _num(v):
    try:
        return float(v) if v not in (None, "") else None
    except ValueError:
        return None


def matching():
    a = request.args
    return filter_records(RECORDS, q=a.get("q", ""), subset=a.get("subset", ""),
                          category=a.get("category", ""),
                          min_duration=_num(a.get("min_duration")),
                          max_duration=_num(a.get("max_duration")))


@app.route("/")
def index():
    found = matching()
    pages = max(1, math.ceil(len(found) / PAGE_SIZE))
    page = min(max(1, request.args.get("page", 1, type=int)), pages)
    rows = found[(page - 1) * PAGE_SIZE: page * PAGE_SIZE]
    args = request.args.to_dict()
    args.pop("page", None)
    return render_template_string(
        PAGE, rows=rows, n=len(found), page=page, pages=pages, a=request.args,
        total=len(RECORDS), src=find_dataset().name, n_labels=N_LABELS,
        n_unlabeled=N_UNLABELED, subset_counts=SUBSET_COUNTS,
        subsets=SUBSETS, categories=CATEGORIES,
        prev_url=url_for("index", page=page - 1, **args),
        next_url=url_for("index", page=page + 1, **args))


@app.route("/api/videos")
def api_videos():
    limit = request.args.get("limit", 100, type=int)
    found = matching()
    return jsonify({"count": len(found), "results": found[:limit]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
