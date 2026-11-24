"""FAMILLE MERGE (épisode 17) : bébé → papy légendaire + PLUS DE WIFI ! (rebondissement).
Tous les personnages sont inventés."""
import math
from PIL import Image, ImageDraw, ImageFilter
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("BÉBÉ",             "Bébé",             24),
    ("ENFANT",           "Enfant",           36),
    ("ADO",              "Ado",              50),
    ("ÉTUDIANT",         "Étudiant",         64),
    ("PARENT",           "Parent",           80),
    ("PAPY",             "Papy",             98),
    ("ARRIÈRE-PAPY",     "Arrière-papy",    120),
    ("PAPY LÉGENDAIRE",  "Papy légendaire", 150),
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


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.65 if level >= 4 else 1.55
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    if level == 0:  # bébé : rose, mèche bouclée, tétine
        shape(img, PINK, lw, lambda md: E(md, c, c + 0.05 * R, 0.92 * R, 0.9 * R))
        d = ImageDraw.Draw(img)
        d.arc([c - 0.12 * R, c - 1.12 * R, c + 0.22 * R, c - 0.72 * R], 100, 400, fill=OUT, width=max(2, lw))
        draw_face(img, c, c - 0.05 * R, 0.66 * R, "happy")
        shape(img, SKY, max(2, lw - 1), lambda md: E(md, c, c + 0.42 * R, 0.24 * R, 0.14 * R))
        shape(img, WHITE, max(2, lw - 1), lambda md: E(md, c, c + 0.42 * R, 0.08 * R, 0.08 * R))
    elif level == 1:  # enfant : jaune, casquette rouge, sucette
        shape(img, SUN, lw, lambda md: E(md, c, c + 0.08 * R, 0.88 * R, 0.86 * R))
        shape(img, RED, lw, lambda md: md.pieslice([c - 0.8 * R, c - 1.05 * R, c + 0.8 * R, c + 0.35 * R], 180, 360, fill=255))
        shape(img, RED, max(2, lw - 1), lambda md: RR(md, c + 0.3 * R, c - 0.42 * R, c + 1.15 * R, c - 0.28 * R, 0.07 * R))
        d = ImageDraw.Draw(img)
        d.line([(c - 0.75 * R, c + 0.85 * R), (c - 0.75 * R, c + 0.2 * R)], fill=(255, 255, 255, 255), width=max(3, lw))
        shape(img, GRAPE, max(2, lw - 1), lambda md: E(md, c - 0.75 * R, c + 0.1 * R, 0.26 * R, 0.26 * R))
        d = ImageDraw.Draw(img)
        d.arc([c - 0.92 * R, c - 0.07 * R, c - 0.58 * R, c + 0.27 * R], 0, 300, fill=(255, 255, 255, 255), width=max(2, lw // 2))
        draw_face(img, c, c + 0.05 * R, 0.62 * R, "open")
    elif level == 2:  # ado : violet, frange, casque audio
        shape(img, GRAPE, lw, lambda md: E(md, c, c + 0.08 * R, 0.86 * R, 0.88 * R))
        shape(img, DARK, lw, lambda md: md.polygon([(c - 0.82 * R, c - 0.1 * R), (c - 0.7 * R, c - 0.7 * R), (c, c - 0.86 * R),
                                                    (c + 0.75 * R, c - 0.62 * R), (c + 0.82 * R, c - 0.15 * R), (c + 0.1 * R, c - 0.4 * R)], fill=255))
        d = ImageDraw.Draw(img)
        d.arc([c - 1.0 * R, c - 1.05 * R, c + 1.0 * R, c + 0.6 * R], 190, 350, fill=OUT, width=max(4, int(0.12 * R)))
        for sx in (-1, 1):
            shape(img, RED, lw, lambda md: RR(md, c + sx * 0.95 * R - 0.2 * R, c - 0.25 * R, c + sx * 0.95 * R + 0.2 * R, c + 0.35 * R, 0.12 * R))
        draw_face(img, c, c + 0.1 * R, 0.6 * R, "sweat")
    elif level == 3:  # étudiant : bleu, lunettes rondes, toque de diplômé
        shape(img, SKY, lw, lambda md: E(md, c, c + 0.12 * R, 0.86 * R, 0.86 * R))
        shape(img, DARK, lw, lambda md: RR(md, c - 0.45 * R, c - 0.82 * R, c + 0.45 * R, c - 0.5 * R, 0.08 * R))
        shape(img, DARK, lw, lambda md: md.polygon([(c - 1.05 * R, c - 0.88 * R), (c, c - 1.18 * R), (c + 1.05 * R, c - 0.88 * R), (c, c - 0.6 * R)], fill=255))
        d = ImageDraw.Draw(img)
        d.line([(c, c - 0.88 * R), (c + 0.75 * R, c - 0.8 * R), (c + 0.75 * R, c - 0.4 * R)], fill=(255, 205, 55, 255), width=max(2, lw // 2))
        d.ellipse([c + 0.66 * R, c - 0.45 * R, c + 0.84 * R, c - 0.28 * R], fill=(255, 205, 55, 255))
        draw_face(img, c, c + 0.12 * R, 0.62 * R, "happy")
        glasses(img, c, c + 0.1 * R, 0.62 * R, lw)
    elif level == 4:  # parent : vert, chignon, cernes, tasse de café
        shape(img, BROWN, lw, lambda md: E(md, c, c - 0.9 * R, 0.32 * R, 0.26 * R))
        shape(img, MINT, lw, lambda md: E(md, c, c + 0.08 * R, 0.86 * R, 0.88 * R))
        shape(img, BROWN, lw, lambda md: md.pieslice([c - 0.86 * R, c - 0.82 * R, c + 0.86 * R, c + 0.2 * R], 180, 360, fill=255))
        draw_face(img, c, c + 0.05 * R, 0.62 * R, "sweat")
        d = ImageDraw.Draw(img)
        for sx in (-1, 1):
            d.arc([c + sx * 0.23 * R - 0.15 * R, c + 0.03 * R, c + sx * 0.23 * R + 0.15 * R, c + 0.17 * R], 20, 160, fill=(110, 90, 160, 255), width=max(2, lw // 3))
        shape(img, WHITE, lw, lambda md: RR(md, c + 0.55 * R, c + 0.2 * R, c + 1.0 * R, c + 0.8 * R, 0.08 * R))
        d = ImageDraw.Draw(img)
        d.arc([c + 0.88 * R, c + 0.3 * R, c + 1.18 * R, c + 0.6 * R], 270, 90, fill=OUT, width=max(2, lw // 2))
        d.rectangle([c + 0.6 * R, c + 0.26 * R, c + 0.95 * R, c + 0.36 * R], fill=(140, 85, 40, 255))
        for k in range(2):
            d.arc([c + 0.62 * R + k * 0.15 * R, c - 0.25 * R, c + 0.8 * R + k * 0.15 * R, c + 0.15 * R], 100, 260, fill=(255, 255, 255, 255), width=max(2, lw // 2))
    elif level == 5:  # papy : pêche, crâne dégarni, touffes blanches, lunettes, moustache
        shape(img, PEACH, lw, lambda md: E(md, c, c + 0.05 * R, 0.86 * R, 0.9 * R))
        for sx in (-1, 1):
            shape(img, WHITE, max(2, lw - 1), lambda md: E(md, c + sx * 0.82 * R, c - 0.25 * R, 0.22 * R, 0.3 * R))
        draw_face(img, c, c - 0.05 * R, 0.6 * R, "happy")
        glasses(img, c, c - 0.07 * R, 0.6 * R, lw)
        mustache(img, c, c + 0.17 * R, 0.6 * R, lw)
        shape(img, RED, lw, lambda md: md.pieslice([c - 0.7 * R, c + 0.55 * R, c + 0.7 * R, c + 1.35 * R], 200, 340, fill=255))
    elif level == 6:  # arrière-papy : crème, longue barbe blanche, canne, béret
        d = ImageDraw.Draw(img)
        d.line([(c + 1.0 * R, c - 0.2 * R), (c + 1.0 * R, c + 1.05 * R)], fill=(110, 65, 25, 255), width=int(0.12 * R))
        d.arc([c + 0.75 * R, c - 0.42 * R, c + 1.06 * R, c - 0.1 * R], 180, 360, fill=(110, 65, 25, 255), width=int(0.12 * R))
        shape(img, CREAM, lw, lambda md: E(md, c, c + 0.05 * R, 0.86 * R, 0.9 * R))
        shape(img, RED, lw, lambda md: E(md, c - 0.05 * R, c - 0.68 * R, 0.72 * R, 0.26 * R))
        d = ImageDraw.Draw(img)
        d.line([(c - 0.05 * R, c - 0.93 * R), (c - 0.05 * R, c - 1.05 * R)], fill=OUT, width=max(2, lw // 2))
        beard(img, c, R, lw, c + 0.15 * R, 0.95 * R)
        draw_face(img, c, c - 0.12 * R, 0.58 * R, "happy")
        mustache(img, c, c + 0.12 * R, 0.62 * R, lw)
    elif level == 7:  # papy légendaire : doré, couronne, barbe immense, rayons, étoiles
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(16):
            a = k / 16 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.12), c + 0.5 * R * math.sin(a - 0.12)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.12), c + 0.5 * R * math.sin(a + 0.12))], fill=(255, 245, 150, 190) if k % 2 else (150, 220, 255, 190))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        shape(img, GRAPE, lw, lambda md: md.polygon([(c - 0.55 * R, c - 0.2 * R), (c + 0.55 * R, c - 0.2 * R), (c + 1.05 * R, c + 0.95 * R), (c - 1.05 * R, c + 0.95 * R)], fill=255))
        shape(img, GOLDC, lw, lambda md: E(md, c, c + 0.0 * R, 0.78 * R, 0.82 * R))
        beard(img, c, R, lw, c + 0.12 * R, 1.0 * R)
        shape(img, GOLDC, lw, lambda md: md.polygon(
            [(c - 0.45 * R, c - 0.6 * R), (c - 0.5 * R, c - 1.05 * R), (c - 0.22 * R, c - 0.83 * R), (c, c - 1.17 * R),
             (c + 0.22 * R, c - 0.83 * R), (c + 0.5 * R, c - 1.05 * R), (c + 0.45 * R, c - 0.6 * R)], fill=255))
        d = ImageDraw.Draw(img)
        for (x, col) in ((-0.25, (255, 70, 120)), (0, (70, 200, 255)), (0.25, (120, 230, 90))):
            d.ellipse([c + x * R - 0.06 * R, c - 0.77 * R, c + x * R + 0.06 * R, c - 0.65 * R], fill=col + (255,), outline=OUT, width=max(2, lw // 3))
        draw_face(img, c, c - 0.2 * R, 0.58 * R, "happy")
        glasses(img, c, c - 0.22 * R, 0.58 * R, lw, col=(200, 120, 0, 255))
        mustache(img, c, c + 0.05 * R, 0.62 * R, lw)
        for (sx, sy, ss) in ((-1.15, -0.9, 0.16), (1.15, -0.85, 0.14), (1.2, 0.6, 0.12), (-1.2, 0.55, 0.11)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
            star(img, c + sx * R, c + sy * R, ss * 0.55 * R, (80, 180, 255, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """PLUS DE WIFI ! : un symbole wifi barré d'une croix rouge, l'air paniqué."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    shape(img, WHITE, lw, lambda md: E(md, c, c, 0.95 * R, 0.95 * R))
    d = ImageDraw.Draw(img)
    for k, rr in enumerate((0.78, 0.56, 0.34)):
        d.arc([c - rr * R, c - 0.15 * R - rr * R, c + rr * R, c - 0.15 * R + rr * R], 225, 315,
              fill=(60, 130, 230, 255), width=int(0.12 * R))
    draw_face(img, c, c + 0.2 * R, 0.55 * R, "open")
    for sx in (-1, 1):  # sourcils inquiets
        d.line([(c + sx * 0.1 * R, c + 0.02 * R), (c + sx * 0.33 * R, c + 0.08 * R)], fill=(28, 18, 20, 255), width=max(2, int(0.05 * R)))
    d = ImageDraw.Draw(img)
    w = int(0.16 * R)
    for (a, b) in (((c + 0.45 * R, c - 1.15 * R), (c + 1.15 * R, c - 0.45 * R)), ((c + 1.15 * R, c - 1.15 * R), (c + 0.45 * R, c - 0.45 * R))):
        d.line([a, b], fill=OUT, width=w + 2 * lw)
    for (a, b) in (((c + 0.45 * R, c - 1.15 * R), (c + 1.15 * R, c - 0.45 * R)), ((c + 1.15 * R, c - 1.15 * R), (c + 0.45 * R, c - 0.45 * R))):
        d.line([a, b], fill=(235, 50, 50, 255), width=w)
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
    sheet = Image.new("RGBA", (W, H), (140, 215, 250, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
