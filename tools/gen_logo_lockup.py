#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kairos 旭日 logo —— 字标锁版(lockup)。在扁平旭日徽标旁/下加「Kairos」字样,扁平币安金、透明底。
复用 tools/gen_logo_sunrise.py 的徽标几何(变体 C: --flat --rays 21 --ray-half-w 2.6),
徽标以「嵌套 <svg> + 裁切到内容包围盒」方式嵌入,再排版字标,零额外依赖。

两种排布:
  below : 字在徽标下方(竖版锁版)
  right : 字在徽标右侧(横版锁版)

用法:
  python3 tools/gen_logo_lockup.py                 # 两种排布都出
  python3 tools/gen_logo_lockup.py --layout below
  python3 tools/gen_logo_lockup.py --text KAIROS --font "Avenir Next" --uppercase

输出 -> wiki/品牌/logo/sunrise_<layout>.svg + sunrise_<layout>_<w>.png
栅格器:rsvg-convert(librsvg)。字体走 fontconfig(默认 Avenir Next);PNG 已把字形烤进像素,跨机可用。
"""
import argparse, math, os, shutil, subprocess, sys, types

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import gen_logo_sunrise as gls  # 复用 build_svg / 配色常量

OUT_DIR = os.path.join(ROOT, "wiki", "品牌", "logo")
GOLD = gls.GOLD_FLAT  # #F0B90B


def emblem_params():
    """变体 C 的徽标参数(与定版扁平 logo 一致)。"""
    return types.SimpleNamespace(
        size=1024, rays=21, sun_radius=150.0, ray_inner=172.0, ray_outer=430.0,
        ray_half_w=2.6, span_start=8.0, span_end=172.0,
        horizon_thick=30.0, horizon_extra=200.0, flat=True,
    )


def emblem_inner_and_bbox(p):
    """返回(徽标内部标记, 内容包围盒 (bx,by,bw,bh))。内部标记不含外层<svg>,供嵌套复用。"""
    full = gls.build_svg(p)
    inner = full[full.index(">") + 1: full.rindex("</svg>")]

    cx = p.size / 2.0
    horizon_y = p.size / 2.0 + p.ray_outer / 2.0
    rx_right = cx + p.ray_outer * math.cos(math.radians(p.span_start))  # 最右尖刺
    rx_left = cx + p.ray_outer * math.cos(math.radians(p.span_end))     # 最左尖刺
    bar_hw = p.sun_radius + p.horizon_extra
    x_min = min(rx_left, cx - bar_hw)
    x_max = max(rx_right, cx + bar_hw)
    y_min = horizon_y - p.ray_outer              # 顶端(90°)尖刺
    y_max = horizon_y + p.horizon_thick / 2.0    # 地平线条下沿
    pad = 0.02 * (x_max - x_min)
    bx, by = x_min - pad, y_min - pad
    bw, bh = (x_max - x_min) + 2 * pad, (y_max - y_min) + 2 * pad
    return inner, (bx, by, bw, bh)


def f(x):
    return f"{x:.2f}"


def nested_emblem(inner, bbox, x, y, w, h):
    """把徽标内部标记放进一个定位/裁切用的嵌套 <svg>。"""
    bx, by, bw, bh = bbox
    return (
        f'<svg x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" '
        f'viewBox="{f(bx)} {f(by)} {f(bw)} {f(bh)}" overflow="visible">'
        f"{inner}</svg>"
    )


def text_el(text, x, y, font_size, font, anchor="middle"):
    ls = font_size * 0.01  # 轻微字距
    return (
        f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" '
        f'font-family="{font}, sans-serif" font-weight="700" '
        f'font-size="{f(font_size)}" letter-spacing="{f(ls)}" '
        f'fill="{GOLD}">{text}</text>'
    )


def build_lockup(layout, text, font, p):
    inner, bbox = emblem_inner_and_bbox(p)
    bw, bh = bbox[2], bbox[3]
    aspect = bw / bh  # 徽标内容宽高比(约 1.9)
    M = 60.0          # 画布外边距

    if layout == "below":
        EW = 1000.0
        EH = EW / aspect
        fs = EW * 0.235          # 字号
        gap = EW * 0.07          # 徽标与字的间距
        cap = fs * 0.72          # 大写高度近似
        CW = EW + 2 * M
        CH = M + EH + gap + cap + M
        ex = M
        ey = M
        body = nested_emblem(inner, bbox, ex, ey, EW, EH)
        tx = CW / 2.0
        ty = M + EH + gap + cap   # 基线
        body += text_el(text, tx, ty, fs, font, anchor="middle")

    elif layout == "right":
        EH = 560.0
        EW = EH * aspect
        fs = EH * 0.62
        gap = EH * 0.16
        cap = fs * 0.72
        # 估算字宽(Avenir Next bold ~0.53em/字 + 字距),用于画布宽度;略宽无妨(透明留白)
        tw = len(text) * fs * 0.53
        CW = M + EW + gap + tw + M
        CH = M + max(EH, cap) + M
        ex = M
        ey = (CH - EH) / 2.0
        body = nested_emblem(inner, bbox, ex, ey, EW, EH)
        tx = M + EW + gap
        ty = CH / 2.0 + cap / 2.0  # 垂直居中基线
        body += text_el(text, tx, ty, fs, font, anchor="start")
    else:
        sys.exit(f"未知 layout: {layout}")

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(CW)} {f(CH)}" '
        f'width="{f(CW)}" height="{f(CH)}">{body}</svg>'
    )
    return svg, CW, CH


def rasterize(svg_path, png_path, w, h):
    rsvg = shutil.which("rsvg-convert")
    if not rsvg:
        sys.exit("找不到 rsvg-convert(brew install librsvg)。")
    subprocess.run([rsvg, "-w", str(w), "-h", str(h), "-o", png_path, svg_path], check=True)


def main():
    ap = argparse.ArgumentParser(description="生成 Kairos 旭日字标锁版(下方/右侧)")
    ap.add_argument("--layout", choices=["below", "right", "both"], default="both")
    ap.add_argument("--text", default="Kairos", help="字标文字(默认 Kairos)")
    ap.add_argument("--uppercase", action="store_true", help="转大写 KAIROS")
    ap.add_argument("--font", default="Avenir Next", help="字体族(默认 Avenir Next)")
    ap.add_argument("--widths", default="2048,1024,512", help="逗号分隔的 PNG 宽度")
    ap.add_argument("--out-dir", default=OUT_DIR, dest="out_dir")
    a = ap.parse_args()

    text = a.text.upper() if a.uppercase else a.text
    layouts = ["below", "right"] if a.layout == "both" else [a.layout]
    widths = [int(s) for s in a.widths.split(",") if s.strip()]
    os.makedirs(a.out_dir, exist_ok=True)
    p = emblem_params()

    for layout in layouts:
        svg, CW, CH = build_lockup(layout, text, a.font, p)
        name = f"sunrise_{layout}"
        svg_path = os.path.join(a.out_dir, f"{name}.svg")
        with open(svg_path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        print(f"[svg] {svg_path}  ({CW:.0f}x{CH:.0f}, 字={text!r}, 字体={a.font})")
        for w in widths:
            h = round(w * CH / CW)
            png_path = os.path.join(a.out_dir, f"{name}_{w}.png")
            rasterize(svg_path, png_path, w, h)
            kb = os.path.getsize(png_path) // 1024
            print(f"  ✔ {w}x{h} -> {png_path}  ({kb} KB)")


if __name__ == "__main__":
    main()
