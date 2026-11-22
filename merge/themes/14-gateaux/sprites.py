"""GÂTEAUX MERGE (épisode 14) : miette → gâteau géant + LA FOURCHETTE ! (rebondissement).
Tous les personnages sont inventés."""
import math
from PIL import Image, ImageDraw, ImageFilter
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("MIETTE",            "Miette",            24),
    ("COOKIE",            "Cookie",            36),
    ("DONUT",             "Donut",             50),
    ("CUPCAKE",           "Cupcake",           64),
    ("PART DE GÂTEAU",    "Part de gâteau",    80),
    ("GÂTEAU D'ANNIV",    "Gâteau d'anniversaire", 98),
    ("PIÈCE MONTÉE",      "Pièce montée",     120),
    ("GÂTEAU GÉANT",      "Gâteau géant",     150),
]
BOMB_R = 48
OUT = (70, 35, 30, 255)

CRUMB = ((255, 230, 170), (225, 170, 90), (165, 105, 45))
COOK = ((255, 225, 160), (220, 160, 80), (160, 95, 40))
CHOC = ((150, 95, 70), (95, 55, 35), (55, 30, 20))
DOUGH = ((255, 220, 160), (235, 170, 90), (190, 115, 50))
PINK = ((255, 220, 240), (255, 140, 195), (220, 70, 140))
CREAM = ((255, 255, 250), (255, 245, 225), (230, 210, 185))
SPONGE = ((255, 240, 190), (250, 210, 120), (215, 160, 70))
STRAW = ((255, 180, 190), (235, 60, 80), (170, 20, 50))
MINT = ((215, 255, 235), (130, 225, 185), (60, 170, 130))
LAV = ((235, 225, 255), (185, 160, 245), (120, 90, 200))
GOLDC = ((255, 250, 200), (255, 210, 60), (215, 140, 0))
METAL = ((255, 255, 255), (205, 212, 225), (130, 140, 160))
SPRINK = [(235, 60, 80), (60, 150, 235), (255, 210, 40), (90, 200, 110), (170, 90, 230), (255, 255, 255)]


def shape(img, cols, lw, draw):
    m = Image.new("L", img.size, 0)
    draw(ImageDraw.Draw(m))
    img.alpha_composite(gradient_fill(img.size, m, *cols))
    edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(max(3, (lw // 2) * 2 + 1)))
    img.alpha_composite(Image.composite(Image.new("RGBA", img.size, OUT), Image.new("RGBA", img.size, (0, 0, 0, 0)), edge))
    return m


def E(md, x, y, rx, ry):
    md.ellipse([x - rx, y - ry, x + rx, y + ry], fill=255)


def sprinkles(img, cx, cy, w, h, n, R, seed=1):
    d = ImageDraw.Draw(img)
    import random
    rnd = random.Random(seed)
    for i in range(n):
        x = cx + (rnd.random() - 0.5) * w; y = cy + (rnd.random() - 0.5) * h
        a = rnd.random() * 3.14; l = 0.07 * R
        d.line([(x - l * math.cos(a), y - l * math.sin(a)), (x + l * math.cos(a), y + l * math.sin(a))],
               fill=SPRINK[i % len(SPRINK)] + (255,), width=max(2, int(0.045 * R)))


def drip_top(md, x0, x1, y, h, n):
    """glaçage : bande + gouttes."""
    md.rectangle([x0, y - h, x1, y], fill=255)
    step = (x1 - x0) / n
    for i in range(n):
        x = x0 + step * (i + 0.5)
        dh = h * (0.6 + 0.5 * ((i * 7) % 3) / 2)
        md.ellipse([x - step * 0.32, y - step * 0.3, x + step * 0.32, y + dh], fill=255)


def candle(img, x, ytop, R, lw, col):
    shape(img, ((255, 255, 255), col, tuple(max(0, v - 70) for v in col)), max(2, lw // 2),
          lambda md: md.rounded_rectangle([x - 0.05 * R, ytop, x + 0.05 * R, ytop + 0.3 * R], 0.03 * R, fill=255))
    shape(img, ((255, 255, 200), (255, 190, 40), (255, 110, 0)), max(2, lw // 2),
          lambda md: (E(md, x, ytop - 0.08 * R, 0.05 * R, 0.08 * R),
                      md.polygon([(x - 0.045 * R, ytop - 0.09 * R), (x, ytop - 0.22 * R), (x + 0.045 * R, ytop - 0.09 * R)], fill=255)))


def tier(img, c, x_c, y_top, w, h, R, lw, body, icing, seed):
    shape(img, body, lw, lambda md: md.rounded_rectangle([x_c - w, y_top, x_c + w, y_top + h], 0.08 * R, fill=255))
    shape(img, icing, max(2, lw - 1), lambda md: drip_top(md, x_c - w, x_c + w, y_top + 0.12 * h, 0.12 * h + 2, max(4, int(w / (0.12 * R)))))


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.65 if level >= 4 else 1.55
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    if level == 0:  # miette
        pts = [(c + R * 0.85 * math.cos(a) * (1 + 0.15 * math.sin(3 * a)), c + R * 0.75 * math.sin(a) * (1 + 0.12 * math.cos(5 * a)))
               for a in [k / 30 * 6.283 for k in range(30)]]
        shape(img, CRUMB, lw, lambda md: md.polygon(pts, fill=255))
        draw_face(img, c, c, 0.65 * R, "happy")
    elif level == 1:  # cookie
        shape(img, COOK, lw, lambda md: E(md, c, c, 0.95 * R, 0.92 * R))
        d = ImageDraw.Draw(img)
        for (x, y) in ((-0.55, -0.45), (0.5, -0.5), (-0.65, 0.35), (0.6, 0.4), (0.05, 0.62), (-0.1, -0.7)):
            d.ellipse([c + x * R - 0.1 * R, c + y * R - 0.09 * R, c + x * R + 0.1 * R, c + y * R + 0.09 * R], fill=CHOC[1] + (255,))
        draw_face(img, c, c, 0.62 * R, "happy")
    elif level == 2:  # donut rose
        shape(img, DOUGH, lw, lambda md: E(md, c, c, 0.98 * R, 0.9 * R))
        shape(img, PINK, lw, lambda md: [E(md, c + 0.75 * R * math.cos(a), c - 0.05 * R + 0.65 * R * math.sin(a), 0.32 * R, 0.3 * R)
                                         for a in [k / 18 * 6.283 for k in range(18)]])
        sprinkles(img, c, c - 0.05 * R, 1.6 * R, 1.3 * R, 16, R, seed=3)
        m = Image.new("L", img.size, 0); E(ImageDraw.Draw(m), c, c - 0.05 * R, 0.28 * R, 0.24 * R)
        img.putalpha(Image.composite(Image.new("L", img.size, 0), img.getchannel("A"), m))
        d = ImageDraw.Draw(img)
        d.ellipse([c - 0.3 * R, c - 0.05 * R - 0.26 * R, c + 0.3 * R, c - 0.05 * R + 0.26 * R], outline=OUT, width=lw)
        draw_face(img, c, c + 0.5 * R, 0.42 * R, "happy")
    elif level == 3:  # cupcake
        shape(img, ((190, 230, 255), (90, 170, 235), (40, 100, 180)), lw,
              lambda md: md.polygon([(c - 0.8 * R, c + 0.05 * R), (c + 0.8 * R, c + 0.05 * R), (c + 0.55 * R, c + 0.95 * R), (c - 0.55 * R, c + 0.95 * R)], fill=255))
        d = ImageDraw.Draw(img)
        for k in range(-3, 4):
            d.line([(c + k * 0.2 * R, c + 0.1 * R), (c + k * 0.14 * R, c + 0.9 * R)], fill=(40, 100, 180, 255), width=max(2, lw // 2))
        shape(img, PINK, lw, lambda md: (E(md, c, c - 0.05 * R, 0.88 * R, 0.32 * R), E(md, c, c - 0.35 * R, 0.66 * R, 0.3 * R), E(md, c, c - 0.62 * R, 0.42 * R, 0.25 * R)))
        sprinkles(img, c, c - 0.3 * R, 1.2 * R, 0.6 * R, 10, R, seed=5)
        shape(img, STRAW, lw, lambda md: E(md, c, c - 0.92 * R, 0.17 * R, 0.17 * R))
        draw_face(img, c, c + 0.45 * R, 0.5 * R, "open")
    elif level == 4:  # part de gâteau (triangle)
        pts = [(c - 0.95 * R, c + 0.7 * R), (c + 0.95 * R, c + 0.7 * R), (c + 0.95 * R, c - 0.35 * R), (c - 0.95 * R, c + 0.05 * R)]
        shape(img, SPONGE, lw, lambda md: md.polygon(pts, fill=255))
        d = ImageDraw.Draw(img)
        for t in (0.35, 0.65):
            d.line([(c - 0.95 * R, c + 0.05 * R + t * 0.65 * R), (c + 0.95 * R, c - 0.35 * R + t * 1.05 * R)], fill=(235, 80, 110, 255), width=int(0.09 * R))
        shape(img, CREAM, lw, lambda md: md.polygon([(c - 0.95 * R, c + 0.05 * R), (c + 0.95 * R, c - 0.35 * R), (c + 0.95 * R, c - 0.55 * R), (c - 0.95 * R, c - 0.12 * R)], fill=255))
        shape(img, STRAW, lw, lambda md: E(md, c + 0.55 * R, c - 0.62 * R, 0.2 * R, 0.18 * R))
        draw_face(img, c, c + 0.32 * R, 0.55 * R, "happy")
    elif level == 5:  # gâteau d'anniversaire
        tier(img, c, c, c - 0.25 * R, 0.92 * R, 1.0 * R, R, lw, LAV, CREAM, 1)
        sprinkles(img, c, c + 0.62 * R, 1.6 * R, 0.14 * R, 12, R, seed=7)
        for i, x in enumerate((-0.5, 0, 0.5)):
            candle(img, c + x * R, c - 0.55 * R, R, lw, [(235, 80, 150), (60, 150, 235), (90, 200, 110)][i])
        draw_face(img, c, c + 0.12 * R, 0.55 * R, "open")
    elif level == 6:  # pièce montée : 3 étages
        tier(img, c, c, c + 0.25 * R, 0.95 * R, 0.6 * R, R, lw, MINT, CREAM, 1)
        tier(img, c, c, c - 0.25 * R, 0.68 * R, 0.52 * R, R, lw, PINK, CREAM, 2)
        tier(img, c, c, c - 0.68 * R, 0.42 * R, 0.45 * R, R, lw, LAV, CREAM, 3)
        shape(img, STRAW, lw, lambda md: E(md, c, c - 0.82 * R, 0.14 * R, 0.14 * R))
        for y in (c - 0.47 * R, c - 0.02 * R):
            for x in (-1, 1):
                pass
        draw_face(img, c, c + 0.55 * R, 0.5 * R, "happy")
    elif level == 7:  # gâteau géant doré
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(16):
            a = k / 16 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.12), c + 0.5 * R * math.sin(a - 0.12)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.12), c + 0.5 * R * math.sin(a + 0.12))], fill=(255, 245, 150, 190) if k % 2 else (255, 190, 220, 190))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        tier(img, c, c, c - 0.2 * R, 0.95 * R, 1.0 * R, R, lw, ((255, 200, 230), (245, 120, 175), (190, 60, 120)), GOLDC, 1)
        sprinkles(img, c, c + 0.66 * R, 1.6 * R, 0.14 * R, 16, R, seed=9)
        # couronne
        shape(img, GOLDC, lw, lambda md: md.polygon(
            [(c - 0.45 * R, c - 0.3 * R), (c - 0.5 * R, c - 0.8 * R), (c - 0.22 * R, c - 0.55 * R), (c, c - 0.92 * R),
             (c + 0.22 * R, c - 0.55 * R), (c + 0.5 * R, c - 0.8 * R), (c + 0.45 * R, c - 0.3 * R)], fill=255))
        d = ImageDraw.Draw(img)
        for (gx, gc) in ((-0.25, (230, 50, 90)), (0, (60, 140, 230)), (0.25, (60, 190, 90))):
            d.ellipse([c + gx * R - 0.06 * R, c - 0.5 * R, c + gx * R + 0.06 * R, c - 0.38 * R], fill=gc + (255,), outline=OUT, width=max(2, lw // 3))
        draw_face(img, c, c + 0.18 * R, 0.6 * R, "open")
        for (sx, sy, ss) in ((-1.15, -0.9, 0.16), (1.15, -0.85, 0.14), (1.2, 0.6, 0.12), (-1.2, 0.55, 0.11)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
            star(img, c + sx * R, c + sy * R, ss * 0.55 * R, (255, 200, 60, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """LA FOURCHETTE ! : fourchette géante en métal, l'air gourmand."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    def fork(md):
        md.rounded_rectangle([c - 0.18 * R, c + 0.1 * R, c + 0.18 * R, c + 1.35 * R], 0.15 * R, fill=255)
        md.rounded_rectangle([c - 0.6 * R, c - 0.35 * R, c + 0.6 * R, c + 0.3 * R], 0.3 * R, fill=255)
        for x in (-0.48, -0.16, 0.16, 0.48):
            md.rounded_rectangle([c + x * R - 0.1 * R, c - 1.25 * R, c + x * R + 0.1 * R, c - 0.2 * R], 0.08 * R, fill=255)
    shape(img, METAL, lw, fork)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        x = c + sx * 0.26 * R; cy = c - 0.08 * R
        d.ellipse([x - 0.13 * R, cy - 0.12 * R, x + 0.13 * R, cy + 0.14 * R], fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=max(2, lw // 2))
        d.ellipse([x - 0.06 * R, cy - 0.02 * R, x + 0.06 * R, cy + 0.1 * R], fill=(10, 10, 10, 255))
        d.line([(x - sx * 0.18 * R, cy - 0.28 * R), (x + sx * 0.12 * R, cy - 0.18 * R)], fill=(20, 20, 20, 255), width=int(0.07 * R))
    d.arc([c - 0.2 * R, c + 0.02 * R, c + 0.2 * R, c + 0.24 * R], 20, 160, fill=(20, 20, 20, 255), width=int(0.06 * R))
    d.ellipse([c + 0.08 * R, c + 0.18 * R, c + 0.2 * R, c + 0.3 * R], fill=(255, 110, 140, 255), outline=(20, 20, 20, 255), width=max(2, lw // 3))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(30, 110, 85, 255), glow=(255, 255, 255)):
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
    sheet = Image.new("RGBA", (W, H), (165, 235, 205, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
