"""VÉHICULES MERGE (épisode 12) : trottinette → méga fusée + UN RADAR ! (rebondissement).
Tous les personnages sont inventés."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("TROTTINETTE", "Trottinette", 24),
    ("VÉLO",        "Vélo",        36),
    ("SCOOTER",     "Scooter",     50),
    ("VOITURE",     "Voiture",     64),
    ("CAMION",      "Camion",      80),
    ("BUS",         "Bus",         98),
    ("AVION",       "Avion",      120),
    ("MÉGA FUSÉE",  "Méga fusée", 150),
]
BOMB_R = 48
OUT = (30, 30, 50, 255)

GREEN = ((190, 255, 215), (50, 200, 140), (15, 120, 80))
ORANGE = ((255, 215, 150), (255, 145, 30), (205, 85, 0))
MAGENTA = ((255, 190, 240), (230, 80, 200), (150, 25, 125))
RED = ((255, 170, 165), (235, 45, 50), (150, 15, 25))
BLUE = ((180, 215, 255), (60, 130, 230), (25, 65, 160))
YELLOW = ((255, 250, 180), (255, 205, 30), (215, 145, 0))
WHITE = ((255, 255, 255), (235, 242, 252), (175, 190, 215))
PURPLE = ((225, 200, 255), (150, 90, 235), (85, 35, 165))
GLASS = ((235, 250, 255), (170, 220, 250), (100, 165, 220))
TIRE = ((120, 120, 135), (55, 55, 70), (20, 20, 30))
HUB = ((250, 250, 255), (205, 210, 225), (140, 150, 170))
STEEL = ((245, 248, 255), (180, 190, 205), (105, 115, 135))
FLAME = ((255, 255, 200), (255, 190, 40), (240, 90, 20))


def shape(img, cols, lw, draw):
    m = Image.new("L", img.size, 0)
    draw(ImageDraw.Draw(m))
    img.alpha_composite(gradient_fill(img.size, m, *cols))
    edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(max(3, (lw // 2) * 2 + 1)))
    img.alpha_composite(Image.composite(Image.new("RGBA", img.size, OUT), Image.new("RGBA", img.size, (0, 0, 0, 0)), edge))
    return m


def E(md, x, y, rx, ry):
    md.ellipse([x - rx, y - ry, x + rx, y + ry], fill=255)


def RR(md, x0, y0, x1, y1, r):
    md.rounded_rectangle([x0, y0, x1, y1], r, fill=255)


def wheel(img, x, y, rw, lw):
    shape(img, TIRE, lw, lambda md: E(md, x, y, rw, rw))
    shape(img, HUB, max(2, lw // 2), lambda md: E(md, x, y, rw * 0.45, rw * 0.45))


def windows(img, x0, x1, y0, y1, n, lw, gap=0.12):
    w = (x1 - x0) / n
    for k in range(n):
        a, b = x0 + k * w + w * gap, x0 + (k + 1) * w - w * gap
        shape(img, GLASS, max(2, lw // 2), lambda md, a=a, b=b: RR(md, a, y0, b, y1, (b - a) * 0.2))


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.65 if level >= 4 else 1.55
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    d = ImageDraw.Draw(img)
    if level == 0:  # trottinette : plateau, guidon, tête ronde sur le guidon
        shape(img, GREEN, lw, lambda md: (RR(md, c - 1.0 * R, c + 0.55 * R, c + 0.75 * R, c + 0.8 * R, 0.12 * R),
                                           md.polygon([(c + 0.55 * R, c + 0.7 * R), (c + 0.62 * R, c - 0.4 * R), (c + 0.82 * R, c - 0.4 * R), (c + 0.78 * R, c + 0.7 * R)], fill=255),
                                           RR(md, c + 0.35 * R, c - 0.55 * R, c + 1.1 * R, c - 0.38 * R, 0.08 * R)))
        wheel(img, c - 0.8 * R, c + 0.9 * R, 0.25 * R, lw)
        wheel(img, c + 0.75 * R, c + 0.9 * R, 0.25 * R, lw)
        shape(img, GREEN, lw, lambda md: E(md, c - 0.15 * R, c - 0.05 * R, 0.62 * R, 0.55 * R))
        draw_face(img, c - 0.15 * R, c - 0.05 * R, 0.62 * R, "happy")
    elif level == 1:  # vélo
        d.line([(c - 0.6 * R, c + 0.5 * R), (c - 0.05 * R, c - 0.35 * R), (c + 0.6 * R, c + 0.5 * R)], fill=(205, 85, 0, 255), width=int(0.13 * R))
        d.line([(c + 0.6 * R, c + 0.5 * R), (c + 0.5 * R, c - 0.55 * R)], fill=(205, 85, 0, 255), width=int(0.12 * R))
        d.line([(c + 0.35 * R, c - 0.6 * R), (c + 0.75 * R, c - 0.68 * R)], fill=OUT, width=int(0.1 * R))
        shape(img, ((90, 90, 110), (50, 50, 65), (20, 20, 30)), max(2, lw // 2), lambda md: RR(md, c - 0.45 * R, c - 0.55 * R, c + 0.1 * R, c - 0.38 * R, 0.08 * R))
        for x in (-0.6, 0.6):
            xx = c + x * R
            d = ImageDraw.Draw(img)
            d.ellipse([xx - 0.45 * R, c + 0.05 * R, xx + 0.45 * R, c + 0.95 * R], outline=OUT, width=int(0.14 * R))
            d.ellipse([xx - 0.1 * R, c + 0.4 * R, xx + 0.1 * R, c + 0.6 * R], fill=(180, 190, 205, 255))
        shape(img, ORANGE, lw, lambda md: E(md, c, c + 0.05 * R, 0.42 * R, 0.4 * R))
        draw_face(img, c, c + 0.05 * R, 0.45 * R, "happy")
    elif level == 2:  # scooter
        wheel(img, c - 0.62 * R, c + 0.7 * R, 0.3 * R, lw)
        wheel(img, c + 0.62 * R, c + 0.7 * R, 0.3 * R, lw)
        shape(img, MAGENTA, lw, lambda md: (md.polygon([(c - 0.95 * R, c + 0.55 * R), (c - 0.95 * R, c - 0.05 * R), (c - 0.3 * R, c - 0.15 * R),
                                                        (c + 0.2 * R, c + 0.3 * R), (c + 0.35 * R, c - 0.7 * R), (c + 0.85 * R, c - 0.6 * R),
                                                        (c + 0.9 * R, c + 0.55 * R)], fill=255),))
        shape(img, ((100, 90, 110), (55, 45, 65), (25, 20, 30)), max(2, lw // 2), lambda md: RR(md, c - 0.9 * R, c - 0.32 * R, c - 0.2 * R, c - 0.08 * R, 0.1 * R))
        d = ImageDraw.Draw(img)
        d.line([(c + 0.45 * R, c - 0.7 * R), (c + 0.35 * R, c - 1.0 * R), (c + 0.1 * R, c - 1.0 * R)], fill=OUT, width=int(0.08 * R))
        draw_face(img, c + 0.6 * R, c - 0.15 * R, 0.42 * R, "happy")
    elif level == 3:  # voiture rouge
        shape(img, RED, lw, lambda md: (RR(md, c - 1.05 * R, c - 0.2 * R, c + 1.05 * R, c + 0.55 * R, 0.25 * R),
                                         md.chord([c - 0.65 * R, c - 0.9 * R, c + 0.65 * R, c + 0.5 * R], 180, 360, fill=255)))
        windows(img, c - 0.52 * R, c + 0.52 * R, c - 0.68 * R, c - 0.25 * R, 2, lw)
        wheel(img, c - 0.6 * R, c + 0.6 * R, 0.3 * R, lw)
        wheel(img, c + 0.6 * R, c + 0.6 * R, 0.3 * R, lw)
        d = ImageDraw.Draw(img)
        d.ellipse([c + 0.85 * R, c - 0.08 * R, c + 1.02 * R, c + 0.1 * R], fill=(255, 245, 160, 255))
        draw_face(img, c, c + 0.12 * R, 0.6 * R, "happy")
    elif level == 4:  # camion
        shape(img, ((235, 240, 250), (200, 210, 225), (130, 140, 165)), lw, lambda md: RR(md, c - 1.1 * R, c - 0.8 * R, c + 0.25 * R, c + 0.5 * R, 0.08 * R))
        shape(img, BLUE, lw, lambda md: md.polygon([(c + 0.3 * R, c + 0.5 * R), (c + 0.3 * R, c - 0.65 * R), (c + 0.8 * R, c - 0.65 * R),
                                                     (c + 1.1 * R, c - 0.1 * R), (c + 1.1 * R, c + 0.5 * R)], fill=255))
        shape(img, GLASS, max(2, lw // 2), lambda md: md.polygon([(c + 0.42 * R, c - 0.08 * R), (c + 0.42 * R, c - 0.53 * R), (c + 0.74 * R, c - 0.53 * R), (c + 0.98 * R, c - 0.08 * R)], fill=255))
        d = ImageDraw.Draw(img)
        d.text((c - 0.95 * R, c - 0.55 * R), "", fill=OUT)
        for k in range(3):
            y = c - 0.55 * R + k * 0.3 * R
            d.line([(c - 0.95 * R, y), (c + 0.1 * R, y)], fill=(170, 180, 200, 255), width=max(2, lw // 2))
        for x in (-0.75, -0.35, 0.75):
            wheel(img, c + x * R, c + 0.6 * R, 0.25 * R, lw)
        draw_face(img, c - 0.42 * R, c - 0.1 * R, 0.7 * R, "open")
    elif level == 5:  # bus jaune
        shape(img, YELLOW, lw, lambda md: RR(md, c - 1.1 * R, c - 0.75 * R, c + 1.1 * R, c + 0.55 * R, 0.22 * R))
        windows(img, c - 0.98 * R, c + 0.55 * R, c - 0.6 * R, c - 0.2 * R, 4, lw)
        shape(img, GLASS, max(2, lw // 2), lambda md: RR(md, c + 0.65 * R, c - 0.6 * R, c + 1.0 * R, c + 0.05 * R, 0.08 * R))
        d = ImageDraw.Draw(img)
        d.line([(c - 1.05 * R, c + 0.05 * R), (c + 1.05 * R, c + 0.05 * R)], fill=(40, 40, 60, 255), width=max(3, lw))
        wheel(img, c - 0.62 * R, c + 0.6 * R, 0.27 * R, lw)
        wheel(img, c + 0.62 * R, c + 0.6 * R, 0.27 * R, lw)
        draw_face(img, c - 0.2 * R, c + 0.3 * R, 0.5 * R, "happy")
    elif level == 6:  # avion
        shape(img, BLUE, lw, lambda md: md.polygon([(c - 0.85 * R, c - 0.05 * R), (c - 1.1 * R, c - 0.95 * R), (c - 0.75 * R, c - 0.95 * R), (c - 0.35 * R, c - 0.1 * R)], fill=255))
        shape(img, WHITE, lw, lambda md: (RR(md, c - 1.1 * R, c - 0.35 * R, c + 0.6 * R, c + 0.3 * R, 0.3 * R),
                                           E(md, c + 0.6 * R, c - 0.02 * R, 0.5 * R, 0.33 * R)))
        shape(img, BLUE, lw, lambda md: md.polygon([(c - 0.3 * R, c + 0.05 * R), (c + 0.25 * R, c + 0.05 * R), (c - 0.25 * R, c + 0.85 * R), (c - 0.6 * R, c + 0.85 * R)], fill=255))
        d = ImageDraw.Draw(img)
        for k in range(4):
            x = c - 0.85 * R + k * 0.25 * R
            d.ellipse([x - 0.07 * R, c - 0.22 * R, x + 0.07 * R, c - 0.08 * R], fill=(120, 175, 225, 255), outline=OUT, width=max(2, lw // 3))
        d.line([(c - 1.05 * R, c + 0.1 * R), (c + 1.0 * R, c + 0.1 * R)], fill=(60, 130, 230, 255), width=max(3, lw))
        draw_face(img, c + 0.6 * R, c - 0.05 * R, 0.45 * R, "open")
    elif level == 7:  # méga fusée : halo, flammes, hublot-visage, couronne d'étoiles
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(16):
            a = k / 16 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.12), c + 0.5 * R * math.sin(a - 0.12)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.12), c + 0.5 * R * math.sin(a + 0.12))], fill=(255, 240, 130, 210) if k % 2 else (200, 170, 255, 210))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        shape(img, FLAME, lw, lambda md: md.polygon([(c - 0.35 * R, c + 0.7 * R), (c - 0.25 * R, c + 1.15 * R), (c - 0.1 * R, c + 1.0 * R), (c, c + 1.4 * R),
                                                      (c + 0.1 * R, c + 1.0 * R), (c + 0.25 * R, c + 1.15 * R), (c + 0.35 * R, c + 0.7 * R)], fill=255))
        for sx in (-1, 1):
            shape(img, RED, lw, lambda md, sx=sx: md.polygon([(c + sx * 0.38 * R, c + 0.05 * R), (c + sx * 0.85 * R, c + 0.6 * R), (c + sx * 0.85 * R, c + 0.95 * R), (c + sx * 0.38 * R, c + 0.7 * R)], fill=255))
        shape(img, WHITE, lw, lambda md: (E(md, c, c + 0.05 * R, 0.48 * R, 1.0 * R),))
        shape(img, PURPLE, lw, lambda md: md.chord([c - 0.48 * R, c - 0.95 * R, c + 0.48 * R, c - 0.15 * R], 180, 360, fill=255))
        shape(img, PURPLE, max(2, lw // 2), lambda md: RR(md, c - 0.42 * R, c + 0.55 * R, c + 0.42 * R, c + 0.72 * R, 0.06 * R))
        shape(img, STEEL, lw, lambda md: E(md, c, c + 0.08 * R, 0.36 * R, 0.36 * R))
        shape(img, GLASS, max(2, lw // 2), lambda md: E(md, c, c + 0.08 * R, 0.29 * R, 0.29 * R))
        draw_face(img, c, c + 0.08 * R, 0.3 * R, "open")
        for (sx, sy, ss) in ((-1.15, -0.9, 0.16), (1.15, -0.85, 0.14), (1.2, 0.5, 0.12), (-1.2, 0.45, 0.11), (0, -1.3, 0.13)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
            star(img, c + sx * R, c + sy * R, ss * 0.55 * R, (255, 220, 80, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """UN RADAR ! : boîtier gris sur poteau, objectif et flash, l'air sévère."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    d = ImageDraw.Draw(img)
    for k in range(7):
        a = math.radians(-160 + k * 23)
        d.line([(c + 0.95 * R * math.cos(a), c - 0.35 * R + 0.95 * R * math.sin(a)), (c + 1.5 * R * math.cos(a), c - 0.35 * R + 1.5 * R * math.sin(a))],
               fill=(255, 245, 120, 255), width=int(0.1 * R))
    shape(img, STEEL, lw, lambda md: RR(md, c - 0.12 * R, c + 0.2 * R, c + 0.12 * R, c + 1.2 * R, 0.05 * R))
    shape(img, ((150, 155, 170), (95, 100, 120), (50, 55, 70)), lw, lambda md: RR(md, c - 0.85 * R, c - 0.9 * R, c + 0.85 * R, c + 0.35 * R, 0.15 * R))
    shape(img, ((255, 250, 200), (255, 230, 80), (230, 170, 0)), max(2, lw // 2), lambda md: RR(md, c - 0.75 * R, c - 0.82 * R, c + 0.75 * R, c - 0.55 * R, 0.08 * R))
    shape(img, ((90, 90, 110), (30, 30, 45), (5, 5, 15)), lw, lambda md: E(md, c, c - 0.1 * R, 0.32 * R, 0.32 * R))
    d = ImageDraw.Draw(img)
    d.ellipse([c - 0.15 * R, c - 0.25 * R, c - 0.02 * R, c - 0.12 * R], fill=(255, 255, 255, 230))
    for sx in (-1, 1):
        x = c + sx * 0.58 * R; cy = c - 0.2 * R
        d.ellipse([x - 0.13 * R, cy - 0.1 * R, x + 0.13 * R, cy + 0.16 * R], fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=max(2, lw // 2))
        d.ellipse([x - 0.06 * R, cy - 0.02 * R, x + 0.06 * R, cy + 0.11 * R], fill=(10, 10, 10, 255))
        d.line([(x - sx * 0.2 * R, cy - 0.3 * R), (x + sx * 0.15 * R, cy - 0.12 * R)], fill=(20, 20, 20, 255), width=int(0.07 * R))
    d.arc([c - 0.2 * R, c + 0.15 * R, c + 0.2 * R, c + 0.32 * R], 200, 340, fill=(20, 20, 20, 255), width=int(0.06 * R))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(20, 50, 90, 255), glow=(255, 255, 255)):
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
    sheet = Image.new("RGBA", (W, H), (125, 205, 255, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
