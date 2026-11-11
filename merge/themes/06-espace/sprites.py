"""ESPACE MERGE (épisode 6) : caillou → trou noir + OVNI (rebondissement)."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from sprites_base import gradient_fill, draw_body, draw_face, star, blob_points

SS = 3
LEVELS = [
    ("CAILLOU",            "Caillou",            24),
    ("ASTÉROÏDE",          "Astéroïde",          36),
    ("LUNE",               "Lune",               50),
    ("PLANÈTE",            "Planète",            64),
    ("PLANÈTE À ANNEAUX",  "Planète à anneaux",  80),
    ("ÉTOILE",             "Étoile",             98),
    ("SUPERNOVA",          "Supernova",         120),
    ("TROU NOIR",          "Trou noir",         150),
]
BOMB_R = 46
OUT = (45, 30, 60, 255)


def craters(img, mask, c, R, seed, n, col):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    rnd = random.Random(seed)
    for _ in range(n):
        x = c + rnd.uniform(-0.7, 0.7) * R; y = c + rnd.uniform(-0.7, 0.7) * R; r = rnd.uniform(0.08, 0.2) * R
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (120,), outline=col + (200,), width=max(1, int(0.02 * R)))
    lay.putalpha(ImageChops.multiply(lay.getchannel("A"), mask))
    img.alpha_composite(lay)


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.65 if level >= 4 else 1.45
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    if level == 0:  # caillou
        pts = blob_points(c, c, R * 1.05, R * 0.85, 1, wobble=0.12)
        draw_body(img, pts, 1, (210, 205, 215), (160, 155, 170), (100, 95, 110), OUT, crumbs=True)
        draw_face(img, c, c + 0.08 * R, 0.62 * R)
    elif level == 1:  # astéroïde
        pts = blob_points(c, c, R * 1.05, R * 0.9, 7, wobble=0.16)
        m = draw_body(img, pts, 7, (205, 170, 140), (150, 110, 80), (90, 60, 40), OUT, crumbs=True)
        craters(img, m, c, R, 3, 5, (90, 60, 40))
        draw_face(img, c, c + 0.05 * R, 0.66 * R, "open")
    elif level == 2:  # lune
        pts = blob_points(c, c, R, R, 2, wobble=0.0)
        m = draw_body(img, pts, 2, (255, 255, 235), (240, 235, 200), (190, 180, 140), OUT, crumbs=False)
        craters(img, m, c, R, 5, 6, (190, 180, 140))
        d = ImageDraw.Draw(img)
        for sx in (-1, 1):  # yeux endormis
            x = c + sx * 0.3 * R
            d.arc([x - 0.14 * R, c - 0.12 * R, x + 0.14 * R, c + 0.08 * R], 0, 180, fill=OUT, width=int(0.05 * R))
        d.arc([c - 0.12 * R, c + 0.12 * R, c + 0.12 * R, c + 0.3 * R], 20, 160, fill=OUT, width=int(0.04 * R))
        f = Image.new("RGBA", img.size, (0, 0, 0, 0)); fd = ImageDraw.Draw(f)
        fd.ellipse([c - 0.7 * R, c + 0.05 * R, c - 0.4 * R, c + 0.25 * R], fill=(255, 140, 160, 140))
        fd.ellipse([c + 0.4 * R, c + 0.05 * R, c + 0.7 * R, c + 0.25 * R], fill=(255, 140, 160, 140))
        img.alpha_composite(f.filter(ImageFilter.GaussianBlur(R * 0.04)))
        d = ImageDraw.Draw(img)
        d.text((c + 0.85 * R, c - 0.95 * R), "z", fill=(90, 70, 200, 255))
        star(img, c + 0.95 * R, c - 0.75 * R, 0.12 * R, (255, 230, 90, 255))
    elif level == 3:  # planète type Terre
        pts = blob_points(c, c, R, R, 3, wobble=0.0)
        m = draw_body(img, pts, 3, (150, 210, 255), (60, 140, 235), (25, 70, 160), OUT, crumbs=False)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        rnd = random.Random(8)
        for _ in range(6):
            x = c + rnd.uniform(-0.8, 0.8) * R; y = c + rnd.uniform(-0.8, 0.8) * R
            ld.polygon(blob_points(x, y, rnd.uniform(0.18, 0.35) * R, rnd.uniform(0.12, 0.25) * R, rnd.randint(0, 99), wobble=0.25, n=24), fill=(80, 190, 90, 255))
        lay.putalpha(ImageChops.multiply(lay.getchannel("A"), m))
        img.alpha_composite(lay)
        draw_face(img, c, c + 0.05 * R, 0.66 * R)
    elif level == 4:  # planète à anneaux
        ring = Image.new("RGBA", img.size, (0, 0, 0, 0)); rd = ImageDraw.Draw(ring)
        rw, rh = 1.55 * R, 0.42 * R
        rd.ellipse([c - rw, c - rh, c + rw, c + rh], outline=(255, 120, 200, 255), width=int(0.13 * R))
        img.alpha_composite(ring.rotate(-14, resample=Image.BICUBIC, center=(c, c)))
        pts = blob_points(c, c, R * 0.95, R * 0.95, 4, wobble=0.0)
        m = draw_body(img, pts, 4, (255, 225, 150), (250, 160, 60), (190, 90, 30), OUT, crumbs=False)
        bands = Image.new("RGBA", img.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(bands)
        for y, h in ((-0.45, 0.1), (0.35, 0.13), (0.62, 0.07)):
            bd.ellipse([c - 1.3 * R, c + (y - h) * R, c + 1.3 * R, c + (y + h) * R], fill=(220, 100, 40, 110))
        bands.putalpha(ImageChops.multiply(bands.getchannel("A"), m))
        img.alpha_composite(bands)
        draw_face(img, c, c + 0.05 * R, 0.66 * R)
        front = Image.new("RGBA", img.size, (0, 0, 0, 0)); fd = ImageDraw.Draw(front)
        fd.arc([c - rw, c - rh, c + rw, c + rh], 5, 175, fill=(255, 160, 225, 255), width=int(0.13 * R))
        img.alpha_composite(front.rotate(-14, resample=Image.BICUBIC, center=(c, c)))
    elif level == 5:  # étoile
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([c - 1.2 * R, c - 1.2 * R, c + 1.2 * R, c + 1.2 * R], fill=(255, 230, 90, 140))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.2)))
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = 1.15 * R if i % 2 == 0 else 0.62 * R
            pts.append((c + rr * math.cos(a), c + 0.08 * R + rr * math.sin(a)))
        m = Image.new("L", img.size, 0)
        ImageDraw.Draw(m).polygon(pts, fill=255)
        m = m.filter(ImageFilter.GaussianBlur(R * 0.06)).point(lambda v: 255 if v > 120 else 0)
        img.alpha_composite(gradient_fill(img.size, m, (255, 255, 190), (255, 215, 40), (230, 150, 0)))
        edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(7))
        img.alpha_composite(Image.composite(Image.new("RGBA", img.size, (170, 100, 0, 255)), Image.new("RGBA", img.size, (0, 0, 0, 0)), edge))
        draw_face(img, c, c + 0.15 * R, 0.55 * R, "open")
    elif level == 6:  # supernova
        burst = Image.new("RGBA", img.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(burst)
        rnd = random.Random(6)
        for k in range(22):
            a = k / 22 * 6.283 + rnd.uniform(-0.05, 0.05); L = rnd.uniform(1.15, 1.55) * R
            w = 0.12 * R
            bd.polygon([(c + 0.6 * R * math.cos(a - 0.15), c + 0.6 * R * math.sin(a - 0.15)), (c + L * math.cos(a), c + L * math.sin(a)),
                        (c + 0.6 * R * math.cos(a + 0.15), c + 0.6 * R * math.sin(a + 0.15))], fill=(255, rnd.randint(90, 200), 40, 230))
        img.alpha_composite(burst.filter(ImageFilter.GaussianBlur(R * 0.02)))
        pts = blob_points(c, c, R * 0.95, R * 0.95, 9, wobble=0.05)
        draw_body(img, pts, 9, (255, 250, 210), (255, 170, 60), (220, 60, 40), OUT, crumbs=False)
        draw_face(img, c, c + 0.05 * R, 0.66 * R, "sweat")
    elif level == 7:  # trou noir
        w = side
        yy, xx = np.mgrid[0:w, 0:w].astype(np.float32)
        dx, dy = (xx - c) / R, (yy - c) / R
        rr = np.sqrt(dx ** 2 + dy ** 2); th = np.arctan2(dy, dx)
        swirl = 0.5 + 0.5 * np.cos(3 * th + 6 * np.log(rr + 0.2))
        disk = np.clip(1 - np.abs(rr - 0.95) / 0.5, 0, 1)
        col = np.array([255, 150, 60], np.float32) * (1 - swirl[..., None]) + np.array([200, 80, 255], np.float32) * swirl[..., None]
        alpha = disk * (0.5 + 0.5 * swirl)
        acc = Image.fromarray(np.dstack([col, alpha[..., None] * 255]).astype(np.uint8), "RGBA")
        img.alpha_composite(acc.filter(ImageFilter.GaussianBlur(R * 0.1)))
        img.alpha_composite(acc)
        d = ImageDraw.Draw(img)
        d.ellipse([c - 0.62 * R, c - 0.62 * R, c + 0.62 * R, c + 0.62 * R], fill=(8, 4, 16, 255), outline=(255, 220, 160, 255), width=int(0.04 * R))
        for sx in (-1, 1):
            x = c + sx * 0.22 * R
            d.ellipse([x - 0.11 * R, c - 0.15 * R, x + 0.11 * R, c + 0.1 * R], fill=(255, 255, 255, 255))
            d.ellipse([x - 0.04 * R, c - 0.06 * R, x + 0.04 * R, c + 0.04 * R], fill=(120, 60, 220, 255))
        d.arc([c - 0.14 * R, c + 0.12 * R, c + 0.14 * R, c + 0.3 * R], 20, 160, fill=(255, 255, 255, 255), width=int(0.035 * R))
        for (sx, sy, ss) in ((-1.2, -0.9, 0.13), (1.15, -0.95, 0.11), (1.2, 0.9, 0.1), (-1.1, 1.0, 0.1)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 250, 200, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """L'OVNI : soucoupe grise, dôme vert, petit alien aux sourcils froncés."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    d = ImageDraw.Draw(img)
    dome = Image.new("RGBA", img.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(dome)
    dd.ellipse([c - 0.55 * R, c - 0.95 * R, c + 0.55 * R, c + 0.15 * R], fill=(150, 255, 170, 150), outline=(220, 255, 230, 255), width=int(0.04 * R))
    d.ellipse([c - 0.3 * R, c - 0.7 * R, c + 0.3 * R, c - 0.1 * R], fill=(120, 220, 90, 255), outline=(40, 90, 30, 255), width=int(0.03 * R))
    for sx in (-1, 1):
        x = c + sx * 0.12 * R
        d.ellipse([x - 0.08 * R, c - 0.5 * R, x + 0.08 * R, c - 0.36 * R], fill=(10, 10, 10, 255))
        d.line([(x - sx * 0.12 * R, c - 0.6 * R), (x + sx * 0.08 * R, c - 0.52 * R)], fill=(20, 40, 10, 255), width=int(0.04 * R))
    img.alpha_composite(dome)
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).ellipse([c - 1.15 * R, c - 0.2 * R, c + 1.15 * R, c + 0.45 * R], fill=255)
    img.alpha_composite(gradient_fill(img.size, m, (235, 235, 245), (160, 165, 180), (80, 85, 100)))
    d = ImageDraw.Draw(img)
    d.ellipse([c - 1.15 * R, c - 0.2 * R, c + 1.15 * R, c + 0.45 * R], outline=(40, 40, 55, 255), width=int(0.04 * R))
    for k in range(5):
        x = c + (k - 2) * 0.42 * R
        d.ellipse([x - 0.08 * R, c + 0.05 * R, x + 0.08 * R, c + 0.2 * R], fill=(255, 220, 60, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(10, 6, 20, 255), glow=(255, 220, 90)):
    a = img.getchannel("A").point(lambda v: 255 if v > 90 else 0).filter(ImageFilter.GaussianBlur(1.2))
    sil = Image.new("RGBA", img.size, col); sil.putalpha(a)
    g = Image.new("RGBA", img.size, glow + (255,))
    g.putalpha(a.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(6)))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(sil)
    return out


def build_all():
    return [make_sprite(i) for i in range(len(LEVELS))]


if __name__ == "__main__":
    import os
    sprites = build_all() + [make_bomb()]
    W = sum(s.width for s in sprites) + 40 * len(sprites)
    H = max(s.height for s in sprites) + 40
    sheet = Image.new("RGBA", (W, H), (185, 150, 255, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
