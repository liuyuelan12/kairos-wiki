#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kairos 旭日(Sunrise)logo —— 扁平矢量版。零依赖(纯标准库)生成参数化 SVG,再栅格化成透明 PNG。
复刻 raw/参考/logoReferences/2.png 的母题:地平线 + 半圆太阳 + ~13 条向上放射尖刺,
但配色改用币安金(默认金色渐变 #FCD535→#F0B90B→#B8860B),只要图标、无文字、透明底。

用法:
  python3 tools/gen_logo_sunrise.py                  # 默认:金色渐变,出 SVG + 2048/512/256/64 PNG
  python3 tools/gen_logo_sunrise.py --flat           # 单色平涂 #F0B90B
  python3 tools/gen_logo_sunrise.py --rays 13 --sun-radius 150 --ray-outer 430
  python3 tools/gen_logo_sunrise.py --sizes 1024,512 # 自定义 PNG 尺寸

输出 -> wiki/品牌/logo/sunrise_flat.svg + sunrise_flat_<size>.png
栅格器:优先 rsvg-convert(librsvg),缺失则回退 cairosvg;两者皆无则报错并提示安装。
"""
import argparse, math, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "wiki", "品牌", "logo")

# 币安金渐变(顶高光→中→暗),与 wiki/品牌/视觉风格.md 一致
GOLD_TOP, GOLD_MID, GOLD_BOT = "#FCD535", "#F0B90B", "#B8860B"
GOLD_FLAT = "#F0B90B"


def polar(cx, cy, r, deg):
    """极坐标 -> SVG 坐标(y 向下,故 sin 取负让角度向上)。deg=0 指向右,90 指向正上。"""
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy - r * math.sin(a))


def fmt(x):
    return f"{x:.2f}"


def build_svg(p):
    """按参数生成旭日 SVG 字符串。"""
    W = p.size
    cx = W / 2.0
    ray_outer = p.ray_outer
    # 垂直居中:绘制内容从 (horizon_y - ray_outer) 到 horizon_y,使其包围盒中点对齐画布中心
    horizon_y = W / 2.0 + ray_outer / 2.0

    fill = "url(#gold)"  # 渐变;flat 模式下改为纯色
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" '
        f'width="{W}" height="{W}">'
    )
    # 渐变(userSpaceOnUse,纵向覆盖整个旭日,使各元素色带连续)
    if not p.flat:
        y_top = horizon_y - ray_outer
        parts.append(
            f'<defs><linearGradient id="gold" gradientUnits="userSpaceOnUse" '
            f'x1="{fmt(cx)}" y1="{fmt(y_top)}" x2="{fmt(cx)}" y2="{fmt(horizon_y)}">'
            f'<stop offset="0" stop-color="{GOLD_TOP}"/>'
            f'<stop offset="0.55" stop-color="{GOLD_MID}"/>'
            f'<stop offset="1" stop-color="{GOLD_BOT}"/>'
            f'</linearGradient></defs>'
        )
    else:
        fill = GOLD_FLAT

    parts.append(f'<g fill="{fill}" stroke="none">')

    # 放射尖刺:span_start..span_end 等角分布,每条三角形尖端朝外、根部稍宽
    n = p.rays
    if n > 1:
        step = (p.span_end - p.span_start) / (n - 1)
    else:
        step = 0
    for i in range(n):
        theta = p.span_start + step * i
        tip = polar(cx, horizon_y, ray_outer, theta)
        b1 = polar(cx, horizon_y, p.ray_inner, theta - p.ray_half_w)
        b2 = polar(cx, horizon_y, p.ray_inner, theta + p.ray_half_w)
        pts = " ".join(fmt(v) for pt in (tip, b1, b2) for v in pt)
        parts.append(f'<polygon points="{pts}"/>')

    # 半圆太阳(上半圆,平边压在地平线上);sweep-flag=0 使弧线向上鼓
    R = p.sun_radius
    parts.append(
        f'<path d="M {fmt(cx - R)} {fmt(horizon_y)} '
        f'A {fmt(R)} {fmt(R)} 0 0 1 {fmt(cx + R)} {fmt(horizon_y)} Z"/>'
    )

    # 地平线:横向圆角条,居中于 horizon_y,略宽于太阳
    bar_hw = p.sun_radius + p.horizon_extra
    bar_h = p.horizon_thick
    parts.append(
        f'<rect x="{fmt(cx - bar_hw)}" y="{fmt(horizon_y - bar_h / 2)}" '
        f'width="{fmt(2 * bar_hw)}" height="{fmt(bar_h)}" '
        f'rx="{fmt(bar_h / 2)}" ry="{fmt(bar_h / 2)}"/>'
    )

    parts.append("</g></svg>")
    return "\n".join(parts)


def rasterize(svg_path, png_path, size):
    """SVG -> 透明 PNG。优先 rsvg-convert,回退 cairosvg。"""
    rsvg = shutil.which("rsvg-convert")
    if rsvg:
        subprocess.run(
            [rsvg, "-w", str(size), "-h", str(size), "-o", png_path, svg_path],
            check=True,
        )
        return "rsvg-convert"
    try:
        import cairosvg
    except ImportError:
        sys.exit(
            "找不到栅格器:请装 rsvg-convert(apt install librsvg2-bin)或 cairosvg(pip install cairosvg)。"
        )
    cairosvg.svg2png(
        url=svg_path, write_to=png_path, output_width=size, output_height=size
    )
    return "cairosvg"


def main():
    ap = argparse.ArgumentParser(description="生成扁平矢量旭日 logo(SVG + 透明 PNG)")
    ap.add_argument("--rays", type=int, default=13, help="放射尖刺数(默认 13)")
    ap.add_argument("--size", type=int, default=1024, help="SVG viewBox 边长")
    ap.add_argument("--sun-radius", type=float, default=150.0, dest="sun_radius")
    ap.add_argument("--ray-inner", type=float, default=172.0, dest="ray_inner",
                    help="尖刺根部半径(应略大于 sun-radius)")
    ap.add_argument("--ray-outer", type=float, default=430.0, dest="ray_outer",
                    help="尖刺尖端半径")
    ap.add_argument("--ray-half-w", type=float, default=4.0, dest="ray_half_w",
                    help="单条尖刺根部的角半宽(度)")
    ap.add_argument("--span-start", type=float, default=8.0, dest="span_start",
                    help="尖刺扇形起始角(度,贴地平线之上)")
    ap.add_argument("--span-end", type=float, default=172.0, dest="span_end")
    ap.add_argument("--horizon-thick", type=float, default=30.0, dest="horizon_thick")
    ap.add_argument("--horizon-extra", type=float, default=200.0, dest="horizon_extra",
                    help="地平线条相对太阳两侧各延伸的额外宽度")
    grp = ap.add_mutually_exclusive_group()
    grp.add_argument("--flat", action="store_true", help="单色平涂 #F0B90B")
    grp.add_argument("--gradient", dest="flat", action="store_false",
                     help="金色渐变(默认)")
    ap.set_defaults(flat=False)
    ap.add_argument("--sizes", default="2048,512,256,64",
                    help="逗号分隔的 PNG 输出尺寸")
    ap.add_argument("--out-dir", default=OUT_DIR, dest="out_dir")
    ap.add_argument("--name", default="sunrise_flat", help="输出文件名前缀")
    p = ap.parse_args()

    os.makedirs(p.out_dir, exist_ok=True)
    svg = build_svg(p)
    svg_path = os.path.join(p.out_dir, f"{p.name}.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    mode = "flat" if p.flat else "gradient"
    print(f"[svg] {svg_path}  ({p.rays} 尖刺, {mode})")

    sizes = [int(s) for s in p.sizes.split(",") if s.strip()]
    for s in sizes:
        png_path = os.path.join(p.out_dir, f"{p.name}_{s}.png")
        engine = rasterize(svg_path, png_path, s)
        kb = os.path.getsize(png_path) // 1024
        print(f"  ✔ {s:>5}px -> {png_path}  ({kb} KB, {engine})")


if __name__ == "__main__":
    main()
