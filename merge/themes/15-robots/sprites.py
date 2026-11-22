"""ROBOTS MERGE (épisode 15) : vis → méga-robot + UN BUG ! (rebondissement).
Tous les personnages sont inventés."""
import math
from PIL import Image, ImageDraw, ImageFilter
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("VIS",            "Vis",            24),
    ("BOULON",         "Boulon",         36),
    ("PUCE",           "Puce",           50),
    ("MINI-ROBOT",     "Mini-robot",     64),
    ("DRONE",          "Drone",          80),
    ("ROBOT MÉNAGER",  "Robot ménager",  98),
    ("MÉCA",           "Méca",          120),
    ("MÉGA-ROBOT",     "Méga-robot",    150),
]
BOMB_R = 48
OUT = (40, 35, 60, 255)

STEEL = ((245, 248, 255), (175, 185, 205), (100, 110, 135))
BRASS = ((255, 240, 170), (225, 175, 60), (150, 100, 20))
PCB = ((170, 240, 180), (50, 170, 90), (20, 100, 55))
TEAL = ((200, 250, 255), (70, 200, 225), (20, 120, 160))
INDIGO = ((210, 215, 255), (110, 125, 235), (55, 60, 170))
ROSE = ((255, 220, 240), (240, 120, 180), (180, 50, 120))
RED = ((255, 200, 190), (230, 80, 65), (160, 30, 30))
GOLDC = ((255, 250, 200), (255, 210, 60), (215, 140, 0))
SCREEN = ((90, 110, 140), (35, 45, 70), (15, 20, 35))
BUGG = ((210, 255, 160), (120, 215, 60), (50, 140, 20))


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


def hexa(cx, cy, r, rot=0.0):
    return [(cx + r * math.cos(rot + k * math.pi / 3), cy + r * math.sin(rot + k * math.pi / 3)) for k in range(6)]


def screen_face(img, cx, cy, w, h, R, lw, col=(120, 255, 230)):
    """écran avec yeux LED + sourire."""
    shape(img, SCREEN, max(2, lw - 1), lambda md: RR(md, cx - w, cy - h, cx + w, cy + h, 0.25 * h))
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        x = cx + sx * 0.45 * w
        d.ellipse([x - 0.2 * h, cy - 0.45 * h, x + 0.2 * h, cy + 0.05 * h], fill=col + (255,))
        d.ellipse([x - 0.08 * h, cy - 0.38 * h, x + 0.02 * h, cy - 0.25 * h], fill=(255, 255, 255, 255))
    d.arc([cx - 0.35 * w, cy - 0.15 * h, cx + 0.35 * w, cy + 0.55 * h], 20, 160, fill=col + (255,), width=max(2, int(0.12 * h)))
    bl = Image.new("RGBA", img.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(bl)
    for sx in (-1, 1):
        x = cx + sx * 0.78 * w
        bd.ellipse([x - 0.14 * h, cy + 0.15 * h, x + 0.14 * h, cy + 0.4 * h], fill=(255, 120, 160, 200))
    img.alpha_composite(bl)


def antenna(img, x, y0, y1, R, lw, ball=(255, 90, 90)):
    d = ImageDraw.Draw(img)
    d.line([(x, y0), (x, y1)], fill=OUT, width=max(3, int(0.06 * R)))
    shape(img, ((255, 230, 230), ball, tuple(max(0, v - 90) for v in ball)), max(2, lw // 2),
          lambda md: E(md, x, y1, 0.11 * R, 0.11 * R))


def bolts(img, pts, R):
    d = ImageDraw.Draw(img)
    for (x, y) in pts:
        d.ellipse([x - 0.05 * R, y - 0.05 * R, x + 0.05 * R, y + 0.05 * R], fill=(235, 240, 250, 255), outline=OUT, width=max(2, int(0.02 * R)))


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.65 if level >= 4 else 1.55
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    if level == 0:  # vis : tête ronde + filetage
        shape(img, STEEL, lw, lambda md: md.polygon([(c - 0.28 * R, c + 0.1 * R), (c + 0.28 * R, c + 0.1 * R), (c, c + 1.0 * R)], fill=255))
        d = ImageDraw.Draw(img)
        for k in range(4):
            y = c + 0.25 * R + k * 0.17 * R; w = 0.26 * R * (1 - k * 0.22)
            d.line([(c - w, y), (c + w, y + 0.06 * R)], fill=OUT, width=max(2, lw // 2))
        shape(img, STEEL, lw, lambda md: E(md, c, c - 0.2 * R, 0.9 * R, 0.6 * R))
        d.line([(c - 0.55 * R, c - 0.55 * R), (c + 0.55 * R, c - 0.55 * R)], fill=OUT, width=max(2, lw // 2))
        draw_face(img, c, c - 0.15 * R, 0.6 * R, "happy")
    elif level == 1:  # boulon : écrou hexagonal laiton
        shape(img, BRASS, lw, lambda md: md.polygon(hexa(c, c, 0.97 * R, math.pi / 6), fill=255))
        d = ImageDraw.Draw(img)
        d.ellipse([c - 0.72 * R, c - 0.72 * R, c + 0.72 * R, c + 0.72 * R], outline=(150, 100, 20, 255), width=max(2, lw // 2))
        draw_face(img, c, c, 0.62 * R, "happy")
    elif level == 2:  # puce électronique
        d = ImageDraw.Draw(img)
        for k in range(-2, 3):
            for (x0, y0, x1, y1) in ((c + k * 0.3 * R, c - 0.95 * R, c + k * 0.3 * R, c - 0.6 * R), (c + k * 0.3 * R, c + 0.6 * R, c + k * 0.3 * R, c + 0.95 * R),
                                     (c - 0.95 * R, c + k * 0.3 * R, c - 0.6 * R, c + k * 0.3 * R), (c + 0.6 * R, c + k * 0.3 * R, c + 0.95 * R, c + k * 0.3 * R)):
                d.line([(x0, y0), (x1, y1)], fill=(230, 200, 90, 255), width=int(0.11 * R))
                d.line([(x0, y0), (x1, y1)], fill=OUT, width=max(2, int(0.03 * R)))
        shape(img, PCB, lw, lambda md: RR(md, c - 0.72 * R, c - 0.72 * R, c + 0.72 * R, c + 0.72 * R, 0.14 * R))
        d = ImageDraw.Draw(img)
        d.ellipse([c - 0.58 * R, c - 0.58 * R, c - 0.44 * R, c - 0.44 * R], fill=(20, 100, 55, 255))
        draw_face(img, c, c + 0.02 * R, 0.6 * R, "open")
    elif level == 3:  # mini-robot
        antenna(img, c, c - 0.6 * R, c - 0.98 * R, R, lw)
        shape(img, TEAL, lw, lambda md: RR(md, c - 0.85 * R, c - 0.65 * R, c + 0.85 * R, c + 0.85 * R, 0.35 * R))
        for sx in (-1, 1):
            shape(img, STEEL, max(2, lw - 1), lambda md: E(md, c + sx * 0.88 * R, c + 0.1 * R, 0.14 * R, 0.2 * R))
        screen_face(img, c, c + 0.05 * R, 0.6 * R, 0.42 * R, R, lw)
    elif level == 4:  # drone : 4 hélices
        d = ImageDraw.Draw(img)
        for sx in (-1, 1):
            for sy in (-1, 1):
                d.line([(c, c), (c + sx * 0.78 * R, c + sy * 0.55 * R)], fill=OUT, width=int(0.16 * R))
                d.line([(c, c), (c + sx * 0.78 * R, c + sy * 0.55 * R)], fill=(150, 160, 190, 255), width=int(0.09 * R))
        for sx in (-1, 1):
            for sy in (-1, 1):
                x, y = c + sx * 0.78 * R, c + sy * 0.55 * R
                shape(img, ((235, 245, 255), (180, 210, 240), (110, 140, 190)), max(2, lw // 2), lambda md: E(md, x, y, 0.36 * R, 0.12 * R))
                shape(img, INDIGO, max(2, lw // 2), lambda md: E(md, x, y, 0.09 * R, 0.09 * R))
        shape(img, INDIGO, lw, lambda md: E(md, c, c + 0.05 * R, 0.58 * R, 0.45 * R))
        draw_face(img, c, c + 0.05 * R, 0.5 * R, "happy")
    elif level == 5:  # robot ménager (avec plumeau)
        d = ImageDraw.Draw(img)
        d.line([(c + 0.75 * R, c + 0.1 * R), (c + 0.9 * R, c - 0.75 * R)], fill=(150, 90, 40, 255), width=int(0.08 * R))
        shape(img, ((255, 240, 200), (250, 200, 90), (210, 140, 40)), max(2, lw // 2),
              lambda md: [E(md, c + 0.9 * R + 0.16 * R * math.cos(a), c - 0.85 * R + 0.14 * R * math.sin(a), 0.13 * R, 0.13 * R) for a in [k / 7 * 6.283 for k in range(7)]])
        shape(img, ROSE, lw, lambda md: (E(md, c, c + 0.15 * R, 0.85 * R, 0.78 * R)))
        shape(img, ((255, 255, 255), (240, 240, 250), (190, 190, 215)), max(2, lw - 1),
              lambda md: md.polygon([(c - 0.45 * R, c + 0.3 * R), (c + 0.45 * R, c + 0.3 * R), (c + 0.55 * R, c + 0.85 * R), (c - 0.55 * R, c + 0.85 * R)], fill=255))
        shape(img, ROSE, lw, lambda md: E(md, c, c - 0.6 * R, 0.55 * R, 0.25 * R))
        antenna(img, c, c - 0.8 * R, c - 1.05 * R, R, lw, ball=(255, 200, 60))
        screen_face(img, c, c - 0.12 * R, 0.55 * R, 0.33 * R, R, lw, col=(255, 230, 120))
    elif level == 6:  # méca : gros robot carré à épaulettes
        for sx in (-1, 1):
            shape(img, RED, lw, lambda md: RR(md, c + sx * 0.62 * R - 0.32 * R, c - 0.45 * R, c + sx * 0.62 * R + 0.32 * R, c + 0.1 * R, 0.14 * R))
        shape(img, STEEL, lw, lambda md: RR(md, c - 0.62 * R, c - 0.55 * R, c + 0.62 * R, c + 0.9 * R, 0.18 * R))
        shape(img, RED, lw, lambda md: RR(md, c - 0.5 * R, c - 0.95 * R, c + 0.5 * R, c - 0.35 * R, 0.16 * R))
        d = ImageDraw.Draw(img)
        d.polygon([(c - 0.15 * R, c - 0.95 * R), (c, c - 1.15 * R), (c + 0.15 * R, c - 0.95 * R)], fill=(255, 210, 60, 255), outline=OUT)
        screen_face(img, c, c - 0.66 * R, 0.4 * R, 0.2 * R, R, lw, col=(120, 255, 200))
        shape(img, ((255, 250, 210), (255, 210, 60), (210, 140, 0)), max(2, lw - 1), lambda md: E(md, c, c + 0.2 * R, 0.24 * R, 0.24 * R))
        bolts(img, [(c - 0.5 * R, c - 0.42 * R), (c + 0.5 * R, c - 0.42 * R), (c - 0.5 * R, c + 0.78 * R), (c + 0.5 * R, c + 0.78 * R)], R)
    elif level == 7:  # méga-robot doré
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(16):
            a = k / 16 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.12), c + 0.5 * R * math.sin(a - 0.12)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.12), c + 0.5 * R * math.sin(a + 0.12))], fill=(255, 245, 150, 190) if k % 2 else (150, 230, 255, 190))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        for sx in (-1, 1):
            shape(img, GOLDC, lw, lambda md: E(md, c + sx * 0.82 * R, c - 0.05 * R, 0.22 * R, 0.3 * R))
        shape(img, GOLDC, lw, lambda md: RR(md, c - 0.8 * R, c - 0.55 * R, c + 0.8 * R, c + 0.92 * R, 0.35 * R))
        for sx in (-1, 1):
            antenna(img, c + sx * 0.4 * R, c - 0.55 * R, c - 0.85 * R, R, lw, ball=(90, 200, 255))
        shape(img, GOLDC, lw, lambda md: md.polygon(
            [(c - 0.3 * R, c - 0.5 * R), (c - 0.34 * R, c - 0.88 * R), (c - 0.14 * R, c - 0.7 * R), (c, c - 0.98 * R),
             (c + 0.14 * R, c - 0.7 * R), (c + 0.34 * R, c - 0.88 * R), (c + 0.3 * R, c - 0.5 * R)], fill=255))
        screen_face(img, c, c + 0.1 * R, 0.6 * R, 0.4 * R, R, lw, col=(130, 240, 255))
        bolts(img, [(c - 0.65 * R, c - 0.4 * R), (c + 0.65 * R, c - 0.4 * R), (c - 0.65 * R, c + 0.78 * R), (c + 0.65 * R, c + 0.78 * R)], R)
        for (sx, sy, ss) in ((-1.15, -0.9, 0.16), (1.15, -0.85, 0.14), (1.2, 0.6, 0.12), (-1.2, 0.55, 0.11)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
            star(img, c + sx * R, c + sy * R, ss * 0.55 * R, (255, 200, 60, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """UN BUG ! : petit insecte vert à pixels, l'air coquin."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        for k, dy in enumerate((-0.25, 0.2, 0.6)):
            d.line([(c + sx * 0.5 * R, c + dy * R), (c + sx * 1.05 * R, c + (dy + 0.15 * (k - 1)) * R)], fill=OUT, width=int(0.08 * R))
        d.line([(c + sx * 0.2 * R, c - 0.7 * R), (c + sx * 0.55 * R, c - 1.25 * R)], fill=OUT, width=int(0.06 * R))
        d.ellipse([c + sx * 0.55 * R - 0.09 * R, c - 1.34 * R, c + sx * 0.55 * R + 0.09 * R, c - 1.16 * R], fill=(255, 80, 120, 255), outline=OUT, width=max(2, lw // 2))
    shape(img, BUGG, lw, lambda md: E(md, c, c + 0.2 * R, 0.72 * R, 0.85 * R))
    d = ImageDraw.Draw(img)
    d.line([(c, c - 0.25 * R), (c, c + 1.02 * R)], fill=OUT, width=max(2, lw // 2))
    for (x, y, col) in ((-0.4, 0.2, (255, 60, 200)), (0.35, 0.45, (60, 220, 255)), (-0.25, 0.65, (255, 220, 40)), (0.45, 0.05, (255, 60, 60))):
        s = 0.13 * R
        d.rectangle([c + x * R - s, c + y * R - s, c + x * R + s, c + y * R + s], fill=col + (255,), outline=OUT, width=max(2, lw // 3))
    shape(img, ((150, 230, 120), (60, 160, 50), (25, 90, 20)), lw, lambda md: E(md, c, c - 0.5 * R, 0.5 * R, 0.38 * R))
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        x = c + sx * 0.2 * R; cy = c - 0.55 * R
        d.ellipse([x - 0.13 * R, cy - 0.14 * R, x + 0.13 * R, cy + 0.12 * R], fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=max(2, lw // 2))
        d.ellipse([x - 0.05 * R + sx * 0.03 * R, cy - 0.06 * R, x + 0.07 * R + sx * 0.03 * R, cy + 0.07 * R], fill=(10, 10, 10, 255))
    d.arc([c - 0.2 * R, c - 0.5 * R, c + 0.2 * R, c - 0.25 * R], 20, 160, fill=(20, 20, 20, 255), width=int(0.05 * R))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(150, 80, 20, 255), glow=(255, 255, 255)):
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
    sheet = Image.new("RGBA", (W, H), (255, 205, 140, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
