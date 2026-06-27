#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kairos logo 生成器。零依赖(标准库 REST) -> Gemini 图像模型(Nano Banana Pro = gemini-3-pro-image)。
风格 = BGB 白皮书的 3D 玻璃/金属质感 + 币安金(#F0B90B/#FCD535),纯黑底,无 cyan。

用法:
  python3 tools/gen_logo.py                 # 生成全部概念
  python3 tools/gen_logo.py --only hourglass # 只生成某个概念
  python3 tools/gen_logo.py --list           # 列出概念
  # 喂参考图条件生成 + 透明底(不透明则回退黑底):
  python3 tools/gen_logo.py --only sunrise --ref raw/参考/logoReferences/2.png

输出 -> wiki/品牌/logo/<concept>.png
Key: 从 项目根/.env 的 GEMINI_API 读(或环境变量 GEMINI_API / GEMINI_API_KEY)。
"""
import argparse, base64, json, os, sys, urllib.request, urllib.error

API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT, ".env")
OUT_DIR = os.path.join(ROOT, "wiki", "品牌", "logo")
MODEL = os.environ.get("GA_MODEL", "gemini-3-pro-image")

# 共用的材质/配色约束(黑底版与透明版都拼它)
_CORE = (
    "Materials: polished metallic gold and translucent amber-gold glass with subtle "
    "iridescent chromatic dispersion at the edges. Premium studio lighting, strong "
    "specular highlights, shallow depth of field, object centered with generous negative space. "
    "Binance golden-yellow palette: base #F0B90B, bright highlight #FCD535, deep shadow #B8860B. "
    "STRICTLY no cyan, no blue, no teal, no green. Minimalist, premium, futuristic crypto brand. "
    "Clean, no extra text, no watermark."
)

# 统一风格底子(每个 prompt 都会拼上)——黑底版(默认/回退用)
STYLE = (
    "Photorealistic 3D render on a pure black (#0B0B0B) background, "
    "soft mirror reflection on a glossy black floor, object floating. " + _CORE
)

# 透明底版:抠像式输出,无背景、无地面反射。模型若不支持透明会返回不透明图 -> 调用方回退黑底。
STYLE_TRANSPARENT = (
    "Photorealistic 3D render of the subject in isolation on a fully TRANSPARENT background "
    "(alpha channel, no backdrop, no floor, no shadow on ground), as a cut-out PNG sticker. " + _CORE
)

# 每个概念只存「主体描述」,风格(黑底/透明)在出图时再拼,便于切换。
CONCEPTS = {
    # 概念1:沙漏(kairos=关键时刻),最贴题
    "hourglass": (
        "A single sleek 3D hourglass as a crypto brand icon. The hourglass frame is polished "
        "metallic gold; the two bulbs are transparent glass with iridescent edge dispersion; "
        "glowing golden sand streams through the narrow center. Sense of a fleeting, decisive moment. "
    ),
    # 概念2:「K」3D 金币/代币(呼应 BGB 那枚 3D coin)
    "k-coin": (
        "A single 3D crypto coin/token tilted in a 3/4 view, as a brand icon. The coin is polished "
        "metallic gold with a translucent amber-gold glass rim showing iridescent dispersion; a bold "
        "embossed capital letter 'K' on its face, clean geometric sans-serif. "
    ),
    # 概念3:额前发绺 / 疾风时刻感(Kairos 神典故:抓住稍纵即逝的额发)
    "seize": (
        "A single abstract 3D emblem symbolizing seizing a fleeting moment: a sleek forward-swept "
        "wing / forelock shape merged with an upward motion arrow, dynamic and fast, as a brand icon. "
        "Polished metallic gold with translucent glass and iridescent dispersion. "
    ),
    # 概念4:旭日/放射光芒——复刻参考图 raw/参考/logoReferences/2.png 的构图(配 --ref 喂图最佳)
    "sunrise": (
        "A premium 3D crypto brand emblem of a rising sun, matching this exact composition: a solid "
        "SEMI-CIRCLE sun (half disk) resting on a horizontal HORIZON line, with about 13 sharp "
        "triangular RAYS fanning upward in a ~180-degree sunburst above the sun (tips pointing "
        "outward, never crossing below the horizon). Reproduce the silhouette of a classic minimalist "
        "rising-sun mark, but rendered as polished metallic gold with translucent amber-gold glass "
        "edges and subtle iridescent dispersion. Symbolizing dawn and the decisive moment. No text. "
    ),
    # 字标锁版:KAIROS wordmark + 小图标
    "wordmark": (
        "A 3D brand logo lockup for a Web3 prediction-market platform named KAIROS. A bold uppercase "
        "wordmark spelling exactly 'KAIROS' in a modern geometric sans-serif, rendered in polished "
        "metallic gold with bright gold highlights and subtle glass iridescence, with a small 3D gold "
        "hourglass icon immediately to its left. Horizontal lockup, perfectly legible letters. "
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


def _mime_for(path):
    ext = os.path.splitext(path)[1].lower()
    return {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".webp": "image/webp"}.get(ext, "image/png")


def load_ref(path):
    """读参考图 -> (base64 字符串, mime)。用于喂图条件生成。"""
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode(), _mime_for(path)


def image_has_alpha(data):
    """是否带透明通道。仅 PNG 的 IHDR color type 6(RGBA)/4(灰+α) 视为透明;JPEG 等永远不透明。"""
    if len(data) >= 26 and data[:8] == b"\x89PNG\r\n\x1a\n":
        return data[25] in (4, 6)  # IHDR color-type 字节
    return False


def ext_for(data):
    """按真实魔数给扩展名,避免把 JPEG 存成 .png。"""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if data[:3] == b"\xff\xd8\xff":
        return "jpg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return "png"


def generate(key, prompt, aspect, ref=None, retries=3):
    """出图,返回原始字节。ref=(b64, mime) 时把参考图作为 inlineData 与文本一起喂入(图文条件生成)。
    大图响应偶发 IncompleteRead/网络抖动 -> 重试。"""
    url = f"{API_ROOT}/{MODEL}:generateContent?key={key}"
    parts = [{"text": prompt}]
    if ref:
        parts.append({"inlineData": {"mimeType": ref[1], "data": ref[0]}})
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": aspect}}}
    last = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=300) as resp:
                payload = json.load(resp)
            for part in payload.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and inline.get("data"):
                    return base64.b64decode(inline["data"])
            raise RuntimeError(f"无图片返回: {json.dumps(payload)[:500]}")
        except urllib.error.HTTPError:
            raise  # HTTP 错误直接抛,交给上层打印
        except Exception as e:
            last = e
            if attempt < retries:
                print(f"  · 网络抖动({type(e).__name__}),重试 {attempt}/{retries-1}")
    raise last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="只生成某个概念名")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--ref", help="参考图路径(喂图条件生成,如 raw/参考/logoReferences/2.png)")
    ap.add_argument("--transparent", action="store_true",
                    help="请求透明底;若模型返回不透明图则自动回退黑底重出")
    a = ap.parse_args()
    if a.list:
        for k in CONCEPTS:
            print(k)
        return
    key = load_key()
    ref = load_ref(a.ref) if a.ref else None
    if a.ref:
        print(f"[ref] {a.ref}")
    os.makedirs(OUT_DIR, exist_ok=True)
    todo = {a.only: CONCEPTS[a.only]} if a.only else CONCEPTS
    for name, body in todo.items():
        aspect = "16:9" if name == "wordmark" else "1:1"
        print(f"[{name}] {MODEL} {aspect}{' +ref' if ref else ''}{' +transparent' if a.transparent else ''}")
        try:
            style = STYLE_TRANSPARENT if a.transparent else STYLE
            img = generate(key, body + style, aspect, ref=ref)
            # 透明回退:要透明却拿到不透明图(本模型常返回 JPEG)-> 用黑底版重出一张(满足「不透明则回退黑底」)
            if a.transparent and not image_has_alpha(img):
                print("  ! 返回图不透明 -> 回退黑底重出")
                img = generate(key, body + STYLE, aspect, ref=ref)
            ext = ext_for(img)  # 按真实格式存扩展名,JPEG 不会被冒充成 .png
            tag = "透明" if image_has_alpha(img) else "不透明(黑底)"
            out = os.path.join(OUT_DIR, f"{name}.{ext}")
            with open(out, "wb") as f:
                f.write(img)
            print(f"  ✔ {len(img)//1024} KB ({tag}) -> {out}")
        except urllib.error.HTTPError as e:
            print(f"  x HTTP {e.code}: {e.read().decode('utf-8','ignore')[:300]}")
        except Exception as e:
            print(f"  ✗ {e}")


if __name__ == "__main__":
    main()
