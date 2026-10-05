"""Build index.html and p/<slug>.html from data/projects.json.
Edit the JSON (add log entries at the top, tick plan items), run `python build.py`, commit, push."""
import json, html, pathlib, re

root = pathlib.Path(__file__).parent
data = json.loads((root / "data/projects.json").read_text(encoding="utf-8"))
E = html.escape
ORDER = {"active": 0, "waiting": 1, "parked": 2, "done": 3}
data.sort(key=lambda p: p["updated"], reverse=True)
data.sort(key=lambda p: (ORDER.get(p["status"], 9), 0 if p.get('priority') == 'high' else 1))

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #4a4a4a 0%, #2a2a2a 100%); min-height: 100vh; padding: 20px; color: #333; }
.container { max-width: 1400px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); overflow: hidden; }
.header { background: linear-gradient(135deg, #3a3a3a 0%, #1a1a1a 100%); color: white; padding: 40px 30px; text-align: center; }
.header h1 { font-size: 2.5em; margin-bottom: 10px; }
.header p { font-size: 1.1em; opacity: 0.95; }
.content { padding: 40px 30px; }
h2 { color: #333; margin: 28px 0 14px; }
.filters { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; }
.filters button { border: 1px solid #ccc; background: #f5f5f5; padding: 6px 16px; border-radius: 20px; cursor: pointer; font-size: .95em; color: #555; }
.filters button.active { background: #333; color: white; border-color: #333; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }
.card { display: flex; flex-direction: column; background: #f9f9f9; border: 1px solid #ddd; border-left: 5px solid #333; border-radius: 8px; padding: 20px; text-decoration: none; color: inherit; transition: box-shadow .2s, transform .2s; }
.card:hover { box-shadow: 0 6px 18px rgba(0,0,0,.15); transform: translateY(-2px); }
.card h3 { color: #222; margin-bottom: 8px; font-size: 1.2em; }
.card p { color: #555; line-height: 1.5; font-size: .95em; flex: 1; }
.meta { display: flex; justify-content: space-between; align-items: center; margin-top: 14px; font-size: .85em; color: #777; }
.tag { display: inline-block; background: #e8e8e8; color: #555; border-radius: 10px; padding: 2px 9px; font-size: .8em; margin: 8px 4px 0 0; }
.status { display: inline-block; border-radius: 10px; padding: 2px 10px; font-size: .8em; font-weight: 600; color: white; }
.s-active { background: #2e7d32; } .s-waiting { background: #b26a00; } .s-parked { background: #777; } .s-done { background: #1565c0; }
.bar { height: 6px; background: #ddd; border-radius: 3px; margin-top: 12px; overflow: hidden; }
.bar > div { height: 100%; background: #333; }
.back { display: inline-block; margin-bottom: 20px; color: #555; text-decoration: none; }
.back:hover { color: #000; }
.plan li, .where li { list-style: none; padding: 6px 0; line-height: 1.5; }
.plan li.done { color: #888; text-decoration: line-through; }
.log { border-left: 3px solid #ddd; padding-left: 18px; }
.log .e { margin-bottom: 14px; line-height: 1.5; }
.log .d { font-weight: 600; color: #333; margin-right: 8px; }
p.about { line-height: 1.6; max-width: 900px; }
pre { background: #f3f3f3; border: 1px solid #ddd; border-radius: 6px; padding: 12px; overflow-x: auto; font-size: .85em; line-height: 1.5; white-space: pre-wrap; }
.sec { margin-top: 8px; }
.sec p { line-height: 1.6; max-width: 1000px; margin: 8px 0; }
.sec ul { margin: 8px 0 8px 22px; line-height: 1.6; max-width: 1000px; }
table.tbl { border-collapse: collapse; margin: 12px 0 18px; font-size: .9em; width: 100%; max-width: 1100px; }
table.tbl th { background: #333; color: white; text-align: left; padding: 7px 10px; }
table.tbl td { padding: 6px 10px; border-bottom: 1px solid #e3e3e3; vertical-align: top; }
table.tbl tr:nth-child(even) td { background: #f7f7f7; }
.note { background: #fff8e1; border-left: 4px solid #e0a800; padding: 10px 14px; margin: 12px 0; max-width: 1000px; line-height: 1.5; }
.toc { display: flex; flex-wrap: wrap; gap: 8px; margin: 14px 0 6px; }
.toc a { font-size: .85em; background: #eee; color: #444; border-radius: 12px; padding: 3px 12px; text-decoration: none; }
.toc a:hover { background: #333; color: white; }
.badge { display: inline-block; border-radius: 10px; padding: 2px 10px; font-size: .8em; font-weight: 600; background: #b71c1c; color: white; margin-left: 6px; }
.foot { text-align: center; color: #999; font-size: .85em; padding: 20px; }
"""


def prog(p):
    return sum(1 for s in p["plan"] if s[0]), len(p["plan"])


def render_sections(secs):
    out = []; toc = []
    for i, sec in enumerate(secs):
        sid = f"s{i}"
        toc.append(f'<a href="#{sid}">{E(sec["heading"])}</a>')
        h = [f'<div class="sec" id="{sid}"><h2>{E(sec["heading"])}</h2>']
        for para in sec.get("text", []):
            h.append(f"<p>{E(para)}</p>")
        if sec.get("bullets"):
            h.append("<ul>" + "".join(f"<li>{E(b)}</li>" for b in sec["bullets"]) + "</ul>")
        if sec.get("table"):
            t = sec["table"]
            h.append('<table class="tbl"><tr>' + "".join(f"<th>{E(c)}</th>" for c in t["head"]) + "</tr>"
                     + "".join("<tr>" + "".join((f'<td style="white-space:nowrap">{E(str(c))}</td>' if re.fullmatch(r"\d{4}-\d{2}-\d{2}|[\d,]+ nt|[\d,]+", str(c)) else f"<td>{E(str(c))}</td>") for c in row) + "</tr>" for row in t["rows"]) + "</table>")
        if sec.get("note"):
            h.append(f'<div class="note">{E(sec["note"])}</div>')
        h.append("</div>")
        out.append("".join(h))
    return '<div class="toc">' + "".join(toc) + "</div>", "".join(out)


def page(title, sub, body, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(title)}</title><style>{CSS}</style></head><body>
<div class="container"><div class="header"><h1>{E(title)}</h1><p>{E(sub)}</p></div>
<div class="content">{body}</div><div class="foot">Maintained with Claude Code from data/projects.json</div></div>{extra}</body></html>"""


cards = []
for p in data:
    d, n = prog(p)
    tags = "".join(f'<span class="tag">{E(t)}</span>' for t in p["tags"])
    cards.append(f'''<a class="card" href="p/{p["slug"]}.html" data-status="{p["status"]}">
<h3>{E(p["title"])}{'<span class="badge">high priority</span>' if p.get('priority') == 'high' else ''}</h3><p>{E(p["summary"])}</p><div>{tags}</div>
<div class="bar"><div style="width:{100 * d // n}%"></div></div>
<div class="meta"><span class="status s-{p["status"]}">{p["status"]}</span><span>{d}/{n} steps · updated {p["updated"]}</span></div></a>''')

statuses = sorted({p["status"] for p in data}, key=lambda s: ORDER.get(s, 9))
filt = ('<div class="filters"><button class="active" data-f="all">All</button>'
        + "".join(f'<button data-f="{s}">{s}</button>' for s in statuses) + "</div>")
js = """<script>
document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{
 document.querySelectorAll('.filters button').forEach(x=>x.classList.toggle('active',x===b));
 document.querySelectorAll('.card').forEach(c=>c.style.display=(b.dataset.f==='all'||c.dataset.status===b.dataset.f)?'':'none');});
</script>"""
(root / "index.html").write_text(
    page("Projects", "What I am working on, where it stands, and what is next",
         filt + '<div class="grid">' + "".join(cards) + "</div>", js), encoding="utf-8")

(root / "p").mkdir(exist_ok=True)
for p in data:
    plan = "".join(f'<li class="{"done" if s[0] else ""}">{"&#9745;" if s[0] else "&#9744;"} {E(s[1])}</li>' for s in p["plan"])
    where = "".join(f"<li>{E(w)}</li>" for w in p["where"])
    log = "".join(f'<div class="e"><span class="d">{E(d)}</span>{E(t)}</div>' for d, t in p["log"])
    cmds = ('<h2>Commands</h2><pre>' + E(chr(10).join(p['commands'])) + '</pre>') if p.get('commands') else ''
    toc, secs = render_sections(p.get('sections', []))
    badge = '<span class="badge">high priority</span>' if p.get('priority') == 'high' else ''
    body = f'''<a class="back" href="../index.html">&larr; All projects</a>
<p><span class="status s-{p["status"]}">{p["status"]}</span>{badge} <span class="meta">updated {p["updated"]}</span></p>{toc}
<h2>About</h2><p class="about">{E(p["about"])}</p>{secs}
<h2>Plan</h2><ul class="plan">{plan}</ul>
<h2>Where things are</h2><ul class="where">{where}</ul>
{cmds}<h2>Log</h2><div class="log">{log}</div>'''
    (root / "p" / f'{p["slug"]}.html').write_text(page(p["title"], p["summary"], body), encoding="utf-8")
print("built", len(data), "projects")
