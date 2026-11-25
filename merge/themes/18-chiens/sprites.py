"""CHIENS MERGE (épisode 18) : chiot → chien cosmique + LE VÉTÉRINAIRE ! (rebondissement).
Tous les personnages sont inventés."""
import math
from PIL import Image, ImageDraw, ImageFilter
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("CHIOT",          "Chiot",          24),
    ("TECKEL",         "Teckel",         36),
    ("CANICHE",        "Caniche",        50),
    ("BEAGLE",         "Beagle",         64),
    ("HUSKY",          "Husky",          80),
    ("LABRADOR",       "Labrador",       98),
    ("SAINT-BERNARD",  "Saint-Bernard", 120),
    ("CHIEN COSMIQUE", "Chien cosmique", 150),
]
BOMB_R = 48
OUT = (40, 35, 70, 255)

PINK = ((255, 225, 235), (255, 160, 190), (215, 90, 130))
SUN = ((255, 250, 200), (255, 210, 80), (215, 150, 20))
GRAPE = ((235, 215, 255), (170, 125, 240), (100, 60, 180))
SKY = ((215, 235, 255), (110, 165, 245), (45, 90, 190))
MINT = ((215, 255, 225), (120, 215, 150), (45, 145, 85))
PEACH = ((255, 235, 215), (245, 190, 150), (195, 120, 80))
CREAM = ((255, 250, 240), (235, 220, 200), (175, 155, 130))
GOLDC = ((255, 250, 200), (255, 205, 55), (210, 130, 0))
WHITE = ((255, 255, 255), (238, 240, 248), (185, 190, 210))
RED = ((255, 205, 195), (235, 85, 70), (160, 35, 35))
DARK = ((120, 120, 150), (60, 60, 85), (25, 25, 40))
WOOD = ((235, 190, 140), (180, 115, 60), (110, 65, 25))
BROWN = ((200, 150, 110), (140, 90, 50), (80, 45, 20))


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


def glasses(img, cx, cy, s, lw, col=(40, 30, 50, 255)):
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        x = cx + sx * 0.37 * s
        d.ellipse([x - 0.25 * s, cy - 0.22 * s, x + 0.25 * s, cy + 0.18 * s], outline=col, width=max(2, lw // 2))
    d.line([(cx - 0.12 * s, cy - 0.06 * s), (cx + 0.12 * s, cy - 0.06 * s)], fill=col, width=max(2, lw // 2))


def mustache(img, cx, cy, s, lw, cols=WHITE):
    for sx in (-1, 1):
        shape(img, cols, max(2, lw // 2), lambda md: md.ellipse(
            [cx + (0.0 if sx > 0 else -0.6) * s, cy - 0.1 * s, cx + (0.6 if sx > 0 else -0.0) * s, cy + 0.2 * s], fill=255))


def beard(img, c, R, lw, top, length, cols=WHITE):
    shape(img, cols, lw, lambda md: md.polygon(
        [(c - 0.62 * R, top), (c + 0.62 * R, top), (c + 0.5 * R, top + 0.45 * length), (c + 0.18 * R, top + length),
         (c, top + 0.85 * length), (c - 0.18 * R, top + length), (c - 0.5 * R, top + 0.45 * length)], fill=255))


TAN = ((255, 240, 215), (240, 200, 150), (190, 135, 85))
GREY = ((240, 245, 255), (170, 180, 200), (100, 110, 135))
BLACK = ((140, 130, 140), (70, 60, 70), (30, 25, 30))
GALAXY = ((230, 200, 255), (150, 100, 240), (80, 40, 170))


def nose(img, c, y, s, lw):
    shape(img, BLACK, max(2, lw // 2), lambda md: E(md, c, y, 0.17 * s, 0.11 * s))
    d = ImageDraw.Draw(img)
    d.ellipse([c - 0.07 * s, y - 0.07 * s, c - 0.01 * s, y - 0.03 * s], fill=(255, 255, 255, 230))


def tongue(img, c, y, s, lw):
    shape(img, ((255, 200, 210), (250, 120, 150), (200, 60, 90)), max(2, lw // 2), lambda md: md.rounded_rectangle([c - 0.11 * s, y, c + 0.11 * s, y + 0.28 * s], 0.1 * s, fill=255))


def floppy(img, c, cy, R, lw, cols, w=0.32, h=0.75, dx=0.78, top=-0.55):
    for sx in (-1, 1):
        x = c + sx * dx * R
        shape(img, cols, lw, lambda md: md.ellipse([x - w * R, cy + top * R, x + w * R, cy + (top + 2 * h) * R], fill=255))


def pointy(img, c, cy, R, lw, cols, inner=None):
    for sx in (-1, 1):
        pts = [(c + sx * 0.25 * R, cy - 0.6 * R), (c + sx * 0.72 * R, cy - 1.25 * R), (c + sx * 0.85 * R, cy - 0.3 * R)]
        shape(img, cols, lw, lambda md: md.polygon(pts, fill=255))
        if inner:
            p2 = [(c + sx * 0.4 * R, cy - 0.6 * R), (c + sx * 0.7 * R, cy - 1.05 * R), (c + sx * 0.76 * R, cy - 0.45 * R)]
            ImageDraw.Draw(img).polygon(p2, fill=inner)


def face(img, c, cy, R, lw, mood="happy", tg=True):
    draw_face(img, c, cy, 0.62 * R, mood)
    nose(img, c, cy + 0.12 * R, R, lw)
    if tg:
        tongue(img, c, cy + 0.25 * R, R, lw)


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.7 if level >= 4 else 1.6
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    if level == 0:  # chiot : beige, petites oreilles tombantes, langue
        floppy(img, c, c, R, lw, BROWN, w=0.28, h=0.4, dx=0.75, top=-0.7)
        shape(img, TAN, lw, lambda md: E(md, c, c + 0.05 * R, 0.9 * R, 0.88 * R))
        face(img, c, c, R, lw)
    elif level == 1:  # teckel : marron, corps saucisse, longues oreilles
        shape(img, WOOD, lw, lambda md: RR(md, c - 1.25 * R, c + 0.2 * R, c + 1.25 * R, c + 0.85 * R, 0.33 * R))
        floppy(img, c, c, R, lw, BROWN, w=0.26, h=0.6, dx=0.7, top=-0.5)
        shape(img, WOOD, lw, lambda md: E(md, c, c - 0.05 * R, 0.75 * R, 0.72 * R))
        face(img, c, c - 0.1 * R, R * 0.9, lw)
    elif level == 2:  # caniche : rose pâle, toupet bouclé, oreilles pompons
        for sx in (-1, 1):
            for k in range(3):
                shape(img, PINK, lw, lambda md: E(md, c + sx * 0.85 * R, c - 0.2 * R + k * 0.3 * R, 0.25 * R, 0.22 * R))
        shape(img, WHITE, lw, lambda md: E(md, c, c + 0.1 * R, 0.78 * R, 0.8 * R))
        for x in (-0.45, 0, 0.45):
            shape(img, PINK, lw, lambda md: E(md, c + x * R, c - 0.68 * R - (0.12 * R if x == 0 else 0), 0.32 * R, 0.3 * R))
        face(img, c, c + 0.1 * R, R * 0.95, lw)
        shape(img, SKY, max(2, lw - 1), lambda md: md.polygon([(c + 0.3 * R, c - 0.95 * R), (c + 0.75 * R, c - 1.1 * R), (c + 0.75 * R, c - 0.8 * R)], fill=255))
    elif level == 3:  # beagle : tricolore, oreilles marron, tache noire
        floppy(img, c, c, R, lw, WOOD, w=0.3, h=0.62, dx=0.82, top=-0.45)
        shape(img, WHITE, lw, lambda md: E(md, c, c + 0.08 * R, 0.82 * R, 0.86 * R))
        d = ImageDraw.Draw(img)
        d.pieslice([c - 0.78 * R, c - 0.76 * R, c + 0.78 * R, c + 0.5 * R], 195, 345, fill=(185, 120, 60, 255))
        d.ellipse([c - 0.12 * R, c - 0.75 * R, c + 0.12 * R, c + 0.05 * R], fill=(255, 255, 255, 255))
        face(img, c, c + 0.1 * R, R, lw, "open", tg=False)
    elif level == 4:  # husky : gris, masque blanc, oreilles pointues
        pointy(img, c, c, R, lw, GREY, inner=(255, 190, 200, 255))
        shape(img, GREY, lw, lambda md: E(md, c, c + 0.08 * R, 0.88 * R, 0.86 * R))
        shape(img, WHITE, max(2, lw - 1), lambda md: md.polygon([(c - 0.7 * R, c + 0.05 * R), (c - 0.35 * R, c - 0.25 * R), (c, c - 0.45 * R),
                                                                 (c + 0.35 * R, c - 0.25 * R), (c + 0.7 * R, c + 0.05 * R), (c + 0.55 * R, c + 0.7 * R),
                                                                 (c, c + 0.9 * R), (c - 0.55 * R, c + 0.7 * R)], fill=255))
        face(img, c, c + 0.08 * R, R, lw)
        d = ImageDraw.Draw(img)
        for sx in (-1, 1):
            x = c + sx * 0.37 * 0.62 * R
            d.ellipse([x - 0.05 * R, c + 0.02 * R, x + 0.04 * R, c + 0.1 * R], fill=(90, 180, 255, 255))
    elif level == 5:  # labrador : doré, oreilles tombantes, collier rouge, balle
        floppy(img, c, c, R, lw, SUN, w=0.3, h=0.55, dx=0.8, top=-0.55)
        shape(img, ((255, 245, 200), (250, 215, 120), (205, 150, 50)), lw, lambda md: E(md, c, c + 0.02 * R, 0.86 * R, 0.84 * R))
        shape(img, RED, lw, lambda md: md.chord([c - 0.75 * R, c + 0.35 * R, c + 0.75 * R, c + 1.1 * R], 0, 180, fill=255))
        shape(img, GOLDC, max(2, lw - 1), lambda md: E(md, c, c + 0.98 * R, 0.13 * R, 0.13 * R))
        face(img, c, c - 0.05 * R, R, lw)
        shape(img, ((240, 255, 180), (190, 230, 60), (120, 160, 20)), lw, lambda md: E(md, c + 1.05 * R, c + 0.7 * R, 0.25 * R, 0.25 * R))
        ImageDraw.Draw(img).arc([c + 0.85 * R, c + 0.5 * R, c + 1.25 * R, c + 0.9 * R], 300, 60, fill=(255, 255, 255, 255), width=max(2, lw // 2))
    elif level == 6:  # saint-bernard : blanc et marron, tonneau au cou
        floppy(img, c, c, R, lw, BROWN, w=0.32, h=0.6, dx=0.8, top=-0.5)
        shape(img, WHITE, lw, lambda md: E(md, c, c + 0.02 * R, 0.88 * R, 0.88 * R))
        d = ImageDraw.Draw(img)
        for sx in (-1, 1):
            d.ellipse([c + sx * 0.25 * R - 0.32 * R, c - 0.45 * R, c + sx * 0.25 * R + 0.32 * R, c + 0.15 * R], fill=(170, 100, 45, 255))
        d.rectangle([c - 0.07 * R, c - 0.9 * R, c + 0.07 * R, c + 0.1 * R], fill=(255, 255, 255, 255))
        face(img, c, c - 0.05 * R, R, lw, "happy", tg=False)
        shape(img, WOOD, lw, lambda md: RR(md, c - 0.38 * R, c + 0.62 * R, c + 0.38 * R, c + 1.02 * R, 0.12 * R))
        d = ImageDraw.Draw(img)
        for x in (-0.2, 0.2):
            d.line([(c + x * R, c + 0.62 * R), (c + x * R, c + 1.02 * R)], fill=OUT, width=max(2, lw // 2))
    elif level == 7:  # chien cosmique : galaxie, casque d'astronaute, rayons, étoiles
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(18):
            a = k / 18 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.11), c + 0.5 * R * math.sin(a - 0.11)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.11), c + 0.5 * R * math.sin(a + 0.11))], fill=(255, 240, 120, 190) if k % 2 else (120, 230, 255, 190))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        pointy(img, c, c, R * 0.95, lw, GALAXY, inner=(255, 160, 220, 255))
        shape(img, GALAXY, lw, lambda md: E(md, c, c + 0.05 * R, 0.85 * R, 0.83 * R))
        d = ImageDraw.Draw(img)
        for (x, y, s) in ((-0.5, -0.4, 0.05), (0.55, -0.3, 0.04), (-0.6, 0.45, 0.04), (0.6, 0.5, 0.05), (0.1, -0.6, 0.03)):
            d.ellipse([c + (x - s) * R, c + (y - s) * R, c + (x + s) * R, c + (y + s) * R], fill=(255, 255, 255, 255))
        face(img, c, c + 0.05 * R, R, lw)
        hl = Image.new("RGBA", img.size, (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
        hd.ellipse([c - 1.0 * R, c - 1.0 * R, c + 1.0 * R, c + 1.05 * R], outline=(220, 245, 255, 230), width=int(0.07 * R))
        hd.arc([c - 0.8 * R, c - 0.85 * R, c + 0.2 * R, c + 0.2 * R], 200, 260, fill=(255, 255, 255, 200), width=int(0.06 * R))
        img.alpha_composite(hl)
        shape(img, GOLDC, lw, lambda md: md.polygon(
            [(c - 0.4 * R, c - 0.95 * R), (c - 0.45 * R, c - 1.35 * R), (c - 0.2 * R, c - 1.15 * R), (c, c - 1.45 * R),
             (c + 0.2 * R, c - 1.15 * R), (c + 0.45 * R, c - 1.35 * R), (c + 0.4 * R, c - 0.95 * R)], fill=255))
        for (sx, sy, ss) in ((-1.2, -0.9, 0.16), (1.2, -0.85, 0.14), (1.25, 0.6, 0.12), (-1.25, 0.55, 0.11)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
            star(img, c + sx * R, c + sy * R, ss * 0.55 * R, (255, 120, 200, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """LE VÉTÉRINAIRE ! : un vétérinaire inventé, miroir frontal et stéthoscope, seringue de dessin animé."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    shape(img, WHITE, lw, lambda md: md.polygon([(c - 0.6 * R, c + 0.4 * R), (c + 0.6 * R, c + 0.4 * R), (c + 0.95 * R, c + 1.3 * R), (c - 0.95 * R, c + 1.3 * R)], fill=255))
    shape(img, MINT, lw, lambda md: E(md, c, c - 0.05 * R, 0.8 * R, 0.8 * R))
    shape(img, MINT, lw, lambda md: md.pieslice([c - 0.82 * R, c - 0.95 * R, c + 0.82 * R, c + 0.25 * R], 180, 360, fill=255))
    d = ImageDraw.Draw(img)
    d.line([(c - 0.78 * R, c - 0.45 * R), (c + 0.78 * R, c - 0.45 * R)], fill=OUT, width=max(3, int(0.08 * R)))
    shape(img, WHITE, lw, lambda md: E(md, c, c - 0.55 * R, 0.25 * R, 0.25 * R))
    d = ImageDraw.Draw(img)
    d.ellipse([c - 0.1 * R, c - 0.65 * R, c + 0.1 * R, c - 0.45 * R], fill=(170, 220, 255, 255))
    draw_face(img, c, c + 0.0 * R, 0.6 * R, "open")
    d = ImageDraw.Draw(img)
    d.arc([c - 0.45 * R, c + 0.2 * R, c + 0.45 * R, c + 1.0 * R], 0, 180, fill=OUT, width=max(3, int(0.06 * R)))
    shape(img, GREY, max(2, lw - 1), lambda md: E(md, c, c + 1.0 * R, 0.12 * R, 0.12 * R))
    # seringue de dessin animé (géante, sans aiguille réaliste)
    shape(img, SKY, lw, lambda md: RR(md, c + 0.85 * R, c - 0.3 * R, c + 1.15 * R, c + 0.6 * R, 0.06 * R))
    shape(img, GREY, lw, lambda md: RR(md, c + 0.78 * R, c - 0.5 * R, c + 1.22 * R, c - 0.36 * R, 0.04 * R))
    d = ImageDraw.Draw(img)
    d.line([(c + 1.0 * R, c + 0.6 * R), (c + 1.0 * R, c + 0.8 * R)], fill=OUT, width=max(2, lw // 2))
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
    sheet = Image.new("RGBA", (W, H), (205, 190, 250, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
