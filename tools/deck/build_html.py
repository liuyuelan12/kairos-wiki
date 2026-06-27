#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kairos Deck v2 -> 自包含 HTML -> Chrome PDF。BGB 设计系统（移植 Agentum），币安金主色 + cyan 次级。
用法: python3 tools/deck/build_html.py [--pdf]
"""
import argparse, base64, html, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from slides import SLIDES, LOGO_SM  # noqa

OUT_HTML = os.path.join(ROOT, "output", "deck", "Kairos-Deck-zh.html")
OUT_PDF = os.path.join(ROOT, "output", "deck", "Kairos-Deck-zh.pdf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = os.path.join(HERE, "assets", "fonts-embedded.css")
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".webp": "image/webp", ".svg": "image/svg+xml"}


def uri(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.isfile(p):
        return ""
    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{MIME.get(os.path.splitext(p)[1].lower(),'image/png')};base64,{b64}"


def e(s):
    return html.escape(str(s)).replace("\n", "<br>")


CSS = """
:root{
 --ink:#0B0B0B;--panel:#141414;--panel-2:#191919;--panel-3:#1F1F1F;
 --gold:#F0B90B;--gold-d:#B8860B;--gold-l:#FCD535;--cyan:#16D2E8;
 --white:#FFFFFF;--text:#FFFFFF;--body:#C2C2C2;--muted:#8A8A8A;--faint:#5C5C5C;
 --line:rgba(255,255,255,.08);--line-2:rgba(255,255,255,.16);
 --glow:0 0 44px rgba(240,185,11,.40);--glow-sm:0 0 14px rgba(240,185,11,.55);
 --display:'Archivo','PingFang SC','Microsoft YaHei',sans-serif;
 --bodyf:'General Sans','PingFang SC','Microsoft YaHei',system-ui,sans-serif;
 --mono:'Spline Sans Mono',ui-monospace,monospace;}
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
@page{size:1280px 720px;margin:0}
body{background:#000;font-family:var(--bodyf);color:var(--text)}
.slide{position:relative;width:1280px;height:720px;overflow:hidden;background:var(--ink);
 page-break-after:always;break-after:page}
.slide:last-child{page-break-after:auto}
.pad{position:absolute;inset:0;padding:60px 84px;display:flex;flex-direction:column}
.glow{position:absolute;border-radius:50%;pointer-events:none;filter:blur(70px)}
.glow.a{width:560px;height:560px;right:-160px;top:-180px;background:radial-gradient(circle,rgba(240,185,11,.16),transparent 65%)}
.glow.b{width:520px;height:520px;left:-200px;bottom:-220px;background:radial-gradient(circle,rgba(240,185,11,.10),transparent 65%)}
.gridbg{position:absolute;inset:0;pointer-events:none;
 background-image:linear-gradient(rgba(240,185,11,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(240,185,11,.05) 1px,transparent 1px);
 background-size:48px 48px;-webkit-mask-image:radial-gradient(120% 120% at 50% 30%,#000 26%,transparent 84%)}
.top{position:relative;height:30px;flex:0 0 auto;margin-bottom:14px}
.top .rule{position:absolute;left:0;right:0;top:24px;height:2px;background:var(--line-2)}
.top .seg{position:absolute;left:0;top:24px;width:62px;height:2px;background:var(--gold);box-shadow:var(--glow-sm)}
.top .no{position:absolute;right:0;top:-2px;font-family:var(--display);font-weight:800;font-size:20px;color:var(--muted);letter-spacing:.04em}
.kicker{font-family:var(--mono);font-size:12px;letter-spacing:.26em;text-transform:uppercase;color:var(--gold)}
.h1{font-family:var(--display);font-weight:900;line-height:.96;letter-spacing:-.02em;color:var(--white)}
.h2{font-family:var(--display);font-weight:800;font-size:46px;line-height:1.04;letter-spacing:-.01em;color:var(--white)}
.dotitle{display:flex;align-items:center;gap:16px}
.dotitle .dot{width:20px;height:20px;border-radius:50%;background:var(--gold);box-shadow:var(--glow-sm);flex:0 0 auto}
.dotitle h2{font-size:38px}
.cy{color:var(--gold)}.gd{color:var(--gold)}
.lede{color:var(--body);font-size:18px;line-height:1.6;max-width:920px}
.lede.sm{font-size:15.5px;line-height:1.58}
.body-col{flex:1;display:flex;flex-direction:column;z-index:2;min-height:0}
.mut{color:var(--muted)}.wt{color:var(--white)}
.grad{background:linear-gradient(96deg,var(--gold-l) 6%,var(--gold) 60%,var(--gold-d));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
/* cover */
.cv-brand{display:flex;align-items:center;gap:12px}
.cv-brand img{width:36px;height:36px;filter:drop-shadow(0 0 12px rgba(240,185,11,.6))}
.cv-brand .wm{font-family:var(--display);font-weight:800;font-size:23px;letter-spacing:.02em}
.backed{position:absolute;left:84px;bottom:46px;z-index:3}
.backed .bl{font-family:var(--mono);font-size:10.5px;letter-spacing:.24em;color:var(--muted);margin-bottom:10px}
.backed .brow{display:flex;gap:9px;flex-wrap:wrap}
.backed .bt{background:#fff;border-radius:7px;height:38px;padding:6px 11px;display:flex;align-items:center}
.backed .bt img{max-height:24px;max-width:96px;object-fit:contain}
/* investors */
.vcgrid{display:grid;grid-template-columns:repeat(6,1fr);gap:13px;margin-top:8px}
.vctile{background:#fff;border-radius:12px;height:74px;display:flex;align-items:center;justify-content:center;padding:13px}
.vctile img{max-width:100%;max-height:42px;object-fit:contain}
.vccaps{display:grid;grid-template-columns:1fr 1fr;gap:7px 40px;margin-top:22px}
.vccaps div{font-size:14px;color:var(--body);line-height:1.4}
.vccaps b{color:var(--gold);font-family:var(--display);font-weight:700}
/* cards */
.cardgrid{display:grid;gap:18px;margin-top:8px}
.card{position:relative;background:var(--panel);border:1px solid var(--line);border-top:3px solid var(--gold);
 border-radius:16px;padding:22px 24px;overflow:hidden}
.card .tag{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;color:var(--gold)}
.card h3{font-family:var(--display);font-weight:800;font-size:23px;margin:7px 0 9px;color:var(--white)}
.card p{color:var(--body);font-size:15.5px;line-height:1.5}
/* statgrid */
.statgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:8px}
.stat{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:18px;
 padding:24px 26px;min-height:150px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}
.stat .lab{font-size:13.5px;color:var(--muted);max-width:82%;line-height:1.35}
.stat .num{font-family:var(--display);font-weight:800;font-size:46px;line-height:1;letter-spacing:-.02em;color:var(--white)}
.stat .num.hero{color:var(--gold);font-size:62px}
.stat .num.small{font-size:30px}
.stat .wmk{position:absolute;right:16px;bottom:8px;font-size:80px;color:rgba(255,255,255,.04);line-height:1}
/* concept */
.cc{display:flex;gap:42px;margin-top:14px;align-items:center;flex:1}
.cc .L{flex:1}.cc .R{width:430px;display:flex;justify-content:center;align-items:center}
.cc .R img{width:430px;height:430px;object-fit:contain;filter:drop-shadow(0 0 50px rgba(240,185,11,.28));
 -webkit-mask-image:radial-gradient(ellipse 72% 72% at 50% 50%,#000 60%,transparent 82%);
 mask-image:radial-gradient(ellipse 72% 72% at 50% 50%,#000 60%,transparent 82%)}
.callout{margin-top:24px;background:linear-gradient(180deg,rgba(240,185,11,.12),rgba(240,185,11,.03));
 border:1px solid rgba(240,185,11,.5);border-radius:16px;padding:22px 26px;box-shadow:inset 0 0 30px rgba(240,185,11,.06)}
.callout .big{font-family:var(--display);font-weight:800;font-size:36px}
.callout .sub{font-size:15px;color:var(--body);margin-top:8px}
.example{margin-top:20px;font-size:17px;color:#E6E6E6;line-height:1.5}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px;max-width:560px}
.chip{border:1px solid var(--line-2);background:#141414;border-radius:999px;padding:7px 15px;font-size:14px;color:#E6E6E6}
.barviz{width:430px}
.bvtot{font-family:var(--display);font-weight:800;text-align:center;font-size:28px;color:var(--gold);margin-bottom:16px}
.bvbar{display:flex;height:92px;border-radius:14px;overflow:hidden;border:1px solid var(--line-2);box-shadow:var(--glow)}
.bvyes{width:18%;background:linear-gradient(180deg,var(--gold-l),var(--gold));color:#1a1200;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:13px;text-align:center}
.bvno{width:82%;background:linear-gradient(180deg,#3de6f6,var(--cyan));color:#042129;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:18px}
.bvleg{display:flex;justify-content:space-between;margin-top:14px;font-family:var(--mono);font-size:13px}
.bvleg .y{color:var(--gold)}.bvleg .n{color:var(--cyan)}
/* cols */
.cols{display:grid;gap:24px;margin-top:14px}
.col .no{font-family:var(--display);font-weight:800;font-size:15px;color:var(--gold);letter-spacing:.04em}
.col h3{font-family:var(--display);font-weight:800;font-size:22px;margin:11px 0 9px;color:var(--white)}
.col p{color:var(--body);font-size:15px;line-height:1.52}
/* flow */
.flow{display:grid;gap:14px;position:relative;margin-top:18px}
.fnode{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:24px 20px;text-align:center;position:relative}
.fnode .b{width:54px;height:54px;border-radius:50%;margin:0 auto 16px;display:grid;place-items:center;
 font-family:var(--display);font-weight:800;font-size:19px;color:#1a1200;
 background:radial-gradient(circle at 45% 30%,var(--gold-l),var(--gold) 55%,var(--gold-d));box-shadow:var(--glow-sm)}
.fnode h4{font-family:var(--display);font-weight:800;font-size:21px;margin-bottom:9px;color:var(--white)}
.fnode p{color:var(--body);font-size:14px;line-height:1.45}
.fnode .ar{position:absolute;right:-11px;top:46px;color:var(--gold);font-size:20px;z-index:3}
/* feature cards w/ 3D icon */
.fcards{display:grid;gap:18px;margin-top:14px}
.fcard{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:22px 20px;overflow:hidden}
.fcard .ic3d{width:96px;height:96px;display:block;margin:-10px auto 6px;object-fit:contain;
 filter:drop-shadow(0 0 16px rgba(240,185,11,.32));
 -webkit-mask-image:radial-gradient(circle at 50% 50%,#000 62%,transparent 80%);mask-image:radial-gradient(circle at 50% 50%,#000 62%,transparent 80%)}
.fcard .tag{font-family:var(--mono);font-size:10.5px;color:var(--gold);letter-spacing:.06em;text-align:center;display:block}
.fcard h3{font-family:var(--display);font-weight:800;font-size:19px;margin:5px 0 8px;color:var(--white);text-align:center}
.fcard p{color:var(--body);font-size:13.5px;line-height:1.48;text-align:center}
/* spec / comparison table */
.cmp{width:100%;border-collapse:separate;border-spacing:0;margin-top:18px;font-size:18px}
.cmp th{font-family:var(--display);font-weight:800;padding:15px 22px;text-align:left;font-size:16px}
.cmp thead th{background:#141414;color:#cfcfcf}
.cmp thead th:last-child{color:#1a1200;background:linear-gradient(180deg,var(--gold-l),var(--gold))}
.cmp td{padding:15px 22px;border-bottom:1px solid var(--line)}
.cmp tbody td:first-child{color:var(--gold);font-weight:700;font-family:var(--display)}
.cmp tbody td:nth-child(2){color:var(--muted)}
.cmp tbody td:last-child{color:#fff;font-weight:600}
.cmp tbody tr:last-child td{border-bottom:none}
/* eco radial */
.eco{position:relative;flex:1;margin-top:6px}
.eco svg{position:absolute;inset:0;width:100%;height:100%}
.eco .er{fill:none;stroke:var(--line);stroke-width:1}
.eco-mark{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:3;
 width:104px;height:104px;border-radius:50%;display:grid;place-items:center;text-align:center;
 background:radial-gradient(circle at 45% 35%,rgba(240,185,11,.28),rgba(240,185,11,.04));border:1px solid var(--line-2);box-shadow:var(--glow)}
.eco-mark span{font-family:var(--display);font-weight:800;font-size:14px;color:var(--white);line-height:1.1}
.enode{position:absolute;transform:translate(-50%,-50%);z-index:2;display:flex;align-items:center;gap:8px;
 font-size:13px;color:var(--body);white-space:nowrap}
.enode .ed{width:9px;height:9px;border-radius:50%;background:var(--gold);box-shadow:0 0 8px var(--gold);flex:0 0 auto}
.enode.out{font-family:var(--display);font-weight:800;font-size:13px;color:var(--gold);text-transform:uppercase;letter-spacing:.04em}
.enode.out .ed{background:var(--cyan);box-shadow:0 0 8px var(--cyan)}
/* biz donut */
.bizrow{display:flex;gap:40px;margin-top:14px;flex:1;align-items:center}
.fees{flex:1;display:flex;flex-direction:column;gap:18px}
.feecard{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:14px;padding:20px 24px;display:flex;align-items:baseline;gap:18px}
.feecard .v{font-family:var(--display);font-weight:900;font-size:48px;color:var(--gold);line-height:1}
.feecard .k{font-size:20px;font-weight:700;color:#fff}.feecard .s{font-size:14px;color:var(--muted);margin-top:4px}
.dist{position:relative;width:540px;height:420px}
.donut3d{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:300px;height:300px;object-fit:contain;
 filter:drop-shadow(0 0 30px rgba(240,185,11,.25));
 -webkit-mask-image:radial-gradient(circle at 50% 50%,#000 66%,transparent 76%);mask-image:radial-gradient(circle at 50% 50%,#000 66%,transparent 76%)}
.donutmid{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);text-align:center;z-index:2}
.donutmid b{font-family:var(--display);font-weight:800;font-size:26px;color:#fff}
.donutmid span{display:block;font-family:var(--mono);font-size:9px;color:var(--muted);letter-spacing:.14em;margin-top:2px}
.lbl{position:absolute;width:150px}
.lbl .p{font-family:var(--display);font-weight:800;font-size:28px;color:var(--gold);line-height:1}
.lbl .n{color:var(--body);font-size:13.5px;margin-top:3px}
.lbl.r{text-align:left}.lbl.l{text-align:right}
/* roadmap */
.road{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;position:relative;margin-top:24px}
.rtrack{position:absolute;left:3%;right:3%;top:26px;height:8px;border-radius:6px;background:var(--panel-2);border:1px solid var(--line)}
.rtrack .fill{position:absolute;left:0;top:0;bottom:0;width:14%;border-radius:6px;background:linear-gradient(90deg,var(--gold),var(--gold-d));box-shadow:var(--glow-sm)}
.rp{position:relative;padding-top:56px;text-align:center}
.rp .pin{position:absolute;left:50%;top:18px;transform:translateX(-50%);width:24px;height:24px;border-radius:50%;
 background:var(--panel-2);border:2px solid var(--line-2);display:grid;place-items:center;color:var(--faint);font-size:11px}
.rp.done .pin{background:radial-gradient(circle at 45% 30%,var(--gold-l),var(--gold));border-color:var(--gold);color:#1a1200;box-shadow:var(--glow-sm)}
.rp .ph{font-family:var(--mono);font-size:10.5px;color:var(--faint);letter-spacing:.1em}
.rp h4{font-family:var(--display);font-weight:800;font-size:17px;margin:8px 0 7px;color:var(--white)}
.rp p{color:var(--muted);font-size:12.5px;line-height:1.42}
.rp .badge{display:inline-block;margin-top:9px;font-family:var(--mono);font-size:9.5px;color:var(--gold);border:1px solid var(--line-2);border-radius:5px;padding:3px 7px}
.closing{margin-top:30px;text-align:center;font-family:var(--display);font-weight:900;font-size:40px;letter-spacing:.02em}
/* team */
.tlist{display:grid;grid-template-columns:1fr 1fr;gap:20px 56px;margin-top:6px}
.tm{display:flex;align-items:flex-start;gap:18px}
.tm .av{width:70px;height:70px;border-radius:50%;object-fit:cover;flex:0 0 auto;box-shadow:0 0 0 1.5px var(--gold),0 0 18px rgba(240,185,11,.3)}
.tm .nm{font-family:var(--display);font-weight:800;font-size:17px;color:var(--gold)}
.tm .rl{font-family:var(--mono);font-size:11px;color:var(--muted);margin-top:2px}
.tm .dash{width:24px;height:2px;background:var(--line-2);margin:7px 0 7px}
.tm .bio{color:var(--body);font-size:13px;line-height:1.45}
.note{font-family:var(--mono);font-size:11.5px;color:var(--faint);letter-spacing:.02em;line-height:1.5;margin-top:16px}
.brandmark{position:absolute;right:60px;bottom:24px;display:flex;align-items:center;gap:7px;opacity:.8;z-index:4}
.brandmark img{height:20px}.brandmark span{font-family:var(--display);font-weight:800;letter-spacing:.1em;font-size:13px;color:var(--gold)}
"""


def top(s):
    return f'<div class="top"><div class="rule"></div><div class="seg"></div><div class="no">{e(s.get("no",""))}</div></div>'


def htitle(s):
    if s.get("dot"):
        h = f'<div class="dotitle" style="margin-bottom:8px"><span class="dot"></span><h2>{e(s["title"])}</h2></div>'
    else:
        h = f'<h2 class="h2" style="margin-bottom:12px">{e(s["title"])}</h2>'
    if s.get("kicker") and not s.get("dot"):
        h = f'<span class="kicker">{e(s["kicker"])}</span>' + h
    lede = f'<div class="lede" style="margin-bottom:8px">{e(s["lede"])}</div>' if s.get("lede") else ""
    return h + lede


def brandmark():
    return f'<div class="brandmark"><img src="{uri(LOGO_SM)}"><span>KAIROS</span></div>'


def wrap(inner, center=True, glow="a"):
    g = "".join(f'<div class="glow {x}"></div>' for x in glow)
    jc = "center" if center else "flex-start"
    return (f'<section class="slide">{g}<div class="gridbg"></div><div class="pad">'
            f'<div class="body-col" style="justify-content:{jc}">{inner}</div></div>{brandmark()}</section>')


# ---- layouts ----
def L_cover(s):
    backed = "".join(f'<div class="bt"><img src="{uri(f)}"></div>' for f in s["backed_by"])
    return (f'<section class="slide">'
            f'<img src="{uri(s["hero"])}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:right center;z-index:0">'
            f'<div style="position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,rgba(7,7,7,.96) 0 34%,rgba(7,7,7,.55) 54%,rgba(7,7,7,0) 74%)"></div>'
            f'<div class="cv-brand" style="position:absolute;top:54px;left:84px;z-index:3"><img src="{uri(LOGO_SM)}"><span class="wm grad">Kairos</span></div>'
            f'<div style="position:absolute;left:84px;top:47%;transform:translateY(-50%);max-width:640px;z-index:3">'
            f'<span class="kicker">{e(s["kicker"])}</span>'
            f'<h1 class="h1 grad" style="font-size:104px;margin:14px 0 14px">{e(s["brand"])}</h1>'
            f'<p class="h2 cy" style="font-size:27px;font-weight:800;max-width:520px;margin-bottom:18px">{e(s["sub"])}</p>'
            f'<p class="lede" style="max-width:500px;margin-bottom:20px">{e(s["lede"])}</p>'
            f'<span class="kicker" style="color:var(--body);letter-spacing:.12em">◆ {e(s["chain"])}</span></div>'
            f'<div class="backed"><div class="bl">BACKED BY WORLD-CLASS INVESTORS</div><div class="brow">{backed}</div></div>'
            f'</section>')


def L_investors(s):
    tiles = "".join(f'<div class="vctile"><img src="{uri(v["file"])}"></div>' for v in s["vcs"])
    caps = "".join(f'<div><b>{e(v["name"])}</b> — {e(v["cap"])}</div>' for v in s["vcs"] if v.get("cap"))
    inner = (top(s) +
             f'<span class="kicker">{e(s["kicker"])}</span>'
             f'<h2 class="h2" style="font-size:48px;margin:10px 0 14px">{e(s["title"])}</h2>'
             f'<div class="lede" style="margin-bottom:22px">{e(s["lede"])}</div>'
             f'<div class="vcgrid">{tiles}</div><div class="vccaps">{caps}</div>')
    return wrap(inner, center=False, glow="ab")


def L_cards(s):
    cols = s.get("cols", 2)
    cards = "".join(f'<div class="card"><span class="tag">{e(c.get("tag",""))}</span>'
                    f'<h3>{e(c["h"])}</h3><p>{e(c["t"])}</p></div>' for c in s["cards"])
    inner = top(s) + htitle(s) + f'<div class="cardgrid" style="grid-template-columns:repeat({cols},1fr)">{cards}</div>'
    return wrap(inner)


def L_statgrid(s):
    cells = ""
    for st in s["stats"]:
        cls = "num" + (" hero" if st.get("hero") else "") + (" small" if st.get("small") else "")
        cells += f'<div class="stat"><div class="lab">{e(st["lab"])}</div><div class="{cls}">{e(st["num"])}</div></div>'
    note = f'<div class="note">{e(s["note"])}</div>' if s.get("note") else ""
    inner = top(s) + htitle(s) + f'<div class="statgrid">{cells}</div>' + note
    return wrap(inner)


def L_concept(s):
    L = ""
    if s.get("callout"):
        L += (f'<div class="callout"><div class="big grad">{e(s["callout"])}</div>'
              f'<div class="sub">{e(s.get("callout_sub",""))}</div></div>')
    if s.get("example"):
        L += f'<div class="example">{e(s["example"])}</div>'
    if s.get("chips"):
        L += '<div class="chips">' + "".join(f'<span class="chip">{e(c)}</span>' for c in s["chips"]) + '</div>'
    if s.get("hero") and uri(s["hero"]):
        R = f'<div class="R"><img src="{uri(s["hero"])}"></div>'
    elif s.get("barviz"):
        R = ('<div class="R"><div class="barviz"><div class="bvtot">＝ $1.00</div>'
             '<div class="bvbar"><div class="bvyes">YES<br>0.18</div><div class="bvno">NO　0.82</div></div>'
             '<div class="bvleg"><span class="y">买 YES @0.18</span><span class="n">≡ 卖 NO @0.82</span></div></div></div>')
    else:
        R = ""
    inner = top(s) + htitle(s) + f'<div class="cc"><div class="L">{L}</div>{R}</div>'
    return wrap(inner)


def L_cols(s):
    cols = s.get("cols", 3)
    items = "".join(f'<div class="col"><div class="no">{e(i["n"])}</div><h3>{e(i["h"])}</h3><p>{e(i["t"])}</p></div>'
                    for i in s["items"])
    inner = top(s) + htitle(s) + f'<div class="cols" style="grid-template-columns:repeat({cols},1fr)">{items}</div>'
    return wrap(inner)


def L_flow(s):
    n = len(s["steps"])
    nodes = ""
    for i, st in enumerate(s["steps"]):
        ar = '<span class="ar">→</span>' if i < n - 1 else ""
        nodes += f'<div class="fnode"><div class="b">{e(st["b"])}</div><h4>{e(st["h"])}</h4><p>{e(st["t"])}</p>{ar}</div>'
    inner = top(s) + htitle(s) + f'<div class="flow" style="grid-template-columns:repeat({n},1fr)">{nodes}</div>'
    return wrap(inner)


def L_spec(s):
    th = "".join(f'<th>{e(h)}</th>' for h in s["headers"])
    rows = "".join("<tr>" + "".join(f'<td>{e(c)}</td>' for c in r) + "</tr>" for r in s["rows"])
    inner = top(s) + htitle(s) + f'<table class="cmp"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>'
    return wrap(inner)


def L_fcards(s):
    cards = "".join(f'<div class="fcard"><img class="ic3d" src="{uri(c["icon"])}">'
                    f'<span class="tag">{e(c["tag"])}</span><h3>{e(c["h"])}</h3><p>{e(c["t"])}</p></div>'
                    for c in s["cards"])
    inner = top(s) + htitle(s) + f'<div class="fcards" style="grid-template-columns:repeat({len(s["cards"])},1fr)">{cards}</div>'
    return wrap(inner)


def L_eco(s):
    # inner 6 modules + outer 3 共建, positioned around center
    inner_pos = [(50, 14), (80, 33), (80, 67), (50, 86), (20, 67), (20, 33)]
    out_pos = [(50, 3), (93, 84), (7, 84)]
    nodes = ""
    for (x, y), label in zip(inner_pos, s["inner"]):
        nodes += f'<div class="enode" style="left:{x}%;top:{y}%"><span class="ed"></span>{e(label)}</div>'
    for (x, y), label in zip(out_pos, s["outer"]):
        nodes += f'<div class="enode out" style="left:{x}%;top:{y}%"><span class="ed"></span>{e(label)}</div>'
    eco = (f'<div class="eco"><svg viewBox="0 0 1112 430" preserveAspectRatio="xMidYMid meet">'
           f'<ellipse class="er" cx="556" cy="215" rx="150" ry="118"/>'
           f'<ellipse class="er" cx="556" cy="215" rx="290" ry="188"/>'
           f'<ellipse class="er" cx="556" cy="215" rx="430" ry="208"/></svg>'
           f'<div class="eco-mark"><span>{e(s["center"])}</span></div>{nodes}</div>')
    inner = top(s) + htitle(s) + eco
    return wrap(inner, center=False)


def L_biz(s):
    fees = "".join(f'<div class="feecard"><div class="v">{e(f["v"])}</div><div><div class="k">{e(f["k"])}</div>'
                   f'<div class="s">{e(f["s"])}</div></div></div>' for f in s["fees"])
    labels = ""
    for seg in s["segs"]:
        side = seg["side"]; pos = f'left:6px;' if side == "l" else f'right:6px;'
        labels += (f'<div class="lbl {side}" style="{pos}top:{seg["top"]}px">'
                   f'<div class="p">{e(seg["p"])}</div><div class="n">{e(seg["n"])}</div></div>')
    dm = s["donut_center"]
    dist = (f'<div class="dist"><img class="donut3d" src="{uri(s["donut"])}">'
            f'<div class="donutmid"><b>{e(dm[0])}</b><span>{e(dm[1])}</span></div>{labels}</div>')
    note = f'<div class="note">{e(s["note"])}</div>' if s.get("note") else ""
    inner = top(s) + htitle(s) + f'<div class="bizrow"><div class="fees">{fees}</div>{dist}</div>' + note
    return wrap(inner)


def L_team(s):
    mem = "".join(f'<div class="tm"><img class="av" src="{uri(m["photo"])}"><div>'
                  f'<div class="nm">{e(m["name"])}</div><div class="rl">{e(m["role"])}</div>'
                  f'<div class="dash"></div><div class="bio">{e(m["bio"])}</div></div></div>' for m in s["members"])
    note = f'<div class="note">{e(s["note"])}</div>' if s.get("note") else ""
    inner = top(s) + htitle(s) + f'<div class="tlist">{mem}</div>' + note
    return wrap(inner)


def L_roadmap(s):
    rps = ""
    for p in s["phases"]:
        done = " done" if p.get("done") else ""
        pin = "✓" if p.get("done") else "▶"
        badge = f'<span class="badge">{e(p["badge"])}</span>' if p.get("badge") else ""
        rps += (f'<div class="rp{done}"><div class="pin">{pin}</div><div class="ph">{e(p["ph"])}</div>'
                f'<h4>{e(p["h"])}</h4><p>{e(p["t"])}</p>{badge}</div>')
    closing = f'<div class="closing grad">{e(s["closing"])}</div>' if s.get("closing") else ""
    note = f'<div class="note" style="text-align:center;margin-top:18px">{e(s["note"])}</div>' if s.get("note") else ""
    inner = top(s) + htitle(s) + f'<div class="road"><div class="rtrack"><div class="fill"></div></div>{rps}</div>' + closing + note
    return wrap(inner)


RENDER = {"cover": L_cover, "investors": L_investors, "cards": L_cards, "statgrid": L_statgrid,
          "concept": L_concept, "cols": L_cols, "flow": L_flow, "spec": L_spec, "fcards": L_fcards,
          "eco": L_eco, "biz": L_biz, "team": L_team, "roadmap": L_roadmap}


def build():
    fonts = open(FONTS, encoding="utf-8").read() if os.path.isfile(FONTS) else ""
    body = "".join(RENDER[s["layout"]](s) for s in SLIDES)
    doc = (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
           f'<style>{fonts}</style><style>{CSS}</style></head><body>{body}</body></html>')
    os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
    open(OUT_HTML, "w", encoding="utf-8").write(doc)
    print(f"✔ HTML -> {OUT_HTML} ({len(doc)//1024} KB, {len(SLIDES)} slides)")


def to_pdf():
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={OUT_PDF}", "file://" + OUT_HTML], capture_output=True, timeout=180)
    print(f"✔ PDF  -> {OUT_PDF} ({os.path.getsize(OUT_PDF)//1024} KB)" if os.path.isfile(OUT_PDF) else "✗ PDF failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args(); build()
    if a.pdf:
        to_pdf()
