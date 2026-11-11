"""FERME MERGE (épisode 5) : animaux de la ferme + loup (rebondissement)."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from sprites_base import gradient_fill, draw_body, draw_face, star, blob_points

SS = 3
LEVELS = [
    ("ŒUF",               "Œuf",               24),
    ("POUSSIN",           "Poussin",           36),
    ("POULE",             "Poule",             50),
    ("CANARD",            "Canard",            64),
    ("COCHON",            "Cochon",            80),
    ("MOUTON",            "Mouton",            98),
    ("VACHE",             "Vache",            120),
    ("VACHE LÉGENDAIRE",  "Vache légendaire", 150),
]
BOMB_R = 46
OUT = (70, 40, 25, 255)


def beak(d, cx, cy, s, col=(255, 150, 30, 255)):
    d.polygon([(cx - 0.16 * s, cy), (cx + 0.16 * s, cy), (cx, cy + 0.2 * s)], fill=col, outline=OUT)


def body(img, c, R, pal, seed, rx=1.0, ry=0.92, wobble=0.04):
    pts = blob_points(c, c + 0.04 * R, R * rx, R * ry, seed, wobble=wobble, squish=0.12)
    return draw_body(img, pts, seed, *pal, OUT, crumbs=False)


def face_noumouth(img, cx, cy, s):
    """Yeux + joues de draw_face, bouche masquée ensuite par le bec/museau."""
    draw_face(img, cx, cy, s, "happy")


def cow(img, c, R, seed, legendary=False):
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):  # cornes + oreilles
        d.polygon([(c + sx * 0.45 * R, c - 0.7 * R), (c + sx * 0.75 * R, c - 1.15 * R), (c + sx * 0.62 * R, c - 0.62 * R)],
                  fill=(250, 235, 190, 255) if not legendary else (255, 215, 60, 255), outline=OUT)
        d.ellipse([c + sx * 1.0 * R - 0.25 * R, c - 0.55 * R, c + sx * 1.0 * R + 0.25 * R, c - 0.3 * R], fill=(240, 240, 240, 255), outline=OUT)
    pal = ((255, 255, 255), (238, 238, 242), (190, 190, 200)) if not legendary else ((255, 250, 210), (255, 225, 120), (210, 160, 40))
    mask = body(img, c, R, pal, seed)
    spots = Image.new("RGBA", img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(spots)
    rnd = random.Random(seed)
    for _ in range(5):
        x = c + rnd.uniform(-0.8, 0.8) * R; y = c + rnd.uniform(-0.75, 0.2) * R; rr = rnd.uniform(0.15, 0.28) * R
        sd.ellipse([x - rr, y - rr * 0.8, x + rr, y + rr * 0.8], fill=(30, 25, 30, 255) if not legendary else (190, 120, 20, 255))
    from PIL import ImageChops
    spots.putalpha(ImageChops.multiply(spots.getchannel("A"), mask))
    img.alpha_composite(spots)
    face_noumouth(img, c, c - 0.12 * R, 0.62 * R)
    d = ImageDraw.Draw(img)
    d.ellipse([c - 0.48 * R, c + 0.12 * R, c + 0.48 * R, c + 0.62 * R], fill=(255, 170, 185, 255), outline=OUT, width=max(2, int(0.03 * R)))
    for sx in (-1, 1):
        d.ellipse([c + sx * 0.2 * R - 0.07 * R, c + 0.3 * R, c + sx * 0.2 * R + 0.07 * R, c + 0.42 * R], fill=(150, 60, 80, 255))
    d.arc([c - 0.15 * R, c + 0.38 * R, c + 0.15 * R, c + 0.56 * R], 20, 160, fill=OUT, width=max(2, int(0.035 * R)))


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.6 if level >= 4 else 1.45
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    d = ImageDraw.Draw(img)
    if level == 0:  # œuf
        pts = blob_points(c, c + 0.05 * R, R * 0.85, R * 1.05, 3, wobble=0.0)
        pts = [(x, y - 0.12 * R * max(0, (c - y) / R)) for x, y in pts]
        draw_body(img, pts, 3, (255, 255, 250), (245, 238, 220), (200, 185, 160), OUT, crumbs=False)
        d = ImageDraw.Draw(img)
        d.line([(c - 0.5 * R, c - 0.35 * R), (c - 0.3 * R, c - 0.5 * R), (c - 0.12 * R, c - 0.32 * R), (c + 0.05 * R, c - 0.52 * R)], fill=OUT, width=max(2, int(0.05 * R)))
        draw_face(img, c, c + 0.15 * R, 0.6 * R)
    elif level == 1:  # poussin
        d.polygon([(c - 0.1 * R, c - 0.85 * R), (c, c - 1.2 * R), (c + 0.12 * R, c - 0.88 * R)], fill=(255, 220, 40, 255), outline=OUT)
        body(img, c, R, ((255, 245, 140), (255, 220, 40), (215, 160, 0)), 11)
        face_noumouth(img, c, c - 0.08 * R, 0.7 * R)
        d = ImageDraw.Draw(img)
        beak(d, c, c + 0.08 * R, 0.8 * R)
        for sx in (-1, 1):
            d.ellipse([c + sx * 0.95 * R - 0.2 * R, c + 0.05 * R, c + sx * 0.95 * R + 0.2 * R, c + 0.45 * R], fill=(255, 205, 30, 255), outline=OUT)
    elif level == 2:  # poule
        for k, dx in enumerate((-0.25, 0, 0.25)):
            d.ellipse([c + dx * R - 0.18 * R, c - 1.12 * R - (0.06 if k == 1 else 0) * R, c + dx * R + 0.18 * R, c - 0.78 * R], fill=(235, 40, 50, 255), outline=OUT)
        body(img, c, R, ((255, 255, 255), (240, 238, 232), (195, 185, 175)), 12)
        face_noumouth(img, c, c - 0.1 * R, 0.68 * R)
        d = ImageDraw.Draw(img)
        beak(d, c, c + 0.06 * R, 0.8 * R)
        d.ellipse([c - 0.08 * R, c + 0.22 * R, c + 0.08 * R, c + 0.42 * R], fill=(235, 40, 50, 255))
    elif level == 3:  # canard
        body(img, c, R, ((255, 245, 150), (255, 215, 50), (220, 160, 10)), 13)
        face_noumouth(img, c, c - 0.15 * R, 0.66 * R)
        d = ImageDraw.Draw(img)
        d.ellipse([c - 0.38 * R, c + 0.02 * R, c + 0.38 * R, c + 0.3 * R], fill=(255, 140, 20, 255), outline=OUT, width=max(2, int(0.03 * R)))
        d.line([(c - 0.32 * R, c + 0.16 * R), (c + 0.32 * R, c + 0.16 * R)], fill=(200, 90, 10, 255), width=max(2, int(0.03 * R)))
        d.pieslice([c - 0.55 * R, c - 1.15 * R, c + 0.55 * R, c - 0.45 * R], 180, 360, fill=(40, 90, 200, 255))  # bob
        d.rectangle([c - 0.6 * R, c - 0.82 * R, c + 0.6 * R, c - 0.74 * R], fill=(255, 255, 255, 255))
    elif level == 4:  # cochon
        for sx in (-1, 1):
            d.polygon([(c + sx * 0.4 * R, c - 0.7 * R), (c + sx * 0.85 * R, c - 1.05 * R), (c + sx * 0.8 * R, c - 0.5 * R)], fill=(255, 150, 180, 255), outline=OUT)
        body(img, c, R, ((255, 210, 225), (255, 160, 190), (215, 100, 140)), 14)
        face_noumouth(img, c, c - 0.15 * R, 0.66 * R)
        d = ImageDraw.Draw(img)
        d.ellipse([c - 0.3 * R, c + 0.02 * R, c + 0.3 * R, c + 0.34 * R], fill=(255, 130, 165, 255), outline=OUT, width=max(2, int(0.03 * R)))
        for sx in (-1, 1):
            d.ellipse([c + sx * 0.11 * R - 0.05 * R, c + 0.12 * R, c + sx * 0.11 * R + 0.05 * R, c + 0.25 * R], fill=(140, 40, 70, 255))
    elif level == 5:  # mouton
        rnd = random.Random(5)
        for k in range(16):
            a = k / 16 * 6.283
            x, y = c + 0.82 * R * math.cos(a), c + 0.75 * R * math.sin(a)
            rr = rnd.uniform(0.28, 0.36) * R
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(255, 255, 255, 255), outline=(190, 185, 180, 255), width=max(2, int(0.02 * R)))
        d.ellipse([c - 0.85 * R, c - 0.78 * R, c + 0.85 * R, c + 0.78 * R], fill=(252, 252, 250, 255))
        for sx in (-1, 1):
            d.ellipse([c + sx * 0.62 * R - 0.25 * R, c - 0.3 * R, c + sx * 0.62 * R + 0.25 * R, c - 0.1 * R], fill=(70, 60, 60, 255))
        d.ellipse([c - 0.5 * R, c - 0.5 * R, c + 0.5 * R, c + 0.45 * R], fill=(80, 70, 70, 255), outline=OUT, width=max(2, int(0.03 * R)))
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw_face(lay, c, c - 0.05 * R, 0.5 * R)
        img.alpha_composite(lay)
        d = ImageDraw.Draw(img)
        for k in range(5):
            x = c + (k - 2) * 0.16 * R
            d.ellipse([x - 0.14 * R, c - 0.68 * R, x + 0.14 * R, c - 0.42 * R], fill=(255, 255, 255, 255))
    elif level == 6:
        cow(img, c, R, 16)
    elif level == 7:  # vache légendaire
        rb = Image.new("RGBA", img.size, (0, 0, 0, 0)); rd = ImageDraw.Draw(rb)
        for k, col in enumerate([(255, 60, 60), (255, 160, 40), (255, 230, 60), (60, 200, 90), (60, 150, 255), (150, 80, 230)]):
            rr = 1.45 * R - k * 0.08 * R
            rd.arc([c - rr, c - rr, c + rr, c + rr], 180, 360, fill=col + (255,), width=int(0.08 * R))
        img.alpha_composite(rb)
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([c - 1.15 * R, c - 1.15 * R, c + 1.15 * R, c + 1.15 * R], fill=(255, 230, 120, 170))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.18)))
        cow(img, c, R * 0.85, 17, legendary=True)
        d = ImageDraw.Draw(img)
        for sx in (-1, 1):  # lunettes noires
            x = c + sx * 0.23 * R
            d.rounded_rectangle([x - 0.2 * R, c - 0.32 * R, x + 0.2 * R, c - 0.08 * R], radius=0.06 * R, fill=(15, 15, 25, 255))
        d.line([(c - 0.05 * R, c - 0.25 * R), (c + 0.05 * R, c - 0.25 * R)], fill=(15, 15, 25, 255), width=int(0.05 * R))
        top = c - 0.95 * R; cw = 0.4 * R
        crown = [(c - cw, top + 0.05 * R), (c - cw, top - 0.32 * R), (c - cw * 0.5, top - 0.1 * R), (c, top - 0.42 * R),
                 (c + cw * 0.5, top - 0.1 * R), (c + cw, top - 0.32 * R), (c + cw, top + 0.05 * R)]
        d.polygon(crown, fill=(255, 205, 40, 255), outline=(150, 90, 0, 255))
        for (sx, sy, ss) in ((-1.2, -0.6, 0.12), (1.2, -0.7, 0.11), (1.15, 0.8, 0.1), (-1.1, 0.9, 0.1)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 180, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """Le loup."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.7) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        d.polygon([(c + sx * 0.35 * R, c - 0.7 * R), (c + sx * 0.8 * R, c - 1.25 * R), (c + sx * 0.9 * R, c - 0.45 * R)], fill=(110, 115, 130, 255), outline=(30, 30, 40, 255))
    m = Image.new("L", (side, side), 0)
    ImageDraw.Draw(m).ellipse([c - R, c - 0.85 * R, c + R, c + R], fill=255)
    img.alpha_composite(gradient_fill((side, side), m, (170, 175, 190), (110, 115, 130), (55, 58, 70)))
    d = ImageDraw.Draw(img)
    d.ellipse([c - 0.5 * R, c + 0.05 * R, c + 0.5 * R, c + 0.8 * R], fill=(225, 225, 230, 255))
    d.ellipse([c - 0.14 * R, c + 0.1 * R, c + 0.14 * R, c + 0.28 * R], fill=(20, 20, 25, 255))
    for k in range(4):
        x = c - 0.3 * R + k * 0.2 * R
        d.polygon([(x - 0.07 * R, c + 0.5 * R), (x + 0.07 * R, c + 0.5 * R), (x, c + 0.68 * R)], fill=(255, 255, 255, 255), outline=(30, 30, 40, 255))
    for sx in (-1, 1):
        x = c + sx * 0.35 * R
        d.ellipse([x - 0.14 * R, c - 0.3 * R, x + 0.14 * R, c - 0.02 * R], fill=(255, 220, 40, 255))
        d.ellipse([x - 0.05 * R, c - 0.22 * R, x + 0.05 * R, c - 0.08 * R], fill=(20, 0, 0, 255))
        d.line([(x - sx * 0.2 * R, c - 0.45 * R), (x + sx * 0.18 * R, c - 0.3 * R)], fill=(30, 30, 40, 255), width=int(0.08 * R))
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
    sprites = build_all() + [make_bomb()]
    W = sum(s.width for s in sprites) + 40 * len(sprites)
    H = max(s.height for s in sprites) + 40
    sheet = Image.new("RGBA", (W, H), (120, 195, 255, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save("/home/claude/merge5/sheet.png")
