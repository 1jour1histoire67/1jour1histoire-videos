"""ÉCOLE MERGE (épisode 9) : gomme → proviseur suprême + INTERRO SURPRISE (rebondissement).
Tous les personnages sont inventés."""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("GOMME",              "Gomme",              24),
    ("CRAYON",             "Crayon",             36),
    ("CAHIER",             "Cahier",             50),
    ("TROUSSE",            "Trousse",            64),
    ("CARTABLE",           "Cartable",           80),
    ("PION",               "Pion",               98),
    ("PROF",               "Prof",              120),
    ("PROVISEUR SUPRÊME",  "Proviseur suprême", 150),
]
BOMB_R = 46
OUT = (35, 30, 50, 255)

PINK = ((255, 205, 220), (245, 130, 165), (190, 60, 100))
YELLOW = ((255, 245, 170), (255, 205, 50), (210, 140, 0))
BLUE = ((180, 220, 255), (70, 140, 240), (30, 70, 170))
GREEN = ((190, 250, 170), (80, 195, 100), (30, 120, 60))
RED = ((255, 175, 160), (235, 70, 60), (150, 25, 30))
PURPLE = ((225, 195, 255), (150, 95, 230), (90, 45, 160))
TEAL = ((170, 250, 235), (40, 180, 165), (15, 110, 105))
GOLD = ((255, 250, 185), (255, 200, 40), (200, 130, 0))
SKIN = ((255, 235, 210), (250, 205, 165), (215, 155, 115))
WOOD = ((255, 230, 190), (235, 190, 130), (185, 130, 70))
WHITE = ((255, 255, 255), (245, 245, 250), (200, 205, 220))
DARK = ((120, 110, 130), (70, 60, 80), (35, 30, 45))


def shape(img, cols, lw, draw):
    m = Image.new("L", img.size, 0)
    draw(ImageDraw.Draw(m))
    img.alpha_composite(gradient_fill(img.size, m, *cols))
    edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(max(3, (lw // 2) * 2 + 1)))
    img.alpha_composite(Image.composite(Image.new("RGBA", img.size, OUT), Image.new("RGBA", img.size, (0, 0, 0, 0)), edge))
    return m


def small_text(img, xy, txt, sz, fill=(35, 30, 50, 255)):
    from PIL import ImageFont
    f = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", sz)
    ImageDraw.Draw(img).text(xy, txt, font=f, fill=fill, anchor="mm", stroke_width=max(1, sz // 14), stroke_fill=(255, 255, 255, 255))


def E(md, x, y, rx, ry):
    md.ellipse([x - rx, y - ry, x + rx, y + ry], fill=255)


def RR(md, x0, y0, x1, y1, r):
    md.rounded_rectangle([x0, y0, x1, y1], r, fill=255)


def glasses(d, cx, cy, s, lw):
    for sx in (-1, 1):
        x = cx + sx * 0.37 * s
        d.ellipse([x - 0.26 * s, cy - 0.27 * s, x + 0.26 * s, cy + 0.2 * s], outline=OUT, width=lw)
    d.line([(cx - 0.11 * s, cy - 0.08 * s), (cx + 0.11 * s, cy - 0.08 * s)], fill=OUT, width=lw)


def person(img, c, R, lw, body_cols, hy=-0.45, hr=0.62, face="happy"):
    """Corps arrondi + grosse tête ; renvoie (hx, hy) du centre de tête."""
    shape(img, body_cols, lw, lambda md: RR(md, c - 0.8 * R, c + 0.05 * R, c + 0.8 * R, c + 1.15 * R, 0.45 * R))
    hx, hyy = c, c + hy * R
    shape(img, SKIN, lw, lambda md: E(md, hx, hyy, hr * R, hr * R * 0.95))
    return hx, hyy


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.65 if level >= 4 else 1.45
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    d = ImageDraw.Draw(img)
    if level == 0:  # gomme rose avec bande bleue
        shape(img, PINK, lw, lambda md: RR(md, c - 1.0 * R, c - 0.7 * R, c + 1.0 * R, c + 0.75 * R, 0.3 * R))
        shape(img, BLUE, max(2, lw // 2), lambda md: md.rectangle([c + 0.35 * R, c - 0.7 * R, c + 1.0 * R, c + 0.75 * R], fill=255))
        shape(img, PINK, lw, lambda md: RR(md, c - 1.0 * R, c - 0.7 * R, c + 0.4 * R, c + 0.75 * R, 0.3 * R))
        draw_face(img, c - 0.3 * R, c + 0.0 * R, 0.85 * R, "happy")
    elif level == 1:  # crayon jaune incliné
        ang = math.radians(-35)
        ca, sa = math.cos(ang), math.sin(ang)
        P = lambda u, v: (c + u * ca - v * sa, c + u * sa + v * ca)
        w = 0.5 * R
        shape(img, PINK, lw, lambda md: md.polygon([P(-1.35 * R, -w), P(-1.0 * R, -w), P(-1.0 * R, w), P(-1.35 * R, w)], fill=255))
        shape(img, ((235, 235, 240), (190, 190, 205), (120, 120, 140)), max(2, lw // 2), lambda md: md.polygon([P(-1.05 * R, -w), P(-0.8 * R, -w), P(-0.8 * R, w), P(-1.05 * R, w)], fill=255))
        shape(img, WOOD, lw, lambda md: md.polygon([P(0.75 * R, -w), P(1.45 * R, 0), P(0.75 * R, w)], fill=255))
        shape(img, DARK, max(2, lw // 2), lambda md: md.polygon([P(1.22 * R, -0.16 * R), P(1.48 * R, 0), P(1.22 * R, 0.16 * R)], fill=255))
        shape(img, YELLOW, lw, lambda md: md.polygon([P(-0.82 * R, -w), P(0.8 * R, -w), P(0.8 * R, w), P(-0.82 * R, w)], fill=255))
        draw_face(img, c, c, 0.62 * R, "open")
    elif level == 2:  # cahier bleu à spirale
        shape(img, BLUE, lw, lambda md: RR(md, c - 0.85 * R, c - 1.05 * R, c + 0.95 * R, c + 1.05 * R, 0.12 * R))
        shape(img, WHITE, max(2, lw // 2), lambda md: RR(md, c - 0.45 * R, c - 0.72 * R, c + 0.7 * R, c - 0.3 * R, 0.08 * R))
        for k in range(7):
            y = c - 0.88 * R + k * 0.29 * R
            d.ellipse([c - 1.05 * R, y - 0.08 * R, c - 0.7 * R, y + 0.08 * R], outline=(110, 110, 125, 255), width=max(2, lw // 2))
        d.line([(c - 0.35 * R, c - 0.51 * R), (c + 0.55 * R, c - 0.51 * R)], fill=(70, 140, 240, 255), width=max(2, lw // 3))
        draw_face(img, c + 0.1 * R, c + 0.3 * R, 0.75 * R, "happy")
    elif level == 3:  # trousse verte à fermeture éclair, crayons qui dépassent
        for k, (dx, col) in enumerate(((-0.55, RED), (-0.15, YELLOW), (0.3, PURPLE))):
            shape(img, col, max(2, lw // 2), lambda md, dx=dx: md.polygon([(c + dx * R - 0.13 * R, c - 0.2 * R), (c + dx * R - 0.13 * R, c - 0.95 * R), (c + dx * R, c - 1.18 * R), (c + dx * R + 0.13 * R, c - 0.95 * R), (c + dx * R + 0.13 * R, c - 0.2 * R)], fill=255))
        shape(img, GREEN, lw, lambda md: (E(md, c, c + 0.2 * R, 1.15 * R, 0.68 * R)))
        d = ImageDraw.Draw(img)
        d.arc([c - 1.0 * R, c - 0.45 * R, c + 1.0 * R, c + 0.35 * R], 200, 340, fill=(240, 240, 240, 255), width=max(3, lw))
        for k in range(9):
            a = math.radians(205 + k * 15)
            x, y = c + 1.0 * R * math.cos(a), c - 0.05 * R + 0.4 * R * math.sin(a)
            d.line([(x, y - 0.06 * R), (x, y + 0.06 * R)], fill=OUT, width=max(2, lw // 3))
        d.ellipse([c + 0.78 * R, c - 0.32 * R, c + 0.98 * R, c - 0.12 * R], fill=(255, 215, 60, 255), outline=OUT, width=max(2, lw // 3))
        draw_face(img, c, c + 0.3 * R, 0.75 * R, "happy")
    elif level == 4:  # cartable rouge
        shape(img, DARK, lw, lambda md: md.arc([c - 0.5 * R, c - 1.25 * R, c + 0.5 * R, c - 0.45 * R], 180, 360, fill=255, width=int(0.17 * R)))
        shape(img, RED, lw, lambda md: RR(md, c - 1.05 * R, c - 0.75 * R, c + 1.05 * R, c + 1.0 * R, 0.25 * R))
        shape(img, ((255, 140, 125), (215, 50, 45), (130, 20, 25)), lw, lambda md: md.rounded_rectangle([c - 1.05 * R, c - 0.75 * R, c + 1.05 * R, c - 0.05 * R], 0.25 * R, fill=255))
        for sx in (-1, 1):
            shape(img, GOLD, max(2, lw // 2), lambda md, sx=sx: RR(md, c + sx * 0.55 * R - 0.15 * R, c - 0.2 * R, c + sx * 0.55 * R + 0.15 * R, c + 0.12 * R, 0.04 * R))
        draw_face(img, c, c + 0.45 * R, 0.75 * R, "open")
    elif level == 5:  # pion : surveillant inventé, casquette + sifflet
        hx, hy = person(img, c, R, lw, PURPLE, hy=-0.35, hr=0.6)
        d = ImageDraw.Draw(img)
        shape(img, TEAL, lw, lambda md: (md.chord([hx - 0.62 * R, hy - 0.95 * R, hx + 0.62 * R, hy + 0.15 * R], 180, 360, fill=255), RR(md, hx - 0.1 * R, hy - 0.45 * R, hx + 1.0 * R, hy - 0.3 * R, 0.07 * R)))
        draw_face(img, hx, hy + 0.05 * R, 0.55 * R, "happy")
        # sifflet
        d = ImageDraw.Draw(img)
        d.line([(hx - 0.3 * R, hy + 0.5 * R), (hx + 0.1 * R, c + 0.5 * R), (hx + 0.35 * R, hy + 0.5 * R)], fill=(250, 250, 250, 255), width=max(2, lw // 2))
        shape(img, GOLD, max(2, lw // 2), lambda md: RR(md, hx + 0.0 * R, c + 0.42 * R, hx + 0.38 * R, c + 0.62 * R, 0.08 * R))
        star(img, c - 0.45 * R, c + 0.65 * R, 0.17 * R, (255, 230, 90, 255))
    elif level == 6:  # prof : chignon, lunettes, règle
        shape(img, ((150, 110, 90), (110, 70, 50), (70, 40, 25)), lw, lambda md: E(md, c, c - 1.08 * R, 0.3 * R, 0.25 * R))
        hx, hy = person(img, c, R, lw, TEAL, hy=-0.4, hr=0.62)
        shape(img, ((150, 110, 90), (110, 70, 50), (70, 40, 25)), lw, lambda md: md.chord([hx - 0.64 * R, hy - 0.65 * R, hx + 0.64 * R, hy + 0.2 * R], 180, 360, fill=255))
        draw_face(img, hx, hy + 0.12 * R, 0.55 * R, "open")
        glasses(ImageDraw.Draw(img), hx, hy + 0.12 * R, 0.55 * R, max(2, lw // 2))
        # règle
        ang = math.radians(-50)
        ca, sa = math.cos(ang), math.sin(ang)
        bx, by = c + 0.75 * R, c + 0.55 * R
        P = lambda u, v: (bx + u * ca - v * sa, by + u * sa + v * ca)
        shape(img, YELLOW, max(2, lw // 2), lambda md: md.polygon([P(0, -0.11 * R), P(1.2 * R, -0.11 * R), P(1.2 * R, 0.11 * R), P(0, 0.11 * R)], fill=255))
        d = ImageDraw.Draw(img)
        for k in range(1, 8):
            d.line([P(k * 0.15 * R, -0.11 * R), P(k * 0.15 * R, 0.0)], fill=OUT, width=max(1, lw // 3))
        shape(img, SKIN, max(2, lw // 2), lambda md: E(md, bx, by, 0.16 * R, 0.16 * R))
    elif level == 7:  # proviseur suprême : doré, toque de diplômé, cape, rayons
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(16):
            a = k / 16 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.12), c + 0.5 * R * math.sin(a - 0.12)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.12), c + 0.5 * R * math.sin(a + 0.12))], fill=(255, 240, 120, 210) if k % 2 else (120, 210, 255, 210))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        shape(img, ((200, 160, 255), (120, 60, 210), (70, 25, 140)), lw, lambda md: md.polygon([(c - 0.55 * R, c - 0.1 * R), (c - 1.2 * R, c + 1.15 * R), (c + 1.2 * R, c + 1.15 * R), (c + 0.55 * R, c - 0.1 * R)], fill=255))
        hx, hy = person(img, c, R, lw, GOLD, hy=-0.3, hr=0.6)
        # moustache + lunettes
        draw_face(img, hx, hy + 0.08 * R, 0.55 * R, "open")
        d = ImageDraw.Draw(img)
        glasses(d, hx, hy + 0.08 * R, 0.55 * R, max(2, lw // 2))
        # toque
        shape(img, DARK, lw, lambda md: RR(md, hx - 0.42 * R, hy - 0.78 * R, hx + 0.42 * R, hy - 0.45 * R, 0.05 * R))
        shape(img, DARK, lw, lambda md: md.polygon([(hx - 0.95 * R, hy - 0.82 * R), (hx, hy - 1.12 * R), (hx + 0.95 * R, hy - 0.82 * R), (hx, hy - 0.55 * R)], fill=255))
        d = ImageDraw.Draw(img)
        d.line([(hx, hy - 0.84 * R), (hx + 0.75 * R, hy - 0.8 * R), (hx + 0.78 * R, hy - 0.35 * R)], fill=(255, 210, 40, 255), width=max(3, lw // 2 + 1))
        d.ellipse([hx + 0.7 * R, hy - 0.4 * R, hx + 0.86 * R, hy - 0.2 * R], fill=(255, 210, 40, 255), outline=OUT, width=max(1, lw // 3))
        # médaille 20/20
        shape(img, ((255, 255, 210), (255, 220, 60), (215, 145, 0)), max(2, lw // 2), lambda md: E(md, c, c + 0.62 * R, 0.3 * R, 0.3 * R))
        small_text(img, (c, c + 0.62 * R), "20", int(0.28 * R))
        for (sx, sy, ss) in ((-1.25, -0.9, 0.14), (1.3, -0.1, 0.12), (1.25, 0.85, 0.11), (-1.0, 0.6, 0.1)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """L'INTERRO SURPRISE : feuille qui fronce les sourcils, avec un gros point d'interrogation rouge."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    # lignes de vitesse
    d = ImageDraw.Draw(img)
    for k in range(3):
        y = c - 0.6 * R + k * 0.5 * R
        d.line([(c + 1.0 * R, y), (c + 1.6 * R, y - 0.4 * R)], fill=(255, 255, 255, 230), width=int(0.08 * R))
    pts = [(c - 0.8 * R, c - 1.05 * R), (c + 0.55 * R, c - 1.05 * R), (c + 0.85 * R, c - 0.75 * R), (c + 0.85 * R, c + 1.05 * R), (c - 0.8 * R, c + 1.05 * R)]
    shape(img, WHITE, lw, lambda md: md.polygon(pts, fill=255))
    d = ImageDraw.Draw(img)
    d.polygon([(c + 0.55 * R, c - 1.05 * R), (c + 0.55 * R, c - 0.75 * R), (c + 0.85 * R, c - 0.75 * R)], fill=(210, 215, 230, 255), outline=OUT)
    for k in range(6):
        y = c - 0.55 * R + k * 0.28 * R
        d.line([(c - 0.65 * R, y), (c + 0.7 * R, y)], fill=(150, 190, 240, 255), width=max(2, lw // 3))
    d.line([(c - 0.5 * R, c - 1.05 * R), (c - 0.5 * R, c + 1.05 * R)], fill=(240, 120, 140, 255), width=max(2, lw // 3))
    small_text(img, (c + 0.45 * R, c + 0.6 * R), "?", int(0.9 * R), fill=(230, 40, 40, 255))
    cx, cy = c - 0.1 * R, c - 0.3 * R
    for sx in (-1, 1):
        x = cx + sx * 0.28 * R
        d.ellipse([x - 0.15 * R, cy - 0.1 * R, x + 0.15 * R, cy + 0.2 * R], fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=max(2, lw // 2))
        d.ellipse([x - 0.07 * R, cy + 0.0 * R, x + 0.07 * R, cy + 0.14 * R], fill=(10, 10, 10, 255))
        d.line([(x - sx * 0.2 * R, cy - 0.3 * R), (x + sx * 0.15 * R, cy - 0.14 * R)], fill=(20, 20, 20, 255), width=int(0.08 * R))
    d.arc([cx - 0.2 * R, cy + 0.3 * R, cx + 0.2 * R, cy + 0.55 * R], 200, 340, fill=(20, 20, 20, 255), width=int(0.06 * R))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(20, 50, 60, 255), glow=(255, 255, 255)):
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
    sheet = Image.new("RGBA", (W, H), (110, 215, 225, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
