"""MÉTÉO MERGE (épisode 13) : goutte → soleil suprême + LA GRÊLE ! (rebondissement).
Tous les personnages sont inventés."""
import math
from PIL import Image, ImageDraw, ImageFilter
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("GOUTTE",         "Goutte",         24),
    ("NUAGE",          "Nuage",          36),
    ("PLUIE",          "Pluie",          50),
    ("ORAGE",          "Orage",          64),
    ("ARC-EN-CIEL",    "Arc-en-ciel",    80),
    ("TORNADE",        "Tornade",        98),
    ("OURAGAN",        "Ouragan",       120),
    ("SOLEIL SUPRÊME", "Soleil suprême", 150),
]
BOMB_R = 48
OUT = (35, 30, 60, 255)

WATER = ((215, 240, 255), (70, 165, 240), (20, 90, 185))
CLOUD = ((255, 255, 255), (238, 242, 252), (185, 195, 220))
RAINC = ((235, 240, 250), (175, 190, 215), (110, 125, 160))
STORM = ((200, 185, 240), (125, 100, 190), (65, 45, 120))
BOLT = ((255, 255, 210), (255, 220, 40), (230, 150, 0))
TEAL = ((205, 250, 240), (90, 200, 185), (30, 125, 115))
HURR = ((215, 225, 255), (120, 140, 230), (50, 60, 160))
SUN = ((255, 255, 210), (255, 205, 40), (245, 130, 0))
ICE = ((255, 255, 255), (205, 235, 255), (130, 180, 230))
RAINBOW = [(235, 50, 60), (255, 140, 30), (255, 215, 40), (60, 190, 90), (50, 130, 230), (140, 80, 220)]


def shape(img, cols, lw, draw):
    m = Image.new("L", img.size, 0)
    draw(ImageDraw.Draw(m))
    img.alpha_composite(gradient_fill(img.size, m, *cols))
    edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(max(3, (lw // 2) * 2 + 1)))
    img.alpha_composite(Image.composite(Image.new("RGBA", img.size, OUT), Image.new("RGBA", img.size, (0, 0, 0, 0)), edge))
    return m


def E(md, x, y, rx, ry):
    md.ellipse([x - rx, y - ry, x + rx, y + ry], fill=255)


def drop(md, x, y, s):
    md.ellipse([x - s, y - s * 0.2, x + s, y + 1.8 * s], fill=255)
    md.polygon([(x - s * 0.93, y + 0.5 * s), (x, y - 1.6 * s), (x + s * 0.93, y + 0.5 * s)], fill=255)


def cloud(md, c, R, cx=0.0, cy=0.0, k=1.0):
    x, y = c + cx * R, c + cy * R
    E(md, x - 0.55 * k * R, y + 0.15 * k * R, 0.45 * k * R, 0.4 * k * R)
    E(md, x + 0.55 * k * R, y + 0.15 * k * R, 0.45 * k * R, 0.4 * k * R)
    E(md, x - 0.15 * k * R, y - 0.25 * k * R, 0.55 * k * R, 0.55 * k * R)
    E(md, x + 0.35 * k * R, y - 0.1 * k * R, 0.45 * k * R, 0.45 * k * R)
    md.rounded_rectangle([x - 0.95 * k * R, y, x + 0.95 * k * R, y + 0.55 * k * R], 0.25 * k * R, fill=255)


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.65 if level >= 4 else 1.55
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    if level == 0:  # goutte
        shape(img, WATER, lw, lambda md: drop(md, c, c - 0.15 * R, 0.62 * R))
        draw_face(img, c, c + 0.4 * R, 0.6 * R, "happy")
    elif level == 1:  # nuage blanc
        shape(img, CLOUD, lw, lambda md: cloud(md, c, R, 0, 0.05))
        draw_face(img, c, c + 0.12 * R, 0.62 * R, "happy")
    elif level == 2:  # pluie : nuage gris + gouttes
        for x in (-0.55, 0.0, 0.55):
            shape(img, WATER, max(2, lw // 2), lambda md, x=x: drop(md, c + x * R, c + 0.85 * R + (0.12 * R if x == 0 else 0), 0.14 * R))
        shape(img, RAINC, lw, lambda md: cloud(md, c, R, 0, -0.2))
        draw_face(img, c, c - 0.08 * R, 0.6 * R, "sweat")
    elif level == 3:  # orage : nuage violet + éclair
        shape(img, BOLT, lw, lambda md: md.polygon([(c + 0.1 * R, c + 0.2 * R), (c - 0.25 * R, c + 0.8 * R), (c + 0.02 * R, c + 0.8 * R),
                                                     (c - 0.2 * R, c + 1.3 * R), (c + 0.4 * R, c + 0.6 * R), (c + 0.12 * R, c + 0.6 * R),
                                                     (c + 0.35 * R, c + 0.2 * R)], fill=255))
        shape(img, STORM, lw, lambda md: cloud(md, c, R, 0, -0.25))
        d = ImageDraw.Draw(img)
        for sx in (-1, 1):  # sourcils froncés
            x = c + sx * 0.22 * R
            d.line([(x - sx * 0.12 * R, c - 0.32 * R), (x + sx * 0.1 * R, c - 0.24 * R)], fill=OUT, width=int(0.06 * R))
        draw_face(img, c, c - 0.12 * R, 0.6 * R, "open")
    elif level == 4:  # arc-en-ciel
        d = ImageDraw.Draw(img)
        band = 0.13 * R
        rr = 1.0 * R
        d.pieslice([c - rr - 0.03 * R, c - rr + 0.2 * R - 0.03 * R, c + rr + 0.03 * R, c + rr + 0.2 * R + 0.03 * R], 180, 360, fill=OUT)
        for i, col in enumerate(RAINBOW):
            q = rr - i * band
            d.pieslice([c - q, c + 0.2 * R - q, c + q, c + 0.2 * R + q], 180, 360, fill=col + (255,))
        q = rr - 6 * band
        d.pieslice([c - q, c + 0.2 * R - q, c + q, c + 0.2 * R + q], 180, 360, fill=(0, 0, 0, 0))
        # efface le trou central proprement
        m = Image.new("L", img.size, 0); ImageDraw.Draw(m).pieslice([c - q + 3, c + 0.2 * R - q + 3, c + q - 3, c + 0.2 * R + q - 3], 180, 360, fill=255)
        img.putalpha(Image.composite(Image.new("L", img.size, 0), img.getchannel("A"), m))
        for sx in (-1, 1):
            shape(img, CLOUD, lw, lambda md, sx=sx: cloud(md, c, R, sx * 0.78, 0.28, 0.42))
        draw_face(img, c - 0.78 * R, c + 0.33 * R, 0.33 * R, "happy")
        draw_face(img, c + 0.78 * R, c + 0.33 * R, 0.33 * R, "happy")
    elif level == 5:  # tornade
        rows = 7
        for i in range(rows):
            t = i / (rows - 1)
            y = c - 0.85 * R + t * 1.65 * R
            w = (1.05 - 0.8 * t) * R
            xo = 0.12 * R * math.sin(t * 5)
            shape(img, TEAL, max(2, lw // 2 + 1), lambda md, y=y, w=w, xo=xo: E(md, c + xo, y, w, 0.19 * R))
        draw_face(img, c + 0.05 * R, c - 0.3 * R, 0.65 * R, "open")
    elif level == 6:  # ouragan : disque en spirale, œil au centre
        shape(img, HURR, lw, lambda md: E(md, c, c, 0.95 * R, 0.95 * R))
        d = ImageDraw.Draw(img)
        for arm in range(3):
            pts = []
            for k in range(60):
                t = k / 59
                a = arm * 2.094 + t * 4.2
                rad = (0.35 + 0.6 * t) * R
                pts.append((c + rad * math.cos(a), c + rad * math.sin(a)))
            d.line(pts, fill=(245, 248, 255, 255), width=int(0.08 * R))
        shape(img, CLOUD, lw, lambda md: E(md, c, c, 0.48 * R, 0.48 * R))
        draw_face(img, c, c, 0.5 * R, "open")
    elif level == 7:  # soleil suprême
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(16):
            a = k / 16 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.12), c + 0.5 * R * math.sin(a - 0.12)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.12), c + 0.5 * R * math.sin(a + 0.12))], fill=(255, 245, 150, 200) if k % 2 else (255, 190, 220, 200))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        def rays(md):
            for k in range(12):
                a = k / 12 * 6.283 + 0.13
                md.polygon([(c + 0.8 * R * math.cos(a - 0.2), c + 0.8 * R * math.sin(a - 0.2)), (c + 1.22 * R * math.cos(a), c + 1.22 * R * math.sin(a)),
                            (c + 0.8 * R * math.cos(a + 0.2), c + 0.8 * R * math.sin(a + 0.2))], fill=255)
        shape(img, ((255, 235, 150), (255, 160, 30), (230, 90, 0)), lw, rays)
        shape(img, SUN, lw, lambda md: E(md, c, c, 0.88 * R, 0.88 * R))
        # couronne
        shape(img, ((255, 250, 200), (255, 215, 60), (215, 145, 0)), lw, lambda md: md.polygon(
            [(c - 0.45 * R, c - 0.6 * R), (c - 0.5 * R, c - 1.05 * R), (c - 0.22 * R, c - 0.8 * R), (c, c - 1.15 * R),
             (c + 0.22 * R, c - 0.8 * R), (c + 0.5 * R, c - 1.05 * R), (c + 0.45 * R, c - 0.6 * R)], fill=255))
        d = ImageDraw.Draw(img)
        for (gx, gc) in ((-0.25, (230, 50, 90)), (0, (60, 140, 230)), (0.25, (60, 190, 90))):
            d.ellipse([c + gx * R - 0.06 * R, c - 0.76 * R, c + gx * R + 0.06 * R, c - 0.64 * R], fill=gc + (255,), outline=OUT, width=max(2, lw // 3))
        # lunettes de soleil
        for sx in (-1, 1):
            x = c + sx * 0.32 * R
            d.rounded_rectangle([x - 0.24 * R, c - 0.2 * R, x + 0.24 * R, c + 0.08 * R], 0.1 * R, fill=(40, 30, 70, 255))
            d.ellipse([x - 0.15 * R, c - 0.16 * R, x - 0.03 * R, c - 0.06 * R], fill=(255, 255, 255, 200))
        d.line([(c - 0.08 * R, c - 0.12 * R), (c + 0.08 * R, c - 0.12 * R)], fill=(40, 30, 70, 255), width=int(0.05 * R))
        d.arc([c - 0.3 * R, c + 0.05 * R, c + 0.3 * R, c + 0.45 * R], 20, 160, fill=OUT, width=int(0.06 * R))
        for sx in (-1, 1):
            d.ellipse([c + sx * 0.6 * R - 0.12 * R, c + 0.15 * R, c + sx * 0.6 * R + 0.12 * R, c + 0.3 * R], fill=(255, 120, 130, 160))
        for (sx, sy, ss) in ((-1.15, -0.9, 0.16), (1.15, -0.85, 0.14), (1.2, 0.6, 0.12), (-1.2, 0.55, 0.11)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
            star(img, c + sx * R, c + sy * R, ss * 0.55 * R, (255, 200, 60, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """LA GRÊLE ! : gros grêlon de glace à pointes, l'air fâché."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    def spiky(md):
        pts = []
        for k in range(24):
            a = k / 24 * 6.283
            rad = (1.05 if k % 2 == 0 else 0.8) * R
            pts.append((c + rad * math.cos(a), c + rad * math.sin(a)))
        md.polygon(pts, fill=255)
    shape(img, ICE, lw, spiky)
    d = ImageDraw.Draw(img)
    for (x, y, s) in ((-0.4, -0.45, 0.12), (0.45, 0.4, 0.09), (-0.5, 0.35, 0.07)):
        d.ellipse([c + x * R - s * R, c + y * R - s * R, c + x * R + s * R, c + y * R + s * R], fill=(255, 255, 255, 220))
    for sx in (-1, 1):
        x = c + sx * 0.3 * R; cy = c - 0.05 * R
        d.ellipse([x - 0.15 * R, cy - 0.12 * R, x + 0.15 * R, cy + 0.18 * R], fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=max(2, lw // 2))
        d.ellipse([x - 0.07 * R, cy - 0.01 * R, x + 0.07 * R, cy + 0.13 * R], fill=(10, 10, 10, 255))
        d.line([(x - sx * 0.22 * R, cy - 0.32 * R), (x + sx * 0.16 * R, cy - 0.14 * R)], fill=(20, 20, 20, 255), width=int(0.08 * R))
    d.arc([c - 0.22 * R, c + 0.28 * R, c + 0.22 * R, c + 0.5 * R], 200, 340, fill=(20, 20, 20, 255), width=int(0.07 * R))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(70, 40, 120, 255), glow=(255, 255, 255)):
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
    sheet = Image.new("RGBA", (W, H), (200, 180, 255, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
