"""lib_video.py — boîte à outils des Shorts 1jour1histoire (1080x1920, 30 fps).

Usage dans un script d'épisode :
    import sys; sys.path.insert(0, PIPELINE_DIR)
    from lib_video import *
    ep = Episode(EP_DIR, title="LA GUERRE DES ÉMEUS", badge="ÉP. 3")
    ... définir build() (remplit le dict A) et les scènes S_xxx(t, t0, t1) -> (img_rgba, zoom, shake)
    SC = [(S_hook, 0.0, ep.L(2)), ..., (S_end, ep.L(n), ep.TOTAL)]
    if __name__ == "__main__": ep.main(SC, build)
Commandes : python3 episode.py stills 1.5 7.2 ...   |   python3 episode.py video 0 2 4 ...   |   python3 episode.py render (tout, en 2 processus)
"""
import json, math, os, random, subprocess, sys, glob, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageOps

W, H, FPS = 1080, 1920, 30
GOLD = (255, 214, 10); RED = (206, 32, 45); GREEN = (40, 170, 70); WHITE = (255, 255, 255)
FONT_DIR = os.environ.get("FONT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts"))

def _find_font(pattern):
    hits = glob.glob(os.path.join(FONT_DIR, "**", pattern), recursive=True)
    if not hits: raise FileNotFoundError(f"police introuvable: {pattern} dans {FONT_DIR} (lancer setup.sh)")
    return hits[0]
FONTS = {
    "anton": "anton-latin-400-normal.woff",
    "type": "special-elite-latin-400-normal.woff",
    "serif": "playfair-display-latin-900-normal.woff",
    "serifr": "playfair-display-latin-400-normal.woff",
}
_fc = {}
def F(name, size):
    k = (name, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(_find_font(FONTS[name]), size)
    return _fc[k]

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, d): return clamp((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)
def ease_out(p): return 1 - (1 - p) ** 3
def ease_back(p):
    c1 = 1.9; c3 = c1 + 1
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2

# ---------- backgrounds ----------
def vgrad(w, h, top, bot):
    a = np.linspace(0, 1, h)[:, None, None]
    top = np.array(top, np.float32); bot = np.array(bot, np.float32)
    return Image.fromarray((top * (1 - a) + bot * a).repeat(w, axis=1).astype(np.uint8), "RGB")

_vig = None
def vignette(img, strength=0.65):
    """img doit faire W x H."""
    global _vig
    if _vig is None:
        y, x = np.mgrid[0:H, 0:W]
        d = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H / 2) / (H * 0.58)) ** 2)
        _vig = np.clip(1 - (d ** 2.2) * 0.9, 0, 1)
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    m = 1 - strength + strength * _vig
    return Image.fromarray((arr * m[..., None]).clip(0, 255).astype(np.uint8))

def full_grad(top, bot, strength=0.5):
    """Fond plein écran dégradé + vignette, en RGBA."""
    return vignette(vgrad(W, H, top, bot), strength).convert("RGBA")

def paper(tint=(226, 205, 160), seed=1):
    rng = np.random.default_rng(seed)
    base = np.ones((H, W, 3), np.float32) * np.array(tint, np.float32)
    n = rng.normal(0, 1, (H // 8, W // 8)).astype(np.float32)
    n = np.asarray(Image.fromarray(((n * 30) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) - 128
    base += (n * 0.5 + rng.normal(0, 7, (H, W)).astype(np.float32))[..., None]
    return vignette(Image.fromarray(base.clip(0, 255).astype(np.uint8)), 0.55).convert("RGBA")

def dark_bg(top, bot, glow=None):
    img = vgrad(W, H, top, bot).convert("RGBA")
    if glow:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.ellipse([W / 2 - 500, H / 2 - 600, W / 2 + 500, H / 2 + 400], fill=tuple(glow) + (120,))
        img = Image.alpha_composite(img, g.filter(ImageFilter.GaussianBlur(160)))
    return vignette(img, 0.7).convert("RGBA")

def map_bg(seed=9):
    img = paper((214, 196, 156), 5); d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(seed)
    for _ in range(8):
        x, y = rng.randint(100, 900), rng.randint(500, 1500)
        d.ellipse([x - rng.randint(120, 260), y - rng.randint(100, 220), x + rng.randint(120, 260), y + rng.randint(100, 220)], fill=(170, 150, 110, 70))
    for gx in range(0, W, 120): d.line([gx, 0, gx, H], fill=(120, 100, 70, 40), width=2)
    for gy in range(0, H, 120): d.line([0, gy, W, gy], fill=(120, 100, 70, 40), width=2)
    return img

def map_route(img, P1, P2, p, name1, name2, curve=260, color=RED):
    """Trajet pointillé animé (p de 0 à 1) entre deux points nommés. Renvoie la position courante."""
    d = ImageDraw.Draw(img)
    for (x, y), name in [(P1, name1), (P2, name2)]:
        d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=color)
        ctext(d, name, x, y + 70, F("anton", 76), (30, 22, 18))
    n = 40; pts = []
    for i in range(n + 1):
        s = i / n
        pts.append((P1[0] + (P2[0] - P1[0]) * s, P1[1] + (P2[1] - P1[1]) * s - math.sin(s * math.pi) * curve))
    k = int(n * clamp(p))
    for i in range(0, k, 2): d.line([pts[i], pts[i + 1]], fill=color, width=12)
    return pts[min(k, n)]

def waves(img, t, y0=1000, col=(255, 255, 255, 60)):
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(9):
        y = y0 + 40 + k * 95 + k * k * 4
        d.line([(x, y + math.sin(x / 60 + t * 2 + k) * (6 + k * 2)) for x in range(-20, W + 40, 40)], fill=col, width=3 + k // 2)

def rain(img, t, k=60, alpha=70):
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(k):
        x = (i * 173 + int(t * 300)) % (W + 200) - 100
        y = (i * 389 + int(t * 1900)) % (H + 300) - 300
        d.line([x, y, x - 18, y + 70], fill=(200, 230, 220, alpha), width=3)

# ---------- text / layers ----------
def ctext(d, txt, cx, y, font, fill, stroke=0, sfill=(0, 0, 0), anchor="mm", spacing=6):
    d.text((cx, y), txt, font=font, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill, align="center", spacing=spacing)

def shadow_paste(base, layer, xy, blur=18, off=(10, 16), alpha=150):
    a = layer.split()[-1]
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: v * alpha // 255))
    pad = blur * 3
    big = Image.new("RGBA", (layer.width + pad * 2, layer.height + pad * 2), (0, 0, 0, 0)); big.paste(sh, (pad, pad))
    big = big.filter(ImageFilter.GaussianBlur(blur))
    _comp(base, big, int(xy[0] - pad + off[0]), int(xy[1] - pad + off[1]))
    _comp(base, layer, int(xy[0]), int(xy[1]))

def _comp(base, L, x, y):
    """alpha_composite qui accepte des coordonnées négatives / hors cadre."""
    x0, y0 = max(0, x), max(0, y); x1, y1 = min(base.width, x + L.width), min(base.height, y + L.height)
    if x1 <= x0 or y1 <= y0: return
    base.alpha_composite(L.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))

def paste_center(base, layer, cx, cy, scale=1.0, rot=0.0, alpha=1.0, shadow=True):
    if scale <= 0.01 or alpha <= 0.01: return
    L = layer
    if scale != 1.0: L = L.resize((max(1, int(L.width * scale)), max(1, int(L.height * scale))), Image.BICUBIC)
    if rot: L = L.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1.0:
        L = L.copy(); L.putalpha(L.split()[-1].point(lambda v: int(v * alpha)))
    x, y = cx - L.width / 2, cy - L.height / 2
    if shadow: shadow_paste(base, L, (x, y), blur=14, off=(8, 14), alpha=int(140 * alpha))
    else: _comp(base, L, int(x), int(y))

def put_bottom(base, L, x, y):
    """Pose L avec son bas-centre en (x, y) (pratique pour des personnages au sol)."""
    _comp(base, L, int(x - L.width / 2), int(y - L.height))

def stamp_layer(text, color=RED, size=170, font="anton", seed=3, pad=40):
    f = F(font, size); bb = f.getbbox(text)
    w, h = int(bb[2] - bb[0] + pad * 2 + 30), int(bb[3] - bb[1] + pad * 2 + 10)
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    bw = max(8, size // 14)
    d.rounded_rectangle([bw, bw, w - bw, h - bw], radius=size // 8, outline=tuple(color) + (255,), width=bw)
    d.text((w / 2, h / 2), text, font=f, fill=tuple(color) + (255,), anchor="mm")
    rng = np.random.default_rng(seed)
    a = np.asarray(L.split()[-1]).astype(np.float32)
    blot = np.asarray(Image.fromarray((rng.random((h // 6 + 1, w // 6 + 1)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255
    a = a * (rng.random((h, w)) > 0.12) * (0.55 + 0.45 * (blot > 0.3))
    L.putalpha(Image.fromarray(a.clip(0, 255).astype(np.uint8)))
    return L

def card(w, h, fill=(244, 236, 216), radius=18, border=None):
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=tuple(fill) + (255,), outline=border, width=4 if border else 0)
    return L

def pill(text, fill=GOLD, tc=(20, 16, 14), size=80, padx=36, pady=18, font="anton"):
    f = F(font, size); bb = f.getbbox(text)
    w, h = int(bb[2] - bb[0] + padx * 2), int(size + pady * 2)
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 4, fill=tuple(fill) + (255,))
    d.text((w / 2, h / 2), text, font=f, fill=tc, anchor="mm")
    return L

def bigtext(text, size, fill, font="anton", stroke=10, sfill=(0, 0, 0), spacing=4):
    f = F(font, size)
    bb = ImageDraw.Draw(Image.new("RGBA", (10, 10))).multiline_textbbox((0, 0), text, font=f, stroke_width=stroke, align="center", spacing=spacing)
    w, h = int(bb[2] - bb[0] + 20), int(bb[3] - bb[1] + 20)
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.multiline_text((w / 2, h / 2), text, font=f, fill=tuple(fill) + (255,), anchor="mm", align="center", stroke_width=stroke, stroke_fill=tuple(sfill) + (255,), spacing=spacing)
    return L

def typed(text, t, t0, dur, size=150, color=(30, 22, 18), font="type"):
    """Texte qui s'écrit lettre par lettre (machine à écrire)."""
    n = int(len(text) * prog(t, t0, dur) + 0.999)
    return bigtext(text[:max(1, n)], size, color, font=font, stroke=0)

# ---------- silhouettes ----------
def man_layer(h, color=(14, 10, 14), cigar=False):
    """Homme en costume + chapeau (années 1900-1950)."""
    w = int(h * 0.95)
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L); cx = w / 2; c = tuple(color) + (255,)
    d.pieslice([cx - w * 0.5, h * 0.52, cx + w * 0.5, h * 1.5], 180, 360, fill=c)
    d.rectangle([cx - w * 0.5, h * 0.98, cx + w * 0.5, h], fill=c)
    d.polygon([(cx - w * 0.13, h * 0.56), (cx, h * 0.8), (cx + w * 0.13, h * 0.56)], fill=tuple(min(255, x + 22) for x in color) + (255,))
    d.rectangle([cx - w * 0.08, h * 0.42, cx + w * 0.08, h * 0.6], fill=c)
    d.ellipse([cx - w * 0.15, h * 0.2, cx + w * 0.15, h * 0.52], fill=c)
    d.ellipse([cx - w * 0.3, h * 0.215, cx + w * 0.3, h * 0.285], fill=c)
    d.rounded_rectangle([cx - w * 0.16, h * 0.08, cx + w * 0.16, h * 0.26], radius=int(w * 0.07), fill=c)
    d.rectangle([cx - w * 0.16, h * 0.205, cx + w * 0.16, h * 0.235], fill=(120, 30, 35, 255))
    if cigar:
        d.rectangle([cx + w * 0.1, h * 0.44, cx + w * 0.3, h * 0.465], fill=(110, 70, 40, 255))
        d.ellipse([cx + w * 0.29, h * 0.435, cx + w * 0.32, h * 0.47], fill=(255, 120, 40, 255))
    return L

def soldier_layer(h, color=(10, 14, 10), aged=False):
    """Soldat avec calot et fusil."""
    w = int(h * 0.95)
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L); cx = w / 2; c = tuple(color) + (255,)
    d.line([cx - w * 0.36, h * 0.98, cx + w * 0.3, h * 0.05], fill=c, width=int(w * 0.045))
    d.pieslice([cx - w * 0.48, h * 0.55, cx + w * 0.48, h * 1.5], 180, 360, fill=c)
    d.rectangle([cx - w * 0.48, h * 1.0 - 4, cx + w * 0.48, h], fill=c)
    d.rectangle([cx - w * 0.07, h * 0.44, cx + w * 0.07, h * 0.62], fill=c)
    d.ellipse([cx - w * 0.14, h * 0.24, cx + w * 0.14, h * 0.54], fill=c)
    d.chord([cx - w * 0.16, h * 0.16, cx + w * 0.16, h * 0.42], 180, 360, fill=c)
    d.polygon([(cx - w * 0.04, h * 0.29), (cx + w * 0.2, h * 0.29), (cx + w * 0.12, h * 0.33)], fill=c)
    if aged: d.chord([cx - w * 0.13, h * 0.38, cx + w * 0.13, h * 0.6], 0, 180, fill=c)
    return L

def woman_layer(h=700, col=(24, 20, 30), apron=True):
    """Femme en robe longue, chignon (début XXe)."""
    w = int(h * 0.8)
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = tuple(col) + (255,); cx = w / 2
    d.polygon([(cx - w * 0.2, h * 0.45), (cx + w * 0.2, h * 0.45), (cx + w * 0.45, h), (cx - w * 0.45, h)], fill=c)
    if apron: d.polygon([(cx - w * 0.12, h * 0.55), (cx + w * 0.12, h * 0.55), (cx + w * 0.2, h), (cx - w * 0.2, h)], fill=(240, 236, 226, 255))
    d.rectangle([cx - w * 0.05, h * 0.36, cx + w * 0.05, h * 0.47], fill=c)
    d.ellipse([cx - w * 0.13, h * 0.14, cx + w * 0.13, h * 0.4], fill=c)
    d.ellipse([cx - w * 0.1, h * 0.06, cx + w * 0.1, h * 0.2], fill=c)
    return L

# ---------- animation helpers ----------
def stamp_in(img, layer, t, ts, x, y, rot, big=1.5):
    """Tampon qui s'écrase à ts. Renvoie l'intensité de tremblement à passer en 3e valeur de la scène."""
    p = prog(t, ts, 0.18)
    if p <= 0: return 0
    paste_center(img, layer, x, y, scale=1 + big * (1 - ease_out(p)), rot=rot, alpha=min(1, p * 2))
    return clamp(1 - (t - ts - 0.18) / 0.25) if t > ts + 0.18 else 0

def pop_in(img, layer, t, ts, x, y, rot=0, scale=1.0):
    p = prog(t, ts, 0.3)
    if p > 0: paste_center(img, layer, x, y, scale=scale * ease_back(p), rot=rot)

def slide_in(img, layer, t, ts, x, y, dur=0.4, rot=0, from_dy=1100):
    paste_center(img, layer, x, y + (1 - ease_out(prog(t, ts, dur))) * from_dy, rot=rot)

# ---------- episode ----------
class Episode:
    def __init__(self, ep_dir, title, badge, cap_y=1420):
        self.dir = ep_dir
        tl = json.load(open(os.path.join(ep_dir, "timeline.json")))
        self.LINES = tl["lines"]; self.TOTAL = tl["total"]
        self.cap_y = cap_y
        self.CHUNKS = self._chunks()
        self.TITLE = self._title(title)
        self.BADGE = pill(badge, fill=GOLD, size=46, padx=22, pady=10)
        rng0 = np.random.default_rng(11)
        self.GRAIN = [Image.fromarray(rng0.normal(128, 22, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)).resize((W, H)).convert("RGB") for _ in range(4)]
        self.CAPF = F("anton", 92)

    def L(self, i): return self.LINES[i]["s"]
    def E(self, i): return self.LINES[i]["e"]
    def wt(self, line, sub):
        """Instant où commence le premier mot de la ligne `line` qui contient `sub` (insensible à la casse)."""
        for w in self.LINES[line]["words"]:
            if sub.lower() in w["w"].lower(): return w["s"]
        raise KeyError(f"'{sub}' absent de la ligne {line}: {[w['w'] for w in self.LINES[line]['words']]}")

    def _title(self, txt):
        f = F("anton", 66); bb = f.getbbox(txt); w = int(bb[2] - bb[0] + 60); h = 104
        L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=16, fill=RED + (255,))
        d.text((w / 2, h / 2 + 2), txt, font=f, fill=(255, 255, 255, 255), anchor="mm")
        return L

    def _chunks(self):
        chunks = []
        for L in self.LINES:
            ws = []
            for w in L["words"]:
                if w["w"] in (":", ",") and ws: ws[-1] = dict(ws[-1], w=ws[-1]["w"] + " " + w["w"]); continue
                ws.append(dict(w))
            cur = []
            for w in ws:
                cur.append(w)
                if len(cur) >= 3 or sum(len(x["w"]) for x in cur) >= 15 or w["w"].endswith((",", ".", ":")):
                    chunks.append(cur); cur = []
            if cur: chunks.append(cur)
        return chunks

    def draw_caption(self, img, t):
        ch = None
        for c in self.CHUNKS:
            if c[0]["s"] - 0.04 <= t <= c[-1]["e"] + 0.12: ch = c
        if ch is None: return
        d = ImageDraw.Draw(img); CAPF = self.CAPF
        words = [w["w"].upper().rstrip(".,") for w in ch]
        widths = [CAPF.getlength(x) for x in words]; sp = 26
        lines = [[0, len(words)]]
        if sum(widths) + sp * (len(words) - 1) > 880:
            k = len(words) // 2 + (1 if len(words) % 2 else 0); lines = [[0, k], [k, len(words)]]
        p = ease_back(prog(t, ch[0]["s"] - 0.04, 0.16))
        y0 = self.cap_y - (len(lines) - 1) * 55
        for li, (a, b) in enumerate(lines):
            lw = sum(widths[a:b]) + sp * (b - a - 1); x = W / 2 - lw / 2 - 20
            for j in range(a, b):
                w = ch[j]; active = w["s"] - 0.03 <= t <= w["e"] + 0.05 or (j == len(ch) - 1 and t > w["e"])
                d.text((x, y0 + li * 110 + (1 - p) * 30), words[j], font=CAPF, fill=GOLD if active else WHITE, anchor="lm", stroke_width=11, stroke_fill=(0, 0, 0))
                x += widths[j] + sp

    def finish(self, scene, t, zoom=1.0, shake=0.0, fi=0):
        img = scene.convert("RGB")
        if zoom != 1.0:
            zw, zh = int(W / zoom), int(H / zoom)
            img = img.crop(((W - zw) // 2, (H - zh) // 2, (W - zw) // 2 + zw, (H - zh) // 2 + zh)).resize((W, H), Image.BILINEAR)
        if shake > 0:
            img = ImageChops.offset(img, int(math.sin(t * 91) * 22 * shake), int(math.cos(t * 77) * 22 * shake))
        img = Image.blend(img, ImageChops.overlay(img, self.GRAIN[fi % 4]), 0.35).convert("RGBA")
        tx = (W - self.TITLE.width - self.BADGE.width - 18) // 2
        img.alpha_composite(self.BADGE, (tx, 230 + (104 - self.BADGE.height) // 2))
        img.alpha_composite(self.TITLE, (tx + self.BADGE.width + 18, 230))
        self.draw_caption(img, t)
        return img.convert("RGB")

    def frame(self, SC, t, fi):
        for i, (fn, a, b) in enumerate(SC):
            if a <= t < b or (i == len(SC) - 1 and t >= a):
                img, z, sh = fn(t, a, b)
                out = self.finish(img, t, z, sh, fi)
                fl = clamp(1 - (t - a) / 0.12) if i > 0 else 0
                if fl > 0: out = Image.blend(out, Image.new("RGB", (W, H), WHITE), 0.35 * fl)
                return out

    def frame_range(self, SC, i):
        fn, a, b = SC[i]
        return int(round(a * FPS)), (int(round(b * FPS)) if i < len(SC) - 1 else int(round(self.TOTAL * FPS)))

    def main(self, SC, build, sfx=None):
        """sfx = dict(stamps=[t...], pops=[t...], whooshes=[(t, durée)...], rain_scenes=[i...]).
        Modes : stills T1 T2... | video I J... | render | sfx | final NOM.mp4"""
        mode = sys.argv[1]
        os.makedirs(os.path.join(self.dir, "scenes"), exist_ok=True)
        if mode == "sfx":
            print(make_sfx(self, SC, **(sfx or {"stamps": [], "pops": []}))); return
        if mode == "final":
            print(assemble(self.dir, len(SC), sys.argv[2])); return
        if mode == "render":
            n = len(SC); a = [str(i) for i in range(0, n, 2)]; b = [str(i) for i in range(1, n, 2)]
            ps = [subprocess.Popen([sys.executable, sys.argv[0], "video"] + g) for g in (a, b)]
            codes = [p.wait() for p in ps]
            missing = [i for i in range(n) if not os.path.exists(os.path.join(self.dir, "scenes", f"s{i:02d}.mp4"))]
            if any(codes) or missing: sys.exit(f"rendu incomplet, scènes manquantes: {missing}")
            print("OK", n, "scènes"); return
        build()
        if mode == "stills":
            outs = []
            for t in [float(x) for x in sys.argv[2:]]:
                p = os.path.join(self.dir, f"still_{t:05.2f}.jpg"); self.frame(SC, t, int(t * FPS)).save(p, quality=88); outs.append(p)
            ims = [Image.open(p).resize((300, 533)) for p in outs]
            for k in range(0, len(ims), 8):
                sheet = Image.new("RGB", (300 * 8, 533), "black")
                for j, im in enumerate(ims[k:k + 8]): sheet.paste(im, (j * 300, 0))
                sheet.save(os.path.join(self.dir, f"sheet{k // 8}.jpg"), quality=85)
            print("planches:", sorted(glob.glob(os.path.join(self.dir, "sheet*.jpg"))))
        elif mode == "video":
            for i in [int(x) for x in sys.argv[2:]]:
                f0, f1 = self.frame_range(SC, i)
                tmp = os.path.join(self.dir, "scenes", f"tmp_{i:02d}.mp4"); out = os.path.join(self.dir, "scenes", f"s{i:02d}.mp4")
                p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                      "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
                for fi in range(f0, f1): p.stdin.write(self.frame(SC, fi / FPS, fi).tobytes())
                p.stdin.close()
                if p.wait() == 0: os.replace(tmp, out); print("scene", i, f1 - f0, "frames")

# ---------- sound ----------
def make_sfx(ep, SC, stamps, pops, whooshes=(), rain_scenes=(), out=None, seed=7):
    """Nappe + battement + whoosh à chaque changement de scène, impact (stamps), pop (pops), longs souffles (whooshes=[(t, durée)])."""
    SR = 44100; T = ep.TOTAL; N = int(T * SR) + SR
    rng = np.random.default_rng(seed)
    o = np.zeros(N, np.float32); t = np.arange(N) / SR
    drone = 0.5 * np.sin(2 * np.pi * 49 * t) + 0.3 * np.sin(2 * np.pi * 73.4 * t + 0.3) + 0.15 * np.sin(2 * np.pi * 98 * t)
    o += 0.05 * drone * (0.6 + 0.4 * np.sin(2 * np.pi * 0.12 * t))
    def add(ts, sig, g):
        s = int(ts * SR); e = min(N, s + len(sig))
        if 0 <= s < N: o[s:e] += g * sig[:e - s]
    def lp(x, a):
        y = np.zeros_like(x); acc = 0.0
        for i, v in enumerate(x): acc += a * (v - acc); y[i] = acc
        return y
    for k in np.arange(0.0, T, 0.5):
        n = int(0.18 * SR); tt = np.arange(n) / SR; add(k, np.sin(2 * np.pi * (60 - 20 * tt / 0.18) * tt) * np.exp(-tt * 22), 0.07)
    n = int(0.5 * SR); tt = np.arange(n) / SR
    TH = np.sin(2 * np.pi * (90 - 40 * tt) * tt) * np.exp(-tt * 9) + rng.normal(0, 1, n) * np.exp(-tt * 40) * 0.6
    def whoosh(dur):
        n = int(dur * SR); tt = np.arange(n) / SR
        return lp(rng.normal(0, 1, n).astype(np.float32), 0.08) * np.sin(np.pi * tt / dur) ** 2 * 3
    n = int(0.12 * SR); tt = np.arange(n) / SR; P = np.sin(2 * np.pi * (500 + 1400 * tt / 0.12) * tt) * np.exp(-tt * 30)
    W1 = whoosh(0.4)
    for fn, a, b in SC[1:]: add(a - 0.12, W1, 0.5)
    for s in stamps: add(s + 0.16, TH, 0.7)
    for s in pops: add(s + 0.05, P, 0.35)
    for s, dur in whooshes: add(s, whoosh(dur), 0.4)
    for i in rain_scenes:
        fn, a, b = SC[i]; n = int((b - a) * SR); add(a, lp(rng.normal(0, 1, n).astype(np.float32), 0.35) * 0.5, 0.25)
    o = o / np.abs(o).max() * 0.5
    out = out or os.path.join(ep.dir, "sfx.wav")
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((o * 32767).astype(np.int16).tobytes())
    return out

def assemble(ep_dir, n_scenes, out_name, crf=26):
    """Concatène les scènes, mixe voix + bruitages, encode le MP4 final (léger, prêt à publier)."""
    os.makedirs(os.path.join(ep_dir, "final"), exist_ok=True)
    lst = os.path.join(ep_dir, "list.txt")
    with open(lst, "w") as f:
        for i in range(n_scenes): f.write(f"file 'scenes/s{i:02d}.mp4'\n")
    vo = os.path.join(ep_dir, "video_only.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vo], check=True)
    tmp = os.path.join(ep_dir, "final", "tmp.mp4"); out = os.path.join(ep_dir, "final", out_name)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vo, "-i", os.path.join(ep_dir, "voice.wav"), "-i", os.path.join(ep_dir, "sfx.wav"),
                    "-filter_complex", "[1:a]aresample=48000,highpass=f=70,acompressor=threshold=-18dB:ratio=2.5:attack=5:release=80,volume=1.4[v];[2:a]aresample=48000,volume=0.45[s];[v][s]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out)
    return out
