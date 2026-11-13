"""DINOSAURES MERGE (épisode 8) : œuf → dino-roi + MÉTÉORITE (rebondissement)."""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("ŒUF",          "Œuf",          24),
    ("BÉBÉ DINO",    "Bébé dino",    36),
    ("RAPTOR",       "Raptor",       50),
    ("TRICÉRATOPS",  "Tricératops",  64),
    ("STÉGOSAURE",   "Stégosaure",   80),
    ("DIPLODOCUS",   "Diplodocus",   98),
    ("T-REX",        "T-Rex",       120),
    ("DINO-ROI",     "Dino-roi",    150),
]
BOMB_R = 46
OUT = (30, 45, 25, 255)

GREEN = ((190, 250, 140), (100, 200, 70), (40, 130, 40))
ORANGE = ((255, 215, 140), (255, 145, 50), (200, 80, 20))
BLUE = ((170, 225, 255), (70, 160, 240), (30, 90, 180))
PURPLE = ((230, 190, 255), (165, 100, 235), (100, 50, 170))
TEAL = ((170, 255, 230), (50, 200, 170), (20, 120, 110))
RED = ((255, 170, 150), (235, 75, 60), (160, 30, 30))
GOLD = ((255, 250, 180), (255, 205, 40), (205, 135, 0))
CREAM = ((255, 255, 240), (250, 240, 200), (215, 195, 140))


def shape(img, cols, lw, draw):
    """draw(md) dessine le masque ; remplissage dégradé + contour épais."""
    m = Image.new("L", img.size, 0)
    draw(ImageDraw.Draw(m))
    img.alpha_composite(gradient_fill(img.size, m, *cols))
    edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(max(3, (lw // 2) * 2 + 1)))
    img.alpha_composite(Image.composite(Image.new("RGBA", img.size, OUT), Image.new("RGBA", img.size, (0, 0, 0, 0)), edge))
    return m


def E(md, x, y, rx, ry):
    md.ellipse([x - rx, y - ry, x + rx, y + ry], fill=255)


def spots(img, mask, c, R, n, col, seed):
    t = Image.new("RGBA", img.size, (0, 0, 0, 0)); td = ImageDraw.Draw(t)
    rnd = random.Random(seed)
    for _ in range(n):
        x = c + rnd.uniform(-1.2, 1.2) * R; y = c + rnd.uniform(-1.2, 1.2) * R; rr = rnd.uniform(0.06, 0.13) * R
        td.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col)
    t.putalpha(ImageChops.multiply(t.getchannel("A"), mask))
    img.alpha_composite(t)


def legs(img, xs, ytop, ybot, w, cols, lw):
    for x in xs:
        shape(img, cols, lw, lambda md, x=x: md.rounded_rectangle([x - w, ytop, x + w, ybot], w * 0.8, fill=255))


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.65 if level >= 4 else 1.45
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    if level == 0:  # œuf tacheté
        m = shape(img, CREAM, lw, lambda md: E(md, c, c + 0.05 * R, 0.85 * R, 1.08 * R))
        spots(img, m, c, R, 9, (120, 200, 90, 200), 1)
        d = ImageDraw.Draw(img)
        d.line([(c - 0.5 * R, c - 0.55 * R), (c - 0.25 * R, c - 0.35 * R), (c, c - 0.6 * R), (c + 0.2 * R, c - 0.4 * R)], fill=OUT, width=max(2, lw // 2))
        draw_face(img, c, c + 0.15 * R, 0.85 * R, "happy")
    elif level == 1:  # bébé dino avec coquille sur la tête
        shape(img, GREEN, lw, lambda md: md.polygon([(c + 0.5 * R, c + 0.5 * R), (c + 1.3 * R, c + 0.85 * R), (c + 0.4 * R, c + 0.95 * R)], fill=255))
        legs(img, (c - 0.45 * R, c + 0.45 * R), c + 0.5 * R, c + 1.1 * R, 0.22 * R, GREEN, lw)
        m = shape(img, GREEN, lw, lambda md: E(md, c, c + 0.15 * R, 0.95 * R, 0.9 * R))
        shape(img, ((255, 255, 220), (240, 245, 190), (190, 200, 140)), max(2, lw // 2), lambda md: E(md, c, c + 0.45 * R, 0.55 * R, 0.4 * R))
        # coquille
        shape(img, CREAM, lw, lambda md: md.polygon([(c - 0.8 * R, c - 0.45 * R), (c - 0.6 * R, c - 1.0 * R), (c - 0.2 * R, c - 1.2 * R), (c + 0.25 * R, c - 1.18 * R),
                                                     (c + 0.65 * R, c - 0.95 * R), (c + 0.8 * R, c - 0.45 * R), (c + 0.5 * R, c - 0.65 * R), (c + 0.25 * R, c - 0.4 * R),
                                                     (c, c - 0.65 * R), (c - 0.25 * R, c - 0.4 * R), (c - 0.5 * R, c - 0.65 * R)], fill=255))
        draw_face(img, c, c - 0.05 * R, 0.8 * R, "open")
    elif level == 2:  # raptor orange, sur deux pattes, tête vers la droite
        shape(img, ORANGE, lw, lambda md: md.polygon([(c - 0.3 * R, c), (c - 1.35 * R, c - 0.6 * R), (c - 1.25 * R, c - 0.35 * R), (c - 0.2 * R, c + 0.45 * R)], fill=255))
        legs(img, (c - 0.3 * R, c + 0.25 * R), c + 0.3 * R, c + 1.15 * R, 0.17 * R, ORANGE, lw)
        m = shape(img, ORANGE, lw, lambda md: (E(md, c, c + 0.15 * R, 0.6 * R, 0.55 * R), md.polygon([(c - 0.1 * R, c), (c + 0.35 * R, c - 0.75 * R), (c + 0.6 * R, c - 0.5 * R), (c + 0.4 * R, c + 0.2 * R)], fill=255)))
        shape(img, ORANGE, lw, lambda md: md.rounded_rectangle([c + 0.05 * R, c - 1.2 * R, c + 1.3 * R, c - 0.4 * R], 0.38 * R, fill=255))
        d = ImageDraw.Draw(img)
        for k in range(4):  # rayures
            x = c - 0.45 * R + k * 0.25 * R
            d.line([(x, c - 0.25 * R), (x + 0.1 * R, c + 0.05 * R)], fill=(170, 60, 20, 255), width=max(2, lw // 2))
        d.line([(c + 0.4 * R, c + 0.1 * R), (c + 0.75 * R, c + 0.25 * R)], fill=OUT, width=lw)  # petit bras
        draw_face(img, c + 0.7 * R, c - 0.8 * R, 0.62 * R, "happy")
    elif level == 3:  # tricératops bleu, de face/trois-quarts
        shape(img, BLUE, lw, lambda md: md.polygon([(c - 0.6 * R, c + 0.4 * R), (c - 1.4 * R, c + 0.75 * R), (c - 0.6 * R, c + 0.85 * R)], fill=255))
        legs(img, (c - 0.65 * R, c - 0.15 * R, c + 0.35 * R, c + 0.8 * R), c + 0.5 * R, c + 1.15 * R, 0.17 * R, BLUE, lw)
        shape(img, BLUE, lw, lambda md: E(md, c - 0.1 * R, c + 0.35 * R, 0.95 * R, 0.55 * R))
        # collerette
        shape(img, PURPLE, lw, lambda md: md.polygon([(c + 0.45 * R + 0.95 * R * math.cos(a), c - 0.3 * R + 0.95 * R * math.sin(a)) for a in [i / 20 * 6.283 for i in range(20)]], fill=255))
        d = ImageDraw.Draw(img)
        for k in range(10):
            a = k / 10 * 6.283
            x, y = c + 0.45 * R + 0.8 * R * math.cos(a), c - 0.3 * R + 0.8 * R * math.sin(a)
            d.ellipse([x - 0.07 * R, y - 0.07 * R, x + 0.07 * R, y + 0.07 * R], fill=(255, 230, 120, 255))
        shape(img, BLUE, lw, lambda md: E(md, c + 0.45 * R, c - 0.15 * R, 0.6 * R, 0.55 * R))
        for (x0, y0, x1, y1) in ((c + 0.15 * R, c - 0.55 * R, c - 0.05 * R, c - 1.25 * R), (c + 0.75 * R, c - 0.55 * R, c + 0.95 * R, c - 1.25 * R)):
            shape(img, CREAM, max(2, lw // 2), lambda md, a=(x0, y0, x1, y1): md.polygon([(a[0] - 0.1 * R, a[1]), (a[2], a[3]), (a[0] + 0.1 * R, a[1])], fill=255))
        shape(img, CREAM, max(2, lw // 2), lambda md: md.polygon([(c + 0.38 * R, c + 0.25 * R), (c + 0.45 * R, c - 0.05 * R), (c + 0.52 * R, c + 0.25 * R)], fill=255))
        draw_face(img, c + 0.45 * R, c - 0.2 * R, 0.55 * R, "happy")
    elif level == 4:  # stégosaure violet avec plaques
        for k in range(5):
            a = math.pi * (0.2 + 0.6 * k / 4)
            ex, ey = c - 0.15 * R + 0.95 * R * math.cos(a) * 0.9, c + 0.25 * R - 0.6 * R * math.sin(a) * 0.9
            nx, ny = math.cos(a) * 0.95 / 0.6, -math.sin(a)
            nn = math.hypot(nx, ny); nx, ny = nx / nn, ny / nn
            h = (0.55 if k == 2 else 0.45) * R; w = 0.2 * R
            shape(img, RED, max(2, lw // 2), lambda md, ex=ex, ey=ey, nx=nx, ny=ny, h=h, w=w: md.polygon(
                [(ex - ny * w, ey + nx * w), (ex + nx * h, ey + ny * h), (ex + ny * w, ey - nx * w)], fill=255))
        shape(img, PURPLE, lw, lambda md: md.polygon([(c - 0.8 * R, c + 0.2 * R), (c - 1.45 * R, c + 0.1 * R), (c - 0.9 * R, c + 0.6 * R)], fill=255))
        d = ImageDraw.Draw(img)
        for (x, y) in ((c - 1.35 * R, c + 0.02 * R), (c - 1.2 * R, c - 0.05 * R)):
            shape(img, CREAM, max(2, lw // 3), lambda md, x=x, y=y: md.polygon([(x - 0.05 * R, y + 0.12 * R), (x, y - 0.18 * R), (x + 0.06 * R, y + 0.12 * R)], fill=255))
        legs(img, (c - 0.75 * R, c - 0.25 * R, c + 0.2 * R, c + 0.6 * R), c + 0.4 * R, c + 1.05 * R, 0.17 * R, PURPLE, lw)
        m = shape(img, PURPLE, lw, lambda md: E(md, c - 0.15 * R, c + 0.25 * R, 0.95 * R, 0.6 * R))
        spots(img, m, c, R, 8, (130, 70, 200, 150), 4)
        shape(img, PURPLE, lw, lambda md: (md.polygon([(c + 0.5 * R, c + 0.1 * R), (c + 0.85 * R, c - 0.15 * R), (c + 1.0 * R, c + 0.3 * R), (c + 0.7 * R, c + 0.5 * R)], fill=255), E(md, c + 1.0 * R, c, 0.42 * R, 0.36 * R)))
        draw_face(img, c + 1.02 * R, c + 0.02 * R, 0.42 * R, "happy")
    elif level == 5:  # diplodocus turquoise au long cou
        shape(img, TEAL, lw, lambda md: md.polygon([(c - 0.5 * R, c + 0.35 * R), (c - 1.5 * R, c + 0.9 * R), (c - 1.55 * R, c + 0.75 * R), (c - 0.55 * R, c + 0.05 * R)], fill=255))
        legs(img, (c - 0.65 * R, c - 0.2 * R, c + 0.25 * R, c + 0.65 * R), c + 0.5 * R, c + 1.15 * R, 0.17 * R, TEAL, lw)
        shape(img, TEAL, lw, lambda md: (E(md, c, c + 0.4 * R, 0.85 * R, 0.55 * R),
                                         md.polygon([(c + 0.35 * R, c + 0.05 * R), (c + 0.75 * R, c - 0.9 * R), (c + 1.05 * R, c - 0.8 * R), (c + 0.8 * R, c + 0.25 * R)], fill=255),
                                         E(md, c + 1.0 * R, c - 1.0 * R, 0.38 * R, 0.3 * R)))
        d = ImageDraw.Draw(img)
        for k in range(4):
            x = c - 0.45 * R + k * 0.3 * R
            d.ellipse([x - 0.08 * R, c + 0.12 * R, x + 0.08 * R, c + 0.26 * R], fill=(20, 150, 130, 255))
        draw_face(img, c + 1.0 * R, c - 1.0 * R, 0.4 * R, "happy")
    elif level in (6, 7):  # T-Rex (rouge) / Dino-roi (doré)
        cols = RED if level == 6 else GOLD
        if level == 7:
            g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
            for k in range(16):
                a = k / 16 * 6.283
                gd.polygon([(c + 0.5 * R * math.cos(a - 0.12), c + 0.5 * R * math.sin(a - 0.12)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                            (c + 0.5 * R * math.cos(a + 0.12), c + 0.5 * R * math.sin(a + 0.12))], fill=(255, 240, 120, 210) if k % 2 else (120, 220, 90, 210))
            img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
            # cape
            shape(img, ((255, 150, 200), (220, 50, 120), (140, 20, 70)), lw, lambda md: md.polygon([(c - 0.2 * R, c - 0.45 * R), (c - 1.25 * R, c + 1.05 * R), (c + 0.4 * R, c + 1.05 * R), (c + 0.35 * R, c - 0.3 * R)], fill=255))
        shape(img, cols, lw, lambda md: md.polygon([(c - 0.3 * R, c + 0.1 * R), (c - 1.4 * R, c + 0.85 * R), (c - 1.3 * R, c + 1.0 * R), (c - 0.2 * R, c + 0.65 * R)], fill=255))
        legs(img, (c - 0.35 * R, c + 0.25 * R), c + 0.5 * R, c + 1.15 * R, 0.22 * R, cols, lw)
        m = shape(img, cols, lw, lambda md: (E(md, c - 0.05 * R, c + 0.35 * R, 0.6 * R, 0.6 * R),
                                             md.polygon([(c - 0.4 * R, c + 0.1 * R), (c - 0.1 * R, c - 0.55 * R), (c + 0.4 * R, c - 0.45 * R), (c + 0.45 * R, c + 0.3 * R)], fill=255)))
        shape(img, CREAM, max(2, lw // 2), lambda md: E(md, c + 0.1 * R, c + 0.45 * R, 0.35 * R, 0.4 * R))
        # grosse tête
        shape(img, cols, lw, lambda md: md.rounded_rectangle([c - 0.25 * R, c - 1.15 * R, c + 1.3 * R, c - 0.25 * R], 0.38 * R, fill=255))
        d = ImageDraw.Draw(img)
        # dents
        for k in range(6):
            x = c + 0.25 * R + k * 0.17 * R
            d.polygon([(x, c - 0.32 * R), (x + 0.08 * R, c - 0.5 * R), (x + 0.16 * R, c - 0.32 * R)], fill=(255, 255, 255, 255), outline=OUT)
        d.line([(c + 0.2 * R, c - 0.33 * R), (c + 1.25 * R, c - 0.33 * R)], fill=OUT, width=max(2, lw // 2))
        # petits bras ridicules
        for dy in (0.0, 0.14):
            d.line([(c + 0.35 * R, c - 0.05 * R + dy * R), (c + 0.62 * R, c + 0.02 * R + dy * R)], fill=OUT, width=int(0.11 * R))
            d.line([(c + 0.35 * R, c - 0.05 * R + dy * R), (c + 0.6 * R, c + 0.02 * R + dy * R)], fill=cols[1] + (255,), width=int(0.06 * R))
        draw_face(img, c + 0.55 * R, c - 0.8 * R, 0.6 * R, "happy" if level == 6 else "open")
        if level == 7:
            cr = [(c + 0.05 * R, c - 1.1 * R), (c - 0.0 * R, c - 1.5 * R), (c + 0.25 * R, c - 1.3 * R), (c + 0.5 * R, c - 1.65 * R),
                  (c + 0.75 * R, c - 1.3 * R), (c + 1.0 * R, c - 1.5 * R), (c + 0.95 * R, c - 1.1 * R)]
            shape(img, ((255, 255, 210), (255, 220, 60), (215, 145, 0)), lw, lambda md: md.polygon(cr, fill=255))
            d = ImageDraw.Draw(img)
            d.ellipse([c + 0.43 * R, c - 1.32 * R, c + 0.57 * R, c - 1.18 * R], fill=(230, 40, 90, 255), outline=OUT)
            for (sx, sy, ss) in ((-1.25, -0.9, 0.14), (1.3, -0.1, 0.12), (1.25, 0.85, 0.11), (-0.9, -1.2, 0.1)):
                star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """La MÉTÉORITE : caillou en feu aux sourcils froncés."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    # traînée de feu (vers le haut à droite)
    for k, (col, s) in enumerate((((255, 120, 30), 1.0), ((255, 200, 50), 0.7), ((255, 250, 180), 0.4))):
        f = Image.new("RGBA", img.size, (0, 0, 0, 0)); fd = ImageDraw.Draw(f)
        fd.polygon([(c - 0.75 * R * s, c - 0.45 * R * s), (c + 1.55 * R * (0.6 + 0.4 * s), c - 1.55 * R * (0.6 + 0.4 * s)), (c + 0.45 * R * s, c + 0.75 * R * s)], fill=col + (255,))
        img.alpha_composite(f.filter(ImageFilter.GaussianBlur(R * 0.04)))
    rnd = random.Random(3)
    pts = []
    for i in range(14):
        a = i / 14 * 6.283
        rr = 0.8 * R * rnd.uniform(0.88, 1.08)
        pts.append((c - 0.1 * R + rr * math.cos(a), c + 0.15 * R + rr * math.sin(a)))
    m = shape(img, ((190, 170, 160), (125, 105, 95), (70, 55, 50)), lw, lambda md: md.polygon(pts, fill=255))
    spots(img, m, c, R, 7, (60, 45, 40, 160), 5)
    d = ImageDraw.Draw(img)
    cx, cy = c - 0.1 * R, c + 0.1 * R
    for sx in (-1, 1):
        x = cx + sx * 0.28 * R
        d.ellipse([x - 0.15 * R, cy - 0.1 * R, x + 0.15 * R, cy + 0.2 * R], fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=max(2, lw // 2))
        d.ellipse([x - 0.07 * R, cy + 0.0 * R, x + 0.07 * R, cy + 0.14 * R], fill=(10, 10, 10, 255))
        d.line([(x - sx * 0.2 * R, cy - 0.3 * R), (x + sx * 0.15 * R, cy - 0.14 * R)], fill=(20, 20, 20, 255), width=int(0.08 * R))
    d.arc([cx - 0.2 * R, cy + 0.3 * R, cx + 0.2 * R, cy + 0.55 * R], 200, 340, fill=(20, 20, 20, 255), width=int(0.06 * R))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(25, 50, 20, 255), glow=(255, 255, 255)):
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
    sheet = Image.new("RGBA", (W, H), (150, 230, 130, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
