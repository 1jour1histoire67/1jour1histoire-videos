"""JARDIN MERGE (épisode 19) : graine → arbre magique + UNE TONDEUSE ! (rebondissement).
Tous les personnages sont inventés."""
import math
from PIL import Image, ImageDraw, ImageFilter
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("GRAINE",        "Graine",         24),
    ("POUSSE",        "Pousse",         36),
    ("FLEUR",         "Fleur",          50),
    ("TOURNESOL",     "Tournesol",      64),
    ("CACTUS",        "Cactus",         80),
    ("BUISSON",       "Buisson",        98),
    ("ARBRE",         "Arbre",         120),
    ("ARBRE MAGIQUE", "Arbre magique", 150),
]
BOMB_R = 48
OUT = (35, 55, 30, 255)

PINK = ((255, 225, 235), (255, 150, 185), (215, 80, 125))
SUN = ((255, 252, 205), (255, 215, 60), (220, 150, 10))
LEAF = ((215, 255, 200), (110, 205, 90), (40, 130, 45))
DLEAF = ((180, 235, 160), (70, 165, 70), (25, 95, 35))
WOOD = ((235, 190, 140), (175, 115, 60), (105, 65, 25))
SEED = ((250, 230, 195), (215, 165, 100), (150, 100, 45))
CACT = ((210, 250, 210), (95, 190, 120), (35, 120, 65))
POT = ((255, 210, 180), (225, 120, 75), (160, 70, 35))
RED = ((255, 205, 195), (240, 75, 70), (160, 30, 35))
GREY = ((240, 245, 255), (170, 180, 200), (100, 110, 135))
WHITE = ((255, 255, 255), (238, 240, 248), (185, 190, 210))
MAGIC = ((240, 215, 255), (190, 120, 245), (110, 50, 190))
GOLDC = ((255, 250, 200), (255, 205, 55), (210, 130, 0))
SKY = ((215, 235, 255), (110, 165, 245), (45, 90, 190))

def shape(img, cols, lw, draw):
    m = Image.new("L", img.size, 0)
    draw(ImageDraw.Draw(m))
    img.alpha_composite(gradient_fill(img.size, m, *cols))
    if lw == 0:
        return m
    edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(max(3, (lw // 2) * 2 + 1)))
    img.alpha_composite(Image.composite(Image.new("RGBA", img.size, OUT), Image.new("RGBA", img.size, (0, 0, 0, 0)), edge))
    return m


def E(md, x, y, rx, ry):
    md.ellipse([x - rx, y - ry, x + rx, y + ry], fill=255)


def RR(md, x0, y0, x1, y1, r):
    md.rounded_rectangle([x0, y0, x1, y1], r, fill=255)



def petals(img, c, cy, R, n, rp, dist, cols, lw, ang0=0):
    for k in range(n):
        a = ang0 + k / n * 6.283
        x, y = c + dist * R * math.cos(a), cy + dist * R * math.sin(a)
        shape(img, cols, lw, lambda md: E(md, x, y, rp * R, rp * R))


def leaf(img, x, y, R, lw, sx, cols=LEAF, size=0.35):
    shape(img, cols, lw, lambda md: md.ellipse([x + (0 if sx > 0 else -2 * size) * R, y - 0.5 * size * R,
                                               x + (2 * size if sx > 0 else 0) * R, y + 0.5 * size * R], fill=255))


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.7 if level >= 4 else 1.6
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    if level == 0:  # graine : ovale beige avec un petit germe
        shape(img, LEAF, lw, lambda md: md.polygon([(c, c - 0.75 * R), (c + 0.45 * R, c - 1.15 * R), (c + 0.1 * R, c - 0.6 * R)], fill=255))
        shape(img, SEED, lw, lambda md: E(md, c, c + 0.05 * R, 0.8 * R, 0.92 * R))
        draw_face(img, c, c + 0.1 * R, 0.6 * R, "happy")
    elif level == 1:  # pousse : deux feuilles sur une tige, petite motte
        d = ImageDraw.Draw(img)
        shape(img, LEAF, lw, lambda md: RR(md, c - 0.1 * R, c - 0.9 * R, c + 0.1 * R, c + 0.2 * R, 0.08 * R))
        leaf(img, c, c - 0.75 * R, R, lw, 1, size=0.4)
        leaf(img, c, c - 0.75 * R, R, lw, -1, size=0.4)
        shape(img, WOOD, lw, lambda md: E(md, c, c + 0.35 * R, 0.85 * R, 0.6 * R))
        draw_face(img, c, c + 0.35 * R, 0.5 * R, "happy")
    elif level == 2:  # fleur : pétales roses, cœur jaune
        petals(img, c, c, R, 6, 0.38, 0.55, PINK, lw)
        shape(img, SUN, lw, lambda md: E(md, c, c, 0.55 * R, 0.55 * R))
        draw_face(img, c, c + 0.02 * R, 0.42 * R, "happy")
    elif level == 3:  # tournesol : pétales jaunes pointus, cœur brun
        for k in range(14):
            a = k / 14 * 6.283
            pts = [(c + 0.55 * R * math.cos(a - 0.22), c + 0.55 * R * math.sin(a - 0.22)), (c + 1.0 * R * math.cos(a), c + 1.0 * R * math.sin(a)),
                   (c + 0.55 * R * math.cos(a + 0.22), c + 0.55 * R * math.sin(a + 0.22))]
            shape(img, SUN, max(2, lw - 1), lambda md: md.polygon(pts, fill=255))
        shape(img, WOOD, lw, lambda md: E(md, c, c, 0.62 * R, 0.62 * R))
        d = ImageDraw.Draw(img)
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i * i + j * j <= 5:
                    d.ellipse([c + i * 0.2 * R - 0.03 * R, c + j * 0.2 * R - 0.03 * R, c + i * 0.2 * R + 0.03 * R, c + j * 0.2 * R + 0.03 * R], fill=(90, 50, 20, 255))
        draw_face(img, c, c + 0.04 * R, 0.5 * R, "open")
    elif level == 4:  # cactus : vert avec bras, pot terre cuite, fleur rose
        for sx in (-1, 1):
            x0, x1 = (c + 0.3 * R, c + 0.85 * R) if sx > 0 else (c - 0.85 * R, c - 0.3 * R)
            shape(img, CACT, lw, lambda md: RR(md, x0, c - 0.2 * R, x1, c + 0.08 * R, 0.13 * R))
            x = c + sx * 0.72 * R
            shape(img, CACT, lw, lambda md: RR(md, x - 0.14 * R, c - 0.65 * R, x + 0.14 * R, c + 0.05 * R, 0.14 * R))
        shape(img, CACT, lw, lambda md: RR(md, c - 0.45 * R, c - 0.95 * R, c + 0.45 * R, c + 0.6 * R, 0.42 * R))
        shape(img, POT, lw, lambda md: md.polygon([(c - 0.65 * R, c + 0.5 * R), (c + 0.65 * R, c + 0.5 * R), (c + 0.5 * R, c + 1.05 * R), (c - 0.5 * R, c + 1.05 * R)], fill=255))
        d = ImageDraw.Draw(img)
        for (x, y) in ((-0.25, -0.55), (0.25, -0.6), (-0.3, 0.3), (0.3, 0.25), (0, -0.75)):
            d.line([(c + x * R - 0.05 * R, c + y * R), (c + x * R + 0.05 * R, c + y * R)], fill=(255, 255, 230, 255), width=max(2, lw // 2))
        petals(img, c, c - 0.98 * R, R, 5, 0.1, 0.12, PINK, max(2, lw // 2))
        draw_face(img, c, c - 0.1 * R, 0.5 * R, "happy")
    elif level == 5:  # buisson : boules vertes + baies rouges
        for (x, y, s) in ((-0.55, 0.2, 0.5), (0.55, 0.2, 0.5), (-0.3, -0.35, 0.5), (0.3, -0.35, 0.5), (0, 0.25, 0.65)):
            shape(img, DLEAF, lw, lambda md: E(md, c + x * R, c + y * R, s * R, s * R))
        shape(img, LEAF, lw, lambda md: E(md, c, c + 0.05 * R, 0.62 * R, 0.6 * R))
        draw_face(img, c, c + 0.05 * R, 0.55 * R, "happy")
        for (x, y) in ((-0.75, -0.1), (0.75, -0.05), (-0.45, -0.7), (0.5, -0.68), (-0.85, 0.5), (0.85, 0.55)):
            shape(img, RED, max(2, lw // 2), lambda md: E(md, c + x * R, c + y * R, 0.1 * R, 0.1 * R))
    elif level == 6:  # arbre : tronc, grand feuillage, pommes
        shape(img, WOOD, lw, lambda md: RR(md, c - 0.25 * R, c + 0.1 * R, c + 0.25 * R, c + 1.05 * R, 0.08 * R))
        for (x, y, s) in ((-0.5, -0.2, 0.5), (0.5, -0.2, 0.5), (0, -0.6, 0.55), (0, 0.0, 0.6)):
            shape(img, LEAF, lw, lambda md: E(md, c + x * R, c + y * R, s * R, s * R))
        shape(img, LEAF, 0, lambda md: E(md, c, c - 0.2 * R, 0.75 * R, 0.6 * R))
        draw_face(img, c, c - 0.2 * R, 0.55 * R, "happy")
        for (x, y) in ((-0.7, -0.45), (0.72, -0.4), (-0.3, -0.85), (0.4, -0.85), (0.75, 0.15)):
            shape(img, RED, max(2, lw // 2), lambda md: E(md, c + x * R, c + y * R, 0.11 * R, 0.11 * R))
    elif level == 7:  # arbre magique : feuillage violet, rayons, étoiles, couronne
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(18):
            a = k / 18 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.11), c + 0.5 * R * math.sin(a - 0.11)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.11), c + 0.5 * R * math.sin(a + 0.11))], fill=(255, 240, 120, 190) if k % 2 else (255, 170, 230, 190))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        shape(img, GOLDC, lw, lambda md: RR(md, c - 0.22 * R, c + 0.2 * R, c + 0.22 * R, c + 1.0 * R, 0.08 * R))
        for (x, y, s) in ((-0.5, -0.15, 0.48), (0.5, -0.15, 0.48), (0, -0.5, 0.52), (0, 0.05, 0.55)):
            shape(img, MAGIC, lw, lambda md: E(md, c + x * R, c + y * R, s * R, s * R))
        shape(img, MAGIC, 0, lambda md: E(md, c, c - 0.15 * R, 0.7 * R, 0.55 * R))
        d = ImageDraw.Draw(img)
        for (x, y, s) in ((-0.65, -0.35, 0.05), (0.6, -0.4, 0.04), (-0.3, -0.75, 0.04), (0.35, -0.72, 0.05), (0.7, 0.15, 0.04)):
            d.ellipse([c + (x - s) * R, c + (y - s) * R, c + (x + s) * R, c + (y + s) * R], fill=(255, 255, 255, 255))
        draw_face(img, c, c - 0.12 * R, 0.55 * R, "happy")
        shape(img, GOLDC, lw, lambda md: md.polygon(
            [(c - 0.4 * R, c - 0.9 * R), (c - 0.45 * R, c - 1.3 * R), (c - 0.2 * R, c - 1.1 * R), (c, c - 1.4 * R),
             (c + 0.2 * R, c - 1.1 * R), (c + 0.45 * R, c - 1.3 * R), (c + 0.4 * R, c - 0.9 * R)], fill=255))
        for (sx, sy, ss) in ((-1.2, -0.9, 0.16), (1.2, -0.85, 0.14), (1.25, 0.6, 0.12), (-1.25, 0.55, 0.11)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
            star(img, c + sx * R, c + sy * R, ss * 0.55 * R, (255, 120, 200, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """UNE TONDEUSE ! : tondeuse de dessin animé rouge, avec des yeux et un guidon."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    d = ImageDraw.Draw(img)
    d.line([(c + 0.3 * R, c - 0.2 * R), (c + 0.95 * R, c - 1.2 * R)], fill=OUT, width=int(0.14 * R))
    d.line([(c + 0.3 * R, c - 0.2 * R), (c + 0.95 * R, c - 1.2 * R)], fill=(200, 205, 215, 255), width=int(0.08 * R))
    shape(img, GREY, lw, lambda md: RR(md, c + 0.7 * R, c - 1.35 * R, c + 1.25 * R, c - 1.1 * R, 0.1 * R))
    shape(img, RED, lw, lambda md: md.chord([c - 1.0 * R, c - 0.75 * R, c + 1.0 * R, c + 1.05 * R], 180, 360, fill=255))
    shape(img, RED, lw, lambda md: RR(md, c - 1.05 * R, c + 0.05 * R, c + 1.05 * R, c + 0.55 * R, 0.12 * R))
    shape(img, GREY, lw, lambda md: RR(md, c - 0.3 * R, c - 0.85 * R, c + 0.3 * R, c - 0.6 * R, 0.08 * R))
    for sx in (-1, 1):
        shape(img, ((120, 120, 140), (55, 55, 70), (20, 20, 30)), lw, lambda md: E(md, c + sx * 0.65 * R, c + 0.65 * R, 0.32 * R, 0.32 * R))
        shape(img, GREY, max(2, lw // 2), lambda md: E(md, c + sx * 0.65 * R, c + 0.65 * R, 0.12 * R, 0.12 * R))
    draw_face(img, c, c - 0.2 * R, 0.6 * R, "open")
    for (x, y) in ((-1.15, 0.9), (-1.3, 0.6), (1.2, 0.95)):
        leaf(img, c + x * R, c + y * R, R, max(2, lw // 2), 1, size=0.15)
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(30, 90, 160, 255), glow=(255, 255, 255)):
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
    sheet = Image.new("RGBA", (W, H), (230, 248, 170, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
