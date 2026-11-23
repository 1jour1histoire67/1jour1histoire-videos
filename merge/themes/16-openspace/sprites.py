"""OPEN SPACE MERGE (épisode 16) : trombone → PDG galactique + RÉUNION SURPRISE ! (rebondissement).
Tous les personnages sont inventés."""
import math
from PIL import Image, ImageDraw, ImageFilter
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("TROMBONE",        "Trombone",        24),
    ("PENSE-BÊTE",      "Pense-bête",      36),
    ("STAGIAIRE",       "Stagiaire",       50),
    ("EMPLOYÉ",         "Employé",         64),
    ("MANAGER",         "Manager",         80),
    ("DIRECTEUR",       "Directeur",       98),
    ("PDG",             "PDG",            120),
    ("PDG GALACTIQUE",  "PDG galactique", 150),
]
BOMB_R = 48
OUT = (55, 30, 60, 255)

STEEL = ((250, 252, 255), (190, 200, 215), (115, 125, 150))
NOTE = ((255, 255, 190), (255, 235, 90), (225, 180, 20))
MINT = ((215, 255, 225), (120, 220, 150), (50, 150, 90))
SKY = ((215, 235, 255), (110, 170, 245), (45, 95, 190))
VIOLET = ((235, 215, 255), (165, 120, 235), (95, 55, 170))
TEAL = ((205, 250, 245), (60, 190, 180), (20, 115, 115))
RED = ((255, 205, 195), (235, 85, 70), (160, 35, 35))
GOLDC = ((255, 250, 200), (255, 205, 55), (210, 130, 0))
WHITE = ((255, 255, 255), (240, 242, 250), (190, 195, 215))
NAVY = ((150, 165, 220), (60, 75, 140), (25, 30, 75))
WOOD = ((235, 190, 140), (190, 125, 70), (120, 70, 30))


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


def tie(img, cx, top, R, lw, cols):
    shape(img, cols, max(2, lw - 1), lambda md: md.polygon(
        [(cx - 0.09 * R, top), (cx + 0.09 * R, top), (cx + 0.05 * R, top + 0.12 * R), (cx + 0.14 * R, top + 0.5 * R),
         (cx, top + 0.64 * R), (cx - 0.14 * R, top + 0.5 * R), (cx - 0.05 * R, top + 0.12 * R)], fill=255))


def collar(img, cx, top, R, lw):
    for sx in (-1, 1):
        shape(img, WHITE, max(2, lw - 1), lambda md: md.polygon(
            [(cx, top + 0.05 * R), (cx + sx * 0.32 * R, top - 0.05 * R), (cx + sx * 0.26 * R, top + 0.2 * R)], fill=255))


def glasses(img, cx, cy, s, lw, col=(40, 30, 50, 255), dark=False):
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        x = cx + sx * 0.37 * s
        box = [x - 0.24 * s, cy - 0.2 * s, x + 0.24 * s, cy + 0.14 * s]
        if dark:
            d.rounded_rectangle(box, int(0.08 * s), fill=(25, 25, 40, 255), outline=col, width=max(2, lw // 2))
            d.line([(x - 0.12 * s, cy - 0.1 * s), (x - 0.02 * s, cy - 0.14 * s)], fill=(255, 255, 255, 230), width=max(2, int(0.05 * s)))
        else:
            d.ellipse(box, outline=col, width=max(2, lw // 2))
    d.line([(cx - 0.13 * s, cy - 0.06 * s), (cx + 0.13 * s, cy - 0.06 * s)], fill=col, width=max(2, lw // 2))


def worker(img, c, R, lw, body, face_mood="happy"):
    """corps-goutte d'un personnage de bureau : retourne (x tête, y visage)."""
    shape(img, body, lw, lambda md: E(md, c, c + 0.08 * R, 0.86 * R, 0.9 * R))
    return c, c - 0.12 * R


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.65 if level >= 4 else 1.55
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    if level == 0:  # trombone : capsule argentée avec boucles
        shape(img, STEEL, lw, lambda md: RR(md, c - 0.62 * R, c - 0.98 * R, c + 0.62 * R, c + 0.98 * R, 0.6 * R))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([c - 0.42 * R, c - 0.78 * R, c + 0.42 * R, c + 0.78 * R], int(0.4 * R), outline=(115, 125, 150, 255), width=max(2, lw // 2))
        draw_face(img, c, c, 0.62 * R, "happy")
    elif level == 1:  # pense-bête : carré jaune coin plié
        shape(img, NOTE, lw, lambda md: md.polygon([(c - 0.85 * R, c - 0.85 * R), (c + 0.85 * R, c - 0.85 * R), (c + 0.85 * R, c + 0.4 * R),
                                                    (c + 0.4 * R, c + 0.85 * R), (c - 0.85 * R, c + 0.85 * R)], fill=255))
        shape(img, ((255, 245, 170), (240, 200, 50), (200, 150, 10)), max(2, lw - 1),
              lambda md: md.polygon([(c + 0.85 * R, c + 0.4 * R), (c + 0.4 * R, c + 0.85 * R), (c + 0.42 * R, c + 0.42 * R)], fill=255))
        d = ImageDraw.Draw(img)
        d.rectangle([c - 0.3 * R, c - 0.98 * R, c + 0.3 * R, c - 0.75 * R], fill=(255, 255, 255, 170))
        draw_face(img, c, c - 0.05 * R, 0.66 * R, "happy")
    elif level == 2:  # stagiaire : petit vert + gobelet de café + badge
        x, y = worker(img, c, R, lw, MINT)
        shape(img, WHITE, max(2, lw - 1), lambda md: md.polygon([(c + 0.6 * R, c + 0.05 * R), (c + 1.05 * R, c + 0.05 * R), (c + 0.98 * R, c + 0.65 * R), (c + 0.67 * R, c + 0.65 * R)], fill=255))
        d = ImageDraw.Draw(img)
        d.rectangle([c + 0.64 * R, c + 0.22 * R, c + 1.01 * R, c + 0.38 * R], fill=(170, 100, 50, 255))
        for k in range(2):
            d.arc([c + 0.68 * R + k * 0.15 * R, c - 0.45 * R, c + 0.85 * R + k * 0.15 * R, c - 0.05 * R], 100, 260, fill=(255, 255, 255, 255), width=max(2, lw // 2))
        d.line([(c - 0.3 * R, c + 0.2 * R), (c - 0.18 * R, c + 0.5 * R), (c - 0.06 * R, c + 0.2 * R)], fill=(230, 60, 90, 255), width=max(2, lw // 2))
        shape(img, WHITE, max(2, lw // 2), lambda md: RR(md, c - 0.33 * R, c + 0.48 * R, c - 0.03 * R, c + 0.75 * R, 0.05 * R))
        draw_face(img, x, y, 0.62 * R, "sweat")
    elif level == 3:  # employé : bleu, col + cravate rouge
        x, y = worker(img, c, R, lw, SKY)
        collar(img, c, c + 0.32 * R, R, lw)
        tie(img, c, c + 0.36 * R, R, lw, RED)
        draw_face(img, x, y, 0.62 * R, "happy")
    elif level == 4:  # manager : violet, lunettes, cravate, porte-bloc
        x, y = worker(img, c, R, lw, VIOLET)
        collar(img, c, c + 0.32 * R, R, lw)
        tie(img, c, c + 0.36 * R, R, lw, GOLDC)
        shape(img, WOOD, max(2, lw - 1), lambda md: RR(md, c + 0.62 * R, c + 0.05 * R, c + 1.08 * R, c + 0.7 * R, 0.05 * R))
        shape(img, WHITE, max(2, lw // 2), lambda md: md.rectangle([c + 0.7 * R, c + 0.17 * R, c + 1.0 * R, c + 0.62 * R], fill=255))
        d = ImageDraw.Draw(img)
        for k in range(3):
            d.line([(c + 0.75 * R, c + 0.28 * R + k * 0.11 * R), (c + 0.95 * R, c + 0.28 * R + k * 0.11 * R)], fill=(120, 130, 160, 255), width=max(2, lw // 3))
        d.line([(c + 0.76 * R, c + 0.6 * R), (c + 0.84 * R, c + 0.68 * R), (c + 0.98 * R, c + 0.48 * R)], fill=(40, 170, 80, 255), width=max(2, lw // 2))
        draw_face(img, x, y, 0.62 * R, "happy")
        glasses(img, x, y - 0.02 * R, 0.62 * R, lw)
    elif level == 5:  # directeur : costume bleu marine, nœud papillon, moustache
        shape(img, TEAL, lw, lambda md: E(md, c, c - 0.1 * R, 0.72 * R, 0.72 * R))
        shape(img, NAVY, lw, lambda md: md.pieslice([c - 0.9 * R, c + 0.2 * R, c + 0.9 * R, c + 1.6 * R], 180, 360, fill=255))
        shape(img, WHITE, max(2, lw - 1), lambda md: md.polygon([(c - 0.25 * R, c + 0.42 * R), (c + 0.25 * R, c + 0.42 * R), (c, c + 0.9 * R)], fill=255))
        for sx in (-1, 1):
            shape(img, RED, max(2, lw - 1), lambda md: md.polygon([(c, c + 0.52 * R), (c + sx * 0.28 * R, c + 0.4 * R), (c + sx * 0.28 * R, c + 0.66 * R)], fill=255))
        shape(img, RED, max(2, lw - 1), lambda md: E(md, c, c + 0.53 * R, 0.07 * R, 0.07 * R))
        draw_face(img, c, c - 0.15 * R, 0.6 * R, "happy")
    elif level == 6:  # PDG : rouge, lunettes noires, cravate dorée, mallette
        shape(img, WOOD, lw, lambda md: RR(md, c + 0.45 * R, c + 0.35 * R, c + 1.12 * R, c + 0.9 * R, 0.08 * R))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([c + 0.65 * R, c + 0.22 * R, c + 0.92 * R, c + 0.4 * R], int(0.05 * R), outline=OUT, width=max(2, lw // 2))
        x, y = worker(img, c, R, lw, RED)
        shape(img, NAVY, lw, lambda md: md.pieslice([c - 0.86 * R, c + 0.32 * R, c + 0.86 * R, c + 2.0 * R], 200, 340, fill=255))
        collar(img, c, c + 0.38 * R, R, lw)
        tie(img, c, c + 0.42 * R, R, lw, GOLDC)
        draw_face(img, x, y, 0.62 * R, "happy")
        glasses(img, x, y - 0.02 * R, 0.62 * R, lw, dark=True)
    elif level == 7:  # PDG galactique : doré, couronne, cape, rayons
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(16):
            a = k / 16 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.12), c + 0.5 * R * math.sin(a - 0.12)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.12), c + 0.5 * R * math.sin(a + 0.12))], fill=(255, 245, 150, 190) if k % 2 else (255, 170, 220, 190))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        shape(img, VIOLET, lw, lambda md: md.polygon([(c - 0.55 * R, c - 0.2 * R), (c + 0.55 * R, c - 0.2 * R), (c + 1.05 * R, c + 0.95 * R), (c - 1.05 * R, c + 0.95 * R)], fill=255))
        shape(img, GOLDC, lw, lambda md: E(md, c, c + 0.1 * R, 0.78 * R, 0.82 * R))
        shape(img, NAVY, lw, lambda md: md.pieslice([c - 0.78 * R, c + 0.38 * R, c + 0.78 * R, c + 1.95 * R], 205, 335, fill=255))
        tie(img, c, c + 0.45 * R, R, lw, RED)
        shape(img, GOLDC, lw, lambda md: md.polygon(
            [(c - 0.45 * R, c - 0.55 * R), (c - 0.5 * R, c - 1.0 * R), (c - 0.22 * R, c - 0.78 * R), (c, c - 1.12 * R),
             (c + 0.22 * R, c - 0.78 * R), (c + 0.5 * R, c - 1.0 * R), (c + 0.45 * R, c - 0.55 * R)], fill=255))
        d = ImageDraw.Draw(img)
        for (x, col) in ((-0.25, (255, 70, 120)), (0, (70, 200, 255)), (0.25, (120, 230, 90))):
            d.ellipse([c + x * R - 0.06 * R, c - 0.72 * R, c + x * R + 0.06 * R, c - 0.6 * R], fill=col + (255,), outline=OUT, width=max(2, lw // 3))
        draw_face(img, c, c - 0.12 * R, 0.6 * R, "open")
        glasses(img, c, c - 0.14 * R, 0.6 * R, lw, col=(255, 210, 60, 255), dark=True)
        for (sx, sy, ss) in ((-1.15, -0.9, 0.16), (1.15, -0.85, 0.14), (1.2, 0.6, 0.12), (-1.2, 0.55, 0.11)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
            star(img, c + sx * R, c + sy * R, ss * 0.55 * R, (255, 120, 190, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """RÉUNION SURPRISE ! : un calendrier à anneaux qui sonne, l'air coquin."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):  # traits de sonnerie
        for k in range(3):
            a = -0.5 + k * 0.5
            d.line([(c + sx * (1.05 * R) , c - 0.2 * R + a * 0.6 * R), (c + sx * 1.35 * R, c - 0.3 * R + a * 0.9 * R)], fill=OUT, width=int(0.07 * R))
    shape(img, WHITE, lw, lambda md: RR(md, c - 0.9 * R, c - 0.8 * R, c + 0.9 * R, c + 0.95 * R, 0.16 * R))
    shape(img, RED, lw, lambda md: RR(md, c - 0.9 * R, c - 0.8 * R, c + 0.9 * R, c - 0.35 * R, 0.16 * R))
    for sx in (-1, 1):
        shape(img, STEEL, max(2, lw - 1), lambda md: RR(md, c + sx * 0.45 * R - 0.08 * R, c - 1.05 * R, c + sx * 0.45 * R + 0.08 * R, c - 0.6 * R, 0.08 * R))
    d = ImageDraw.Draw(img)
    for i in range(4):
        for j in range(2):
            x = c - 0.6 * R + i * 0.4 * R; y = c + 0.62 * R + j * 0.18 * R
            d.rectangle([x - 0.06 * R, y - 0.05 * R, x + 0.06 * R, y + 0.05 * R], fill=(200, 205, 225, 255))
    d.ellipse([c + 0.14 * R, c + 0.52 * R, c + 0.46 * R, c + 0.98 * R], outline=(230, 40, 60, 255), width=max(2, int(0.05 * R)))
    draw_face(img, c, c + 0.08 * R, 0.62 * R, "open")
    for sx in (-1, 1):  # sourcils coquins
        d.line([(c + sx * 0.12 * R, c - 0.12 * R), (c + sx * 0.38 * R, c - 0.2 * R)], fill=(28, 18, 20, 255), width=max(2, int(0.05 * R)))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(160, 40, 100, 255), glow=(255, 255, 255)):
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
    sheet = Image.new("RGBA", (W, H), (255, 185, 215, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
