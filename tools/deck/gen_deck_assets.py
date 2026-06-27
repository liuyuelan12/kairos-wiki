#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kairos Deck v2 3D 素材（Gemini / Nano Banana Pro）。币安金玻璃/金属 + 微 cyan 冷光，纯黑底。
关键：强制 IPv4（绕过本网络 IPv6 路径的 geo-block）+ 重试多次（代理出口节点部分被封）。
封面用 sunrise logo 作参考图保持品牌一致。
用法: python3 tools/deck/gen_deck_assets.py [--only cover-hero] [--force]
"""
import base64, json, os, socket, sys, time, urllib.request, urllib.error

# 强制 IPv4
_gai = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: _gai(h, p, socket.AF_INET, t, pr, fl)

API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models"
MODEL = os.environ.get("GA_MODEL", "gemini-3-pro-image")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV = os.path.join(ROOT, ".env")
REF = os.path.join(ROOT, "wiki", "品牌", "logo", "sunrise_flat_512.png")
OUTDIR = os.path.join(ROOT, "output", "deck-assets")

BASE = ("Photoreal 3D product render, glossy glass / iridescent material, Binance golden-yellow "
        "#F0B90B and #FCD535 as the dominant accent and rim light, with only a subtle secondary "
        "CYAN edge glow, deep PURE BLACK background, premium fintech whitepaper style, studio "
        "lighting, soft reflections, octane look. NO text, NO words, NO labels.")

# name -> (aspect, use_ref, prompt)
ASSETS = {
    "cover-hero.png": ("16:9", True,
        "Crypto whitepaper COVER hero. A large floating IRIDESCENT GLASS sphere emblem with a glowing "
        "golden RISING-SUN / radiating-rays motif inside (silhouette matching the provided rising-sun "
        "mark), clear acrylic with chromatic dispersion and a bright GOLD inner glow; beside it a glossy "
        "metallic gold coin tilted in space with faint gold energy trails. Leave the LEFT THIRD darker / "
        "emptier for a title. " + BASE),
    "icon-rwa.png": ("1:1", False,
        "A 3D glossy icon of a translucent globe wrapped with small floating event tags and data nodes, "
        "representing real-world events turned into tradable assets. " + BASE),
    "icon-oracle.png": ("1:1", False,
        "A 3D glossy icon of a checkmark inside a shield with a subtle eye motif, representing verifiable "
        "oracle settlement and proof. " + BASE),
    "icon-ai.png": ("1:1", False,
        "A 3D glossy icon of a glowing neural-network brain fused with a microchip, representing an AI "
        "engine. " + BASE),
    "icon-local.png": ("1:1", False,
        "A 3D glossy icon of a map location pin merged with a small globe and chat bubbles, representing "
        "localization and multi-language reach. " + BASE),
    "donut-gold.png": ("1:1", False,
        "A glossy 3D DONUT / torus chart, slight top-down tilt, divided into 4 unequal segments by thin "
        "dark gaps. ONE large segment (~50%) is bright glowing GOLD glass; the other three are dark "
        "graphite-gold glass with faint gold edges, decreasing in size. Hollow center and surrounding "
        "area EMPTY pure black for overlaying labels later. Centered. " + BASE),
}


def load_key():
    for v in ("GEMINI_API", "GEMINI_API_KEY"):
        if os.environ.get(v):
            return os.environ[v].strip()
    for line in open(ENV, encoding="utf-8"):
        if line.strip().startswith("GEMINI_API="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("no GEMINI_API")


def image_part(path):
    with open(path, "rb") as f:
        return {"inlineData": {"mimeType": "image/png", "data": base64.b64encode(f.read()).decode()}}


def generate(key, aspect, parts, out, tries=45):
    url = f"{API_ROOT}/{MODEL}:generateContent?key={key}"
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}}
    data = json.dumps(body).encode(); last = ""
    for attempt in range(1, tries + 1):
        try:
            req = urllib.request.Request(url, data=data,
                                         headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=300) as resp:
                payload = json.load(resp)
            for part in payload.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and inline.get("data"):
                    img = base64.b64decode(inline["data"])
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    with open(out, "wb") as f:
                        f.write(img)
                    print(f"  ✔ {os.path.basename(out)} ({len(img)//1024} KB, try {attempt})", flush=True)
                    return True
            last = "no image"
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode('utf-8','ignore')[:90]}"
        except Exception as e:
            last = str(e)[:90]
        print(f"  · retry {attempt}/{tries} — {last[:74]}", flush=True)
        time.sleep(4)
    print(f"  ✗ {os.path.basename(out)} failed: {last[:110]}")
    return False


def main():
    only = None; force = "--force" in sys.argv
    for a in sys.argv[1:]:
        if a == "--only":
            continue
        if not a.startswith("--"):
            only = a
    key = load_key()
    for name, (aspect, use_ref, prompt) in ASSETS.items():
        if only and only not in name:
            continue
        dest = os.path.join(OUTDIR, name)
        if os.path.isfile(dest) and not force:
            print(f"skip {name} (exists)"); continue
        parts = ([image_part(REF)] if use_ref and os.path.isfile(REF) else []) + [{"text": prompt}]
        print(f"generating {name} [{aspect}] ref={use_ref}", flush=True)
        generate(key, aspect, parts, dest)


if __name__ == "__main__":
    main()
