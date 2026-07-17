"""
Minimal, standalone test -- NOT part of the main app. Its only purpose is to
answer one question on a real Linux host (Render's free tier): can Pillow's
bundled text-shaping library correctly join the Pashto-only letters
(ت ډ ړ ږ ښ ګ ڼ ځ څ) that Windows' GDI+ handles correctly but a simpler
reshaping approach (arabic_reshaper) was confirmed NOT to handle?

If this renders correctly, the main app's image-translation feature can be
ported off GDI+ for Linux hosting. If not, we know that early and cheaply,
before investing in a bigger port.
"""
from flask import Flask, Response
from PIL import Image, ImageDraw, ImageFont, features
import io
import os

app = Flask(__name__)

# Bundled directly with the app (Noto Naskh Arabic, open-source/OFL-licensed)
# rather than relying on whatever fonts happen to be preinstalled on the
# host -- guarantees the test isn't confounded by a missing/different font.
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "NotoNaskhArabic.ttf")

# Every Pashto-only letter without a Unicode presentation form, per
# gdiplus_text.py's own docstring -- the exact set that broke before.
TEST_WORDS = [
    "ټولنه",   # tolana (society) -- ټ
    "ډاکټر",   # daktar (doctor) -- ډ
    "زړه",     # zra (heart) -- ړ
    "غږ",      # ghagh (voice) -- ږ
    "ښځه",     # khza (woman) -- ښ
    "ګل",      # gul (flower) -- ګ
    "زڼی",     # -- ڼ
    "ځای",     # zaay (place) -- ځ
    "څوک",     # tsok (who) -- څ
]

@app.route("/")
def index():
    info = (
        f"Pillow raqm feature available: {features.check_feature('raqm')}<br>"
        f"Pillow raqm version: {features.version_feature('raqm')}<br>"
        f"Font exists: {os.path.exists(FONT_PATH)}<br>"
        f'<img src="/render" style="border:1px solid #ccc; background:white;"><br>'
        f'<img src="/render_basic" style="border:1px solid #ccc; background:white;">'
        f"<br>(top image = RAQM/HarfBuzz shaping, bottom = BASIC/no shaping, for comparison)"
    )
    return info


def _render(layout_engine):
    font = ImageFont.truetype(FONT_PATH, 48, layout_engine=layout_engine)
    img = Image.new("RGB", (500, 40 + 60 * len(TEST_WORDS)), "white")
    draw = ImageDraw.Draw(img)
    for i, word in enumerate(TEST_WORDS):
        draw.text((20, 10 + i * 55), word, font=font, fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@app.route("/render")
def render():
    return Response(_render(ImageFont.Layout.RAQM), mimetype="image/png")


@app.route("/render_basic")
def render_basic():
    return Response(_render(ImageFont.Layout.BASIC), mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
