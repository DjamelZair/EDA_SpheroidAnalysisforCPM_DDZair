"""
report_utils.py - render the curated analysis into the author's portfolio design language.

The HTML emits the SAME component classes as the portfolio pages (hero card with gold ring,
kpi-strip, sec-h, card + verdict, stack-row, big-cta) against the extracted stylesheets
(style.css for theme pages, landing.css for the index). Personal/portfolio chrome (profile
photo, bio, contact, hire, other projects) is stripped; author attribution is kept.

This module renders only. It runs no analysis and restyles no figure: each figure is the
already-generated PNG, shown as-is. Content is supplied as block dicts (see build_site.py),
which keeps the rich layout under control and lets us emit a matching markdown reader too.
"""
from __future__ import annotations
import html as _html
import re
from pathlib import Path

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Anton&'
    'family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&'
    'family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500;600&'
    'display=swap" rel="stylesheet">'
)

# ---- tiny inline markdown (bold / italic / code / links) for prose strings -------------
def inline(t: str) -> str:
    # escape < and > but preserve &entity; (we control the content, and titles use
    # named entities like &ge; &rarr; &middot; that must render, not be double-escaped)
    t = t.replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    return t

def paras(text: str) -> str:
    return "".join(f"<p>{inline(p.strip())}</p>" for p in text.strip().split("\n\n") if p.strip())


# ---- header / shell (personal chrome stripped) ----------------------------------------
def _header(rel_root: str, active: str | None) -> str:
    def nav(href, label, key):
        cls = ' class="active"' if key == active else ""
        return f'<a href="{rel_root}{href}"{cls}>{label}</a>'
    return f"""<header>
  <a class="brand-block" href="{rel_root}index.html">
    <span class="brand-name">CLL <span class="dot">&rarr;</span> CPM<span class="role">Analysis appendix &middot; MSc thesis</span></span>
  </a>
  <nav class="top">
    {nav('index.html','Themes', 'index')}
    {nav('THESIS_CITE_MAP.md','Cite map', 'cite')}
    <a href="https://github.com/DjamelZair" target="_blank" rel="noopener">GitHub</a>
  </nav>
</header>"""

def _page(title, body, rel_root, css):
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{_html.escape(title)}</title>{FONTS}'
            f'<link rel="stylesheet" href="{rel_root}{css}"></head><body>{body}</body></html>')


# ---- block renderers (theme page) ------------------------------------------------------
def _hero(b, rel_root, prev_next):
    meta = '<span class="dot">&middot;</span>'.join(f"<span>{inline(m)}</span>" for m in b["meta"])
    summary = f'<p class="summary">{inline(b["summary"])}</p>' if b.get("summary") else ""
    back = (f'<a class="back" href="{rel_root}index.html">&larr; All analysis themes</a>')
    tabs = ""
    if prev_next:
        items = "".join(
            f'<a href="{rel_root}{d["href"]}" class="{"active" if d.get("active") else ""}">'
            f'{d["tag"]}<span class="label">{d["name"]}</span></a>' for d in prev_next)
        tabs = f'<nav class="rq-tabs">{items}</nav>'
    bg = b.get("bg", "assets/hero_spheroid_healthy.png")
    cap = f'<div class="cap">{inline(b["caption"])}</div>' if b.get("caption") else ""
    return (f'{back}{tabs}<section class="bhero">'
            f'<div class="bg" style="background-image:url(\'{rel_root}{bg}\')"></div>'
            f'<div class="radial"></div><div class="scrim"></div>'
            f'<div class="inner"><div class="meta">{meta}</div>'
            f'<h1 class="display">{b["title"]}</h1>'
            f'<p class="lede">{inline(b["lede"])}</p>{summary}</div>{cap}</section>')

def _kpis(b):
    cells = []
    for k in b["items"]:
        gold = " gold" if k.get("gold") else ""
        numcls = " numeric" if k.get("numeric") else ""
        cells.append(f'<div class="kpi{gold}"><div class="lbl">{inline(k["lbl"])}</div>'
                     f'<div class="num{numcls}">{inline(k["num"])}</div>'
                     f'<div class="desc">{inline(k["desc"])}</div></div>')
    return f'<section class="kpi-strip">{"".join(cells)}</section>'

def _section(b):
    right = f'<span class="right">{inline(b["right"])}</span>' if b.get("right") else ""
    return f'<div class="sec-h"><h2 class="display">{b["title"]}</h2>{right}</div>'

def _figure(b, rel_root):
    """Full-width figure card: image edge-to-edge + 'what it shows' + 'informs' verdict."""
    sub = f'<span class="sub">{inline(b["sub"])}</span>' if b.get("sub") else ""
    ttl = f'<span class="ttl">{b["ttl"]}</span>' if b.get("ttl") else ""
    head = f'<div class="card-h">{ttl}{sub}</div>' if (ttl or sub) else ""
    shows = f'<p>{inline(b["shows"])}</p>' if b.get("shows") else ""
    informs = ""
    if b.get("informs"):
        tag = b.get("informs_tag", "Informs the method")
        informs = (f'<div class="verdict">{inline(b["informs"])}'
                   f'<span class="small">{inline(tag)}</span></div>')
    imgs = b["img"] if isinstance(b["img"], list) else [b["img"]]
    # figures are theme-local (figures/x.png), so they are NOT prefixed with rel_root
    img_html = "".join(f'<img src="{src}" alt="{_html.escape(b.get("alt",""))}">'
                       for src in imgs)
    # native = transparent figure built for the teal card (no blend). light = white-bg
    # matplotlib figure multiply-blended so its white tints into the teal.
    if b.get("native"):
        wrap_cls = "figwrap native"
    elif b.get("light"):
        wrap_cls = "figwrap light"
    else:
        wrap_cls = "figwrap"
    return (f'<section class="card" style="padding:0;overflow:hidden">'
            f'<div class="{wrap_cls}">{img_html}</div>'
            f'<div style="padding:1.2rem 1.7rem 1.5rem">{head}{shows}{informs}</div></section>')

def _prose(b):
    inner = paras(b["text"])
    if b.get("title"):
        inner = f'<div class="card-h"><span class="ttl">{b["title"]}</span></div>' + inner
    return f'<section class="card">{inner}</section>'

def _table(b):
    head = "".join(f"<th>{inline(c)}</th>" for c in b["head"])
    rows = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in b["rows"])
    cap = f'<div class="card-h"><span class="ttl">{b["title"]}</span></div>' if b.get("title") else ""
    return (f'<section class="card">{cap}<table style="width:100%;border-collapse:collapse">'
            f'<thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></section>')

def _tools(b):
    chips = "".join(f'<span class="chip{" gold" if c.get("gold") else ""}">{inline(c["t"])}</span>'
                    for c in b["chips"])
    return (f'<section class="stack-row"><div class="lbl">{b["label"]}</div>'
            f'<div class="stack-chips">{chips}</div></section>')

def _bigcta(b, rel_root):
    links = "".join(f'<a class="cta{" primary" if l.get("primary") else ""}" '
                    f'href="{rel_root}{l["href"]}">{inline(l["t"])}</a>' for l in b["links"])
    return (f'<section class="big-cta"><h3>{b["title"]}</h3>'
            f'<div class="links">{links}</div></section>')

import json as _json

CHART_CDN = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>'

# Themed Chart.js runtime (your portfolio palette + mono fonts). Data is inlined per chart.
CHART_RUNTIME = """<script>
const C={TEAL_1:'#052e36',TEAL_3:'#0d5963',GOLD:'#c8a05c',GOLD_2:'#a37432',GOLD_3:'#e7c98a',
  PAPER:'#f3ecd6',MUTED:'rgba(168,181,184,0.65)',CLAY:'#c44a30',ICE:'#7CFEF0',GREEN:'#6dd9a1'};
const GRID='rgba(199,160,92,0.12)', MF={family:'JetBrains Mono',size:10};
function ax(label,opts){return Object.assign({ticks:{color:C.PAPER,font:MF},grid:{color:GRID},
  border:{display:false},title:label?{display:true,text:label,color:C.GOLD_3,font:{family:'JetBrains Mono',size:11}}:{display:false}},opts||{});}
function tip(){return {backgroundColor:C.TEAL_1,titleColor:C.PAPER,bodyColor:C.PAPER,borderColor:C.GOLD,borderWidth:1,padding:9,cornerRadius:2,displayColors:false};}
function leg(show){return {display:show,position:'top',align:'end',labels:{color:C.PAPER,font:{family:'JetBrains Mono',size:10,weight:'500'},boxWidth:14,boxHeight:14}};}
function base(showLeg){return {responsive:true,maintainAspectRatio:false,animation:{duration:850,easing:'easeOutCubic'},
  plugins:{legend:leg(showLeg),tooltip:tip()}};}

function barH(id,d){const el=document.getElementById(id);if(!el)return;
  const o=base(d.datasets.length>1);o.indexAxis='y';
  o.scales={x:ax(d.xlabel,{min:d.min||0,max:d.max,ticks:{color:C.PAPER,font:MF,callback:v=>(+v).toLocaleString(undefined,{maximumFractionDigits:d.dec??2})}}),y:ax()};
  if(d.logx){o.scales.x.type='logarithmic';delete o.scales.x.min;delete o.scales.x.max;}
  new Chart(el,{type:'bar',data:{labels:d.labels,datasets:d.datasets.map(s=>({label:s.label,data:s.data,backgroundColor:s.color,borderColor:C.TEAL_1,borderWidth:1.2}))},options:o});}

function barV(id,d){const el=document.getElementById(id);if(!el)return;
  const o=base(d.datasets.length>1);
  o.scales={x:ax(d.xlabel),y:ax(d.ylabel,{min:d.min||0,max:d.max,ticks:{color:C.PAPER,font:MF,callback:v=>(+v).toFixed(d.dec??2)}})};
  new Chart(el,{type:'bar',data:{labels:d.labels,datasets:d.datasets.map(s=>({label:s.label,data:s.data,backgroundColor:s.color,borderColor:C.TEAL_1,borderWidth:1.2}))},options:o});}

function scatter(id,d){const el=document.getElementById(id);if(!el)return;
  const o=base(false);o.plugins.tooltip.callbacks={label:c=>d.xlabel+' '+c.parsed.x.toFixed(2)+'  '+d.ylabel+' '+c.parsed.y};
  o.scales={x:ax(d.xlabel),y:ax(d.ylabel,{min:0})};
  new Chart(el,{type:'scatter',data:{datasets:[{data:d.points,backgroundColor:C.GOLD,borderColor:C.TEAL_1,borderWidth:1,radius:5,hoverRadius:7}]},options:o});}

/* parameter sweep line with a parameter toggle (cluster area vs level) */
function sweepline(id,d){const el=document.getElementById(id);if(!el)return;
  let p=d.order[0]; let chart;
  function draw(){const o=base(false);o.parsing=false;
    o.plugins.tooltip.callbacks={title:i=>d.nice[p]+' = '+i[0].parsed.x,label:c=>'cluster area '+(+c.parsed.y).toLocaleString()+' px'};
    o.scales={x:ax(d.nice[p]),y:ax('cluster area (px)')};
    const pts=d.levels[p].map((x,i)=>({x:x,y:d.area[p][i]}));
    if(chart)chart.destroy();
    chart=new Chart(el,{type:'line',data:{datasets:[{data:pts,borderColor:C.GOLD,
      backgroundColor:'rgba(199,160,92,0.15)',pointRadius:3,pointHoverRadius:5,borderWidth:2,tension:.25,fill:true}]},options:o});}
  draw();
  const wrap=el.closest('.card').querySelector('.metric-toggle');
  if(wrap)wrap.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
    if(b.classList.contains('active'))return;
    wrap.querySelectorAll('button').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');p=b.dataset.metric;draw();}));}

/* model leaderboard, horizontal bar with a metric toggle, winner in gold */
function lbboard(id,d){const el=document.getElementById(id);if(!el)return;
  let metric=d.metrics[0].key; let chart;
  function draw(){const m=d.metrics.find(x=>x.key===metric);
    const sorted=[...d.models].sort((a,b)=>b[metric]-a[metric]);
    const labels=sorted.map(x=>x.label), vals=sorted.map(x=>x[metric]);
    const cols=sorted.map(x=>x.winner?C.GOLD:(x[metric]>=m.mid?C.GOLD_2:'rgba(168,181,184,0.55)'));
    const o=base(false);o.indexAxis='y';
    o.plugins.tooltip.callbacks={label:c=>m.label+' '+c.parsed.x.toFixed(3)};
    o.scales={x:ax(m.label,{min:m.min||0,max:m.max,ticks:{color:C.PAPER,font:MF,callback:v=>(+v).toFixed(2)}}),y:ax()};
    if(chart)chart.destroy();
    chart=new Chart(el,{type:'bar',data:{labels,datasets:[{data:vals,backgroundColor:cols,borderColor:C.TEAL_1,borderWidth:1.2}]},options:o});}
  draw();
  const wrap=el.closest('.card').querySelector('.metric-toggle');
  if(wrap)wrap.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
    if(b.classList.contains('active'))return;
    wrap.querySelectorAll('button').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');metric=b.dataset.metric;draw();}));}

/* multi-feature drug timecourse with a feature toggle */
function timecourse(id,d){const el=document.getElementById(id);if(!el)return;
  const COLORS=[C.ICE,C.CLAY,C.GOLD,C.GREEN,C.GOLD_3]; let metric=d.order[0]; let chart;
  function draw(){const sets=d.series.map((s,i)=>({label:s.label,data:d.features[metric][s.key],
      borderColor:COLORS[i%COLORS.length],backgroundColor:COLORS[i%COLORS.length],
      pointRadius:2.5,pointHoverRadius:5,borderWidth:2,tension:0.25}));
    const o=base(true);o.parsing=false;
    o.plugins.tooltip.callbacks={title:items=>'day '+items[0].parsed.x.toFixed(2),label:c=>c.dataset.label+': '+(+c.parsed.y).toLocaleString()};
    o.scales={x:ax('time (days)',{type:'linear',min:0}),y:ax(d.nice[metric])};
    if(chart)chart.destroy(); chart=new Chart(el,{type:'line',data:{datasets:sets},options:o});}
  draw();
  const wrap=el.closest('.card').querySelector('.metric-toggle');
  if(wrap)wrap.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
    if(b.classList.contains('active'))return;
    wrap.querySelectorAll('button').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');metric=b.dataset.metric;draw();}));}
</script>"""

def _chart(b):
    sub = f'<span class="sub">{inline(b["sub"])}</span>' if b.get("sub") else ""
    toggle = ""
    if b.get("toggle"):
        btns = "".join(f'<button class="{"active" if i==0 else ""}" data-metric="{m[0]}">{inline(m[1])}</button>'
                       for i, m in enumerate(b["toggle"]))
        toggle = f'<div class="metric-toggle">{btns}</div>'
    note = f'<p style="margin-top:.9rem;font-size:.94rem;line-height:1.6;color:var(--paper);opacity:.92">{inline(b["note"])}</p>' if b.get("note") else ""
    informs = ""
    if b.get("informs"):
        informs = (f'<div class="verdict">{inline(b["informs"])}'
                   f'<span class="small">{inline(b.get("informs_tag","Informs the method"))}</span></div>')
    h = b.get("height", 380)
    script = f'<script>{b["fn"]}("{b["id"]}",{_json.dumps(b["data"])});</script>'
    return (f'<section class="card"><div class="card-h"><span class="ttl">{b["title"]}</span>'
            f'{toggle}{sub}</div>'
            f'<div class="chart-host" style="height:{h}px"><canvas id="{b["id"]}"></canvas></div>'
            f'{note}{informs}</section>{script}')

_RENDER = dict(hero=_hero, kpis=_kpis, section=_section, figure=_figure,
               prose=_prose, table=_table, tools=_tools, bigcta=_bigcta, chart=_chart)

def render_theme_html(*, title, blocks, rel_root="../", prev_next=None, out_path=None):
    has_charts = any(b["type"] == "chart" for b in blocks)
    head = (CHART_CDN + CHART_RUNTIME) if has_charts else ""
    parts = [head, _header(rel_root, active=None), '<main>']
    for b in blocks:
        fn = _RENDER[b["type"]]
        if b["type"] in ("hero",):
            parts.append(fn(b, rel_root, prev_next))
        elif b["type"] in ("figure", "bigcta"):
            parts.append(fn(b, rel_root))
        else:
            parts.append(fn(b))
    parts.append(
        '<footer>&copy; 2026 Djamel Zair &middot; Amsterdam &middot; '
        '<a href="https://github.com/DjamelZair" target="_blank" rel="noopener">GitHub</a></footer>')
    parts.append('</main>')
    htmlt = _page(title, "".join(parts), rel_root, "style.css")
    if out_path:
        Path(out_path).write_text(htmlt, encoding="utf-8")
    return htmlt


def _strip(s: str) -> str:
    """plain text from a small HTML/markdown title string (for the markdown reader)."""
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&rarr;", "->").strip()

def render_theme_markdown(*, title, blocks, out_path=None):
    """Emit the human-readable markdown reader from the SAME blocks the HTML uses.
    Keeps markdown as the source-of-record while HTML is the citable render."""
    L = []
    for b in blocks:
        t = b["type"]
        if t == "hero":
            L += [f"# {_strip(b['title'])}", "",
                  f"**Thesis target:** {' / '.join(b['meta'])}.", "",
                  f"> {_strip(b['lede'])}", ""]
            if b.get("summary"):
                L += [_strip(b["summary"]), ""]
        elif t == "kpis":
            L += ["| Metric | Value | Note |", "|---|---|---|"]
            L += [f"| {_strip(k['lbl'])} | {_strip(k['num'])} | {_strip(k['desc'])} |"
                  for k in b["items"]] + [""]
        elif t == "section":
            L += [f"## {_strip(b['title'])}"
                  + (f"  ({_strip(b['right'])})" if b.get("right") else ""), ""]
        elif t == "figure":
            if b.get("ttl"):
                L += [f"### {_strip(b['ttl'])}"
                      + (f" - {_strip(b['sub'])}" if b.get("sub") else ""), ""]
            for src in (b["img"] if isinstance(b["img"], list) else [b["img"]]):
                L += [f"![]({src})"]
            L += [""]
            if b.get("shows"):
                L += [f"**What it shows.** {_strip(b['shows'])}", ""]
            if b.get("informs"):
                L += [f"**What it motivated ({_strip(b.get('informs_tag','informs'))}).** "
                      f"{_strip(b['informs'])}", ""]
        elif t == "prose":
            if b.get("title"):
                L += [f"### {_strip(b['title'])}", ""]
            L += [b["text"], ""]
        elif t == "table":
            if b.get("title"):
                L += [f"### {_strip(b['title'])}", ""]
            L += ["| " + " | ".join(_strip(c) for c in b["head"]) + " |",
                  "|" + "|".join("---" for _ in b["head"]) + "|"]
            L += ["| " + " | ".join(_strip(c) for c in r) + " |" for r in b["rows"]] + [""]
        elif t == "chart":
            L += [f"### {_strip(b['title'])}"
                  + (f" - {_strip(b['sub'])}" if b.get("sub") else ""), "",
                  "*(interactive chart in the HTML version)*", ""]
            if b.get("note"):
                L += [f"**What it shows.** {_strip(b['note'])}", ""]
            if b.get("informs"):
                L += [f"**What it motivated ({_strip(b.get('informs_tag','informs'))}).** "
                      f"{_strip(b['informs'])}", ""]
        elif t == "tools":
            L += ["**Sources / tools:** " + ", ".join(_strip(c["t"]) for c in b["chips"]), ""]
    md = "\n".join(L).rstrip() + "\n"
    if out_path:
        Path(out_path).write_text(md, encoding="utf-8")
    return md


# ---- landing (index) -------------------------------------------------------------------
def render_landing(*, themes, tape, hero, out_path=None):
    tape_items = "".join(
        (f'<span class="gold">{inline(t)}</span><span class="dot">&middot;</span>'
         if i % 2 == 0 else f'<span>{inline(t)}</span><span class="dot">&middot;</span>')
        for i, t in enumerate(tape))
    tape_block = (f'<div class="tape" aria-hidden="true"><div class="tape-track">'
                  f'{tape_items}{tape_items}</div></div>')

    cards = []
    for t in themes:
        feat = " featured-rq" if t.get("featured") else ""
        disabled = "" if t.get("ready") else ' style="opacity:.55;pointer-events:none"'
        link = "Open &rarr;" if t.get("ready") else "Pending"
        cards.append(
            f'<a class="rq{feat}" href="{t["href"]}"{disabled}>'
            f'<div class="rq-num">{t["num"]}</div>'
            f'<div class="rq-name">{t["name"]}</div>'
            f'<p class="rq-lede">{inline(t["lede"])}</p>'
            f'<div class="rq-foot"><span class="rq-metric">{inline(t["metric"])}</span>'
            f'<span class="rq-link">{link}</span></div></a>')
    cards_html = "".join(cards)

    kpis = "".join(
        f'<div class="it"><div class="v{" gold" if k.get("gold") else ""}">{inline(k["v"])}</div>'
        f'<div class="l">{inline(k["l"])}</div></div>' for k in hero["kpis"])

    body = f"""<header>
  <div class="header-inner">
    <a href="#top" class="brand-block">
      <span class="brand-name">CLL &rarr; CPM<span class="role">Analysis appendix &middot; MSc thesis</span></span>
    </a>
    <nav class="top"><a href="#themes">Themes</a><a href="THESIS_CITE_MAP.md">Cite map</a>
      <a href="https://github.com/DjamelZair" target="_blank" rel="noopener">GitHub</a></nav>
  </div>
</header>
<a id="top"></a>
<section class="hero" style="background:none;border:none;box-shadow:none;padding:0">
  <div class="wrap">
    <section class="bhero" style="min-height:520px">
      <div class="bg" style="background-image:url('{hero["image"]}')"></div>
      <div class="radial"></div><div class="scrim"></div>
      <div class="inner">
        <div class="meta"><span>Exploratory &amp; analytical work</span><span class="dot">&middot;</span>
          <span>Examiner index</span><span class="dot">&middot;</span>
          <span>Djamel Zair &middot; MSc AI, UvA &middot; 2025-2026</span></div>
        <h1>{hero["title"]}</h1>
        <p class="lede">{inline(hero["lead"])}</p>
        <div class="cta-row">
          <a class="cta primary" href="#themes">Browse the five themes &darr;</a>
          <a class="cta" href="https://github.com/DjamelZair" target="_blank" rel="noopener">GitHub &nearr;</a>
        </div>
      </div>
      <div class="cap">CLL spheroid &middot; brightfield &middot; AI-drawn outline</div>
    </section>
  </div>
  {tape_block}
</section>
<section class="featured" id="themes">
  <div class="wrap">
    <div class="feat-head">
      <div>
        <span class="eyebrow">Five analysis themes &middot; mapped to research question &amp; thesis section</span>
        <h2>The analysis <span class="it">behind</span><br>the thesis, <span class="it">curated</span>.</h2>
        <p style="font-family:'Instrument Serif',serif;font-style:italic;font-size:1.2rem;color:#e7c98a;margin-top:.6rem;max-width:52ch;line-height:1.4">
          Each study reads as "here is what I found and why it shaped the method." Figures are
          embedded as-is from the executed notebooks.</p>
      </div>
      <div class="meta">Appendix A-J<br>RQ1 &middot; RQ2 &middot; RQ3<br>2025-2026</div>
    </div>
    <div class="feat-rqs">{cards_html}</div>
    <div class="feat-kpis">{kpis}</div>
  </div>
</section>
<footer>&copy; 2026 Djamel Zair &middot; Amsterdam &middot;
  <a href="https://github.com/DjamelZair" target="_blank" rel="noopener">GitHub</a></footer>
"""
    htmlt = _page("CLL CPM thesis - analysis index", body, "", "landing.css")
    if out_path:
        Path(out_path).write_text(htmlt, encoding="utf-8")
    return htmlt
