#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kairos logo 生成器。零依赖(标准库 REST) -> Gemini 图像模型(Nano Banana Pro = gemini-3-pro-image)。
风格 = BGB 白皮书的 3D 玻璃/金属质感 + 币安金(#F0B90B/#FCD535),纯黑底,无 cyan。

用法:
  python3 tools/gen_logo.py                 # 生成全部概念
  python3 tools/gen_logo.py --only hourglass # 只生成某个概念
  python3 tools/gen_logo.py --list           # 列出概念

输出 -> wiki/品牌/logo/<concept>.png
Key: 从 项目根/.env 的 GEMINI_API 读(或环境变量 GEMINI_API / GEMINI_API_KEY)。
"""
import argparse, base64, json, os, sys, urllib.request, urllib.error

API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT, ".env")
OUT_DIR = os.path.join(ROOT, "wiki", "品牌", "logo")
MODEL = os.environ.get("GA_MODEL", "gemini-3-pro-image")

# 统一风格底子(每个 prompt 都会拼上)
STYLE = (
    "Photorealistic 3D render on a pure black (#0B0B0B) background. "
    "Materials: polished metallic gold and translucent amber-gold glass with subtle "
    "iridescent chromatic dispersion at the edges. Premium studio lighting, strong "
    "specular highlights, soft mirror reflection on a glossy black floor, shallow depth "
    "of field, object floating and centered with generous negative space. "
    "Binance golden-yellow palette: base #F0B90B, bright highlight #FCD535, deep shadow #B8860B. "
    "STRICTLY no cyan, no blue, no teal, no green. Minimalist, premium, futuristic crypto brand. "
    "Clean, no extra text, no watermark."
)

CONCEPTS = {
    # 概念1:沙漏(kairos=关键时刻),最贴题
    "hourglass": (
        "A single sleek 3D hourglass as a crypto brand icon. The hourglass frame is polished "
        "metallic gold; the two bulbs are transparent glass with iridescent edge dispersion; "
        "glowing golden sand streams through the narrow center. Sense of a fleeting, decisive moment. "
        + STYLE
    ),
    # 概念2:「K」3D 金币/代币(呼应 BGB 那枚 3D coin)
    "k-coin": (
        "A single 3D crypto coin/token tilted in a 3/4 view, as a brand icon. The coin is polished "
        "metallic gold with a translucent amber-gold glass rim showing iridescent dispersion; a bold "
        "embossed capital letter 'K' on its face, clean geometric sans-serif. "
        + STYLE
    ),
    # 概念3:额前发绺 / 疾风时刻感(Kairos 神典故:抓住稍纵即逝的额发)
    "seize": (
        "A single abstract 3D emblem symbolizing seizing a fleeting moment: a sleek forward-swept "
        "wing / forelock shape merged with an upward motion arrow, dynamic and fast, as a brand icon. "
        "Polished metallic gold with translucent glass and iridescent dispersion. "
        + STYLE
    ),
    # 概念4:旭日/放射光芒(参照 raw/参考/logoReferences 的 sunburst 母题)
    "sunrise": (
        "A single 3D emblem of a stylized rising sun over a horizon line, with clean radiating rays "
        "fanning upward like a sunburst, as a premium crypto brand icon (inspired by a minimalist "
        "rising-sun mark). Symbolizing dawn and the decisive moment. Polished metallic gold with "
        "translucent glass rays showing subtle iridescent dispersion, contained in a soft rounded "
        "emblem silhouette. "
        + STYLE
    ),
    # 字标锁版:KAIROS wordmark + 小图标
    "wordmark": (
        "A 3D brand logo lockup for a Web3 prediction-market platform named KAIROS. A bold uppercase "
        "wordmark spelling exactly 'KAIROS' in a modern geometric sans-serif, rendered in polished "
        "metallic gold with bright gold highlights and subtle glass iridescence, with a small 3D gold "
        "hourglass icon immediately to its left. Horizontal lockup, perfectly legible letters. "
        + STYLE
    ),
}


def load_key():
    for v in ("GEMINI_API", "GEMINI_API_KEY"):
        if os.environ.get(v):
            return os.environ[v].strip()
    if os.path.isfile(ENV_PATH):
        with open(ENV_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit(f"找不到 API key:环境变量未设,且 {ENV_PATH} 内无 GEMINI_API")


def generate(key, prompt, aspect):
    url = f"{API_ROOT}/{MODEL}:generateContent?key={key}"
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": aspect}}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=300) as resp:
        payload = json.load(resp)
    for part in payload.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            return base64.b64decode(inline["data"])
    raise RuntimeError(f"无图片返回: {json.dumps(payload)[:500]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="只生成某个概念名")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        for k in CONCEPTS:
            print(k)
        return
    key = load_key()
    os.makedirs(OUT_DIR, exist_ok=True)
    todo = {a.only: CONCEPTS[a.only]} if a.only else CONCEPTS
    for name, prompt in todo.items():
        aspect = "16:9" if name == "wordmark" else "1:1"
        out = os.path.join(OUT_DIR, f"{name}.png")
        print(f"[{name}] {MODEL} {aspect} -> {out}")
        try:
            img = generate(key, prompt, aspect)
            with open(out, "wb") as f:
                f.write(img)
            print(f"  ✔ {len(img)//1024} KB")
        except urllib.error.HTTPError as e:
            print(f"  x HTTP {e.code}: {e.read().decode('utf-8','ignore')[:300]}")
        except Exception as e:
            print(f"  ✗ {e}")


if __name__ == "__main__":
    main()
