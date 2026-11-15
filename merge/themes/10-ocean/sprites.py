"""OCÉAN MERGE (épisode 10) : bulle → baleine céleste + UN FILET ! (rebondissement).
Tous les personnages sont inventés."""
import math
from PIL import Image, ImageDraw, ImageFilter
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("BULLE",            "Bulle",            24),
    ("CREVETTE",         "Crevette",         36),
    ("POISSON",          "Poisson",          50),
    ("CRABE",            "Crabe",            64),
    ("POULPE",           "Poulpe",           80),
    ("DAUPHIN",          "Dauphin",          98),
    ("REQUIN",           "Requin",          120),
    ("BALEINE CÉLESTE",  "Baleine céleste", 150),
]
BOMB_R = 48
OUT = (30, 35, 60, 255)

BUBBLE = ((235, 250, 255), (160, 220, 250), (80, 160, 220))
PINK = ((255, 190, 170), (250, 115, 95), (195, 55, 45))
YELLOW = ((255, 245, 170), (255, 200, 40), (215, 130, 0))
RED = ((255, 175, 150), (235, 75, 55), (160, 30, 25))
PURPLE = ((230, 200, 255), (165, 105, 235), (95, 50, 170))
DOLPH = ((200, 230, 255), (110, 165, 225), (50, 95, 170))
SHARK = ((215, 225, 240), (140, 160, 190), (75, 90, 125))
WHITE = ((255, 255, 255), (245, 248, 252), (205, 215, 230))
WHALE = ((200, 215, 255), (95, 115, 230), (45, 50, 160))
GOLD = ((255, 250, 190), (255, 205, 50), (205, 135, 0))
NET = ((235, 215, 170), (200, 165, 100), (140, 105, 50))


def shape(img, cols, lw, draw):
    m = Image.new("L", img.size, 0)
    draw(ImageDraw.Draw(m))
    img.alpha_composite(gradient_fill(img.size, m, *cols))
    edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(max(3, (lw // 2) * 2 + 1)))
    img.alpha_composite(Image.composite(Image.new("RGBA", img.size, OUT), Image.new("RGBA", img.size, (0, 0, 0, 0)), edge))
    return m


def E(md, x, y, rx, ry):
    md.ellipse([x - rx, y - ry, x + rx, y + ry], fill=255)


def shine(img, x, y, r):
    d = ImageDraw.Draw(img)
    d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(255, 255, 255, 200))


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.65 if level >= 4 else 1.5
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    if level == 0:  # bulle
        shape(img, BUBBLE, lw, lambda md: E(md, c, c, 1.0 * R, 1.0 * R))
        shine(img, c - 0.45 * R, c - 0.5 * R, 0.22 * R)
        draw_face(img, c, c + 0.12 * R, 0.85 * R, "happy")
    elif level == 1:  # crevette rose recourbée
        def body(md):
            outer, inner = [], []
            n = 40
            for i in range(n + 1):
                t = i / n
                a = math.radians(170 + 250 * t)
                th = 0.62 - 0.42 * t
                rm = 0.6 * R
                outer.append((c + (rm + th * R / 2) * math.cos(a), c + (rm + th * R / 2) * math.sin(a)))
                inner.append((c + (rm - th * R / 2) * math.cos(a), c + (rm - th * R / 2) * math.sin(a)))
            md.polygon(outer + inner[::-1], fill=255)
        ex, ey = c + 0.6 * R * math.cos(math.radians(60)), c + 0.6 * R * math.sin(math.radians(60))
        shape(img, PINK, lw, lambda md: md.polygon([(ex, ey), (ex + 0.55 * R, ey - 0.1 * R), (ex + 0.35 * R, ey + 0.45 * R)], fill=255))
        shape(img, PINK, lw, body)
        d = ImageDraw.Draw(img)
        for k in range(1, 6):
            a = math.radians(170 + 250 * k / 6)
            th = 0.62 - 0.42 * k / 6
            d.line([(c + (0.6 * R - th * R / 2) * math.cos(a), c + (0.6 * R - th * R / 2) * math.sin(a)),
                    (c + (0.6 * R + th * R / 2) * math.cos(a), c + (0.6 * R + th * R / 2) * math.sin(a))], fill=(200, 70, 60, 255), width=max(2, lw // 2))
        hx, hy = c - 0.62 * R, c + 0.2 * R
        shape(img, PINK, lw, lambda md: E(md, hx, hy, 0.42 * R, 0.4 * R))
        d = ImageDraw.Draw(img)
        for sx in (0.0, 0.3):
            d.line([(hx - 0.1 * R, hy - 0.3 * R), (hx - 0.5 * R + sx * R, hy - 1.15 * R)], fill=OUT, width=max(2, lw // 2))
        draw_face(img, hx, hy + 0.05 * R, 0.5 * R, "open")
    elif level == 2:  # poisson jaune rond
        shape(img, YELLOW, lw, lambda md: md.polygon([(c + 0.6 * R, c), (c + 1.3 * R, c - 0.6 * R), (c + 1.15 * R, c), (c + 1.3 * R, c + 0.6 * R)], fill=255))
        shape(img, YELLOW, lw, lambda md: md.polygon([(c - 0.3 * R, c - 0.7 * R), (c + 0.2 * R, c - 1.15 * R), (c + 0.45 * R, c - 0.6 * R)], fill=255))
        shape(img, YELLOW, lw, lambda md: E(md, c - 0.1 * R, c, 0.9 * R, 0.78 * R))
        d = ImageDraw.Draw(img)
        for k in range(3):
            x = c + 0.1 * R + k * 0.18 * R
            d.arc([x - 0.15 * R, c - 0.45 * R, x + 0.15 * R, c + 0.45 * R], 300, 60, fill=(240, 140, 0, 255), width=max(2, lw // 2))
        draw_face(img, c - 0.35 * R, c, 0.6 * R, "happy")
    elif level == 3:  # crabe rouge
        for sx in (-1, 1):
            for k in range(3):
                y = c + 0.15 * R + k * 0.22 * R
                ImageDraw.Draw(img).line([(c + sx * 0.7 * R, y), (c + sx * 1.25 * R, y + 0.3 * R)], fill=OUT, width=max(3, lw))
            shape(img, RED, lw, lambda md, sx=sx: md.pieslice([c + sx * 1.0 * R - 0.42 * R, c - 1.25 * R, c + sx * 1.0 * R + 0.42 * R, c - 0.45 * R], 20 if sx < 0 else -200, 300 if sx < 0 else 80, fill=255))
            ImageDraw.Draw(img).line([(c + sx * 0.5 * R, c - 0.3 * R), (c + sx * 0.9 * R, c - 0.6 * R)], fill=OUT, width=max(3, lw))
        shape(img, RED, lw, lambda md: E(md, c, c + 0.05 * R, 0.95 * R, 0.62 * R))
        for sx in (-1, 1):
            ImageDraw.Draw(img).line([(c + sx * 0.25 * R, c - 0.4 * R), (c + sx * 0.3 * R, c - 0.75 * R)], fill=OUT, width=max(3, lw))
            shape(img, WHITE, max(2, lw // 2), lambda md, sx=sx: E(md, c + sx * 0.3 * R, c - 0.8 * R, 0.17 * R, 0.17 * R))
            d = ImageDraw.Draw(img); d.ellipse([c + sx * 0.3 * R - 0.08 * R, c - 0.84 * R, c + sx * 0.3 * R + 0.08 * R, c - 0.68 * R], fill=(10, 10, 10, 255))
        d = ImageDraw.Draw(img)
        d.arc([c - 0.3 * R, c - 0.15 * R, c + 0.3 * R, c + 0.3 * R], 20, 160, fill=OUT, width=max(3, lw))
        for sx in (-1, 1):
            d.ellipse([c + sx * 0.6 * R - 0.12 * R, c - 0.02 * R, c + sx * 0.6 * R + 0.12 * R, c + 0.14 * R], fill=(255, 140, 150, 200))
    elif level == 4:  # poulpe violet
        for k in range(6):
            x = c - 0.85 * R + k * 0.34 * R
            shape(img, PURPLE, lw, lambda md, x=x, k=k: (md.rounded_rectangle([x - 0.15 * R, c + 0.1 * R, x + 0.15 * R, c + 1.05 * R], 0.15 * R, fill=255), E(md, x + (0.12 if k % 2 else -0.12) * R, c + 1.02 * R, 0.17 * R, 0.13 * R)))
        shape(img, PURPLE, lw, lambda md: (E(md, c, c - 0.25 * R, 0.95 * R, 0.95 * R), md.rectangle([c - 0.95 * R, c - 0.25 * R, c + 0.95 * R, c + 0.35 * R], fill=255)))
        d = ImageDraw.Draw(img)
        for (x, y, s) in ((-0.5, -0.8, 0.1), (0.55, -0.7, 0.08), (0.65, -0.35, 0.06)):
            d.ellipse([c + x * R - s * R, c + y * R - s * R, c + x * R + s * R, c + y * R + s * R], fill=(255, 220, 255, 230))
        draw_face(img, c, c - 0.05 * R, 0.8 * R, "open")
    elif level == 5:  # dauphin bleu qui saute
        shape(img, DOLPH, lw, lambda md: md.polygon([(c + 0.85 * R, c + 0.4 * R), (c + 1.4 * R, c + 0.05 * R), (c + 1.25 * R, c + 0.55 * R), (c + 1.45 * R, c + 0.95 * R)], fill=255))
        shape(img, DOLPH, lw, lambda md: md.polygon([(c - 0.1 * R, c - 0.55 * R), (c + 0.35 * R, c - 1.15 * R), (c + 0.45 * R, c - 0.5 * R)], fill=255))
        shape(img, DOLPH, lw, lambda md: (E(md, c, c + 0.05 * R, 1.0 * R, 0.62 * R), E(md, c - 1.05 * R, c + 0.2 * R, 0.35 * R, 0.16 * R)))
        shape(img, WHITE, max(2, lw // 2), lambda md: E(md, c - 0.2 * R, c + 0.35 * R, 0.7 * R, 0.25 * R))
        draw_face(img, c - 0.45 * R, c - 0.05 * R, 0.55 * R, "happy")
        star(img, c + 0.9 * R, c - 0.8 * R, 0.15 * R, (255, 255, 255, 255))
    elif level == 6:  # requin gris tout gentil
        shape(img, SHARK, lw, lambda md: md.polygon([(c + 0.85 * R, c), (c + 1.45 * R, c - 0.7 * R), (c + 1.25 * R, c + 0.05 * R), (c + 1.4 * R, c + 0.6 * R)], fill=255))
        shape(img, SHARK, lw, lambda md: md.polygon([(c - 0.3 * R, c - 0.6 * R), (c + 0.15 * R, c - 1.35 * R), (c + 0.45 * R, c - 0.55 * R)], fill=255))
        shape(img, SHARK, lw, lambda md: E(md, c, c, 1.05 * R, 0.68 * R))
        shape(img, WHITE, max(2, lw // 2), lambda md: md.chord([c - 1.0 * R, c - 0.3 * R, c + 0.9 * R, c + 0.68 * R], 0, 180, fill=255))
        draw_face(img, c - 0.4 * R, c - 0.05 * R, 0.6 * R, "happy")
        d = ImageDraw.Draw(img)
        for k in range(3):
            x = c + 0.35 * R + k * 0.13 * R
            d.arc([x - 0.08 * R, c - 0.3 * R, x + 0.08 * R, c + 0.1 * R], 270, 90, fill=OUT, width=max(2, lw // 2))
        # petit cœur
        hx, hy, s = c + 0.75 * R, c - 0.85 * R, 0.16 * R
        d.ellipse([hx - s, hy - s, hx, hy], fill=(240, 70, 110, 255)); d.ellipse([hx, hy - s, hx + s, hy], fill=(240, 70, 110, 255))
        d.polygon([(hx - s, hy - s * 0.45), (hx + s, hy - s * 0.45), (hx, hy + s)], fill=(240, 70, 110, 255))
    elif level == 7:  # baleine céleste : bleu, couronne d'or, jet d'eau étoilé, halo
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(16):
            a = k / 16 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.12), c + 0.5 * R * math.sin(a - 0.12)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.12), c + 0.5 * R * math.sin(a + 0.12))], fill=(255, 240, 130, 210) if k % 2 else (150, 230, 255, 210))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        shape(img, WHALE, lw, lambda md: md.polygon([(c + 0.8 * R, c + 0.1 * R), (c + 1.45 * R, c - 0.55 * R), (c + 1.25 * R, c + 0.2 * R), (c + 1.5 * R, c + 0.7 * R)], fill=255))
        shape(img, WHALE, lw, lambda md: E(md, c - 0.1 * R, c + 0.15 * R, 1.1 * R, 0.8 * R))
        shape(img, ((255, 245, 235), (230, 225, 250), (170, 170, 220)), max(2, lw // 2), lambda md: md.chord([c - 1.15 * R, c - 0.15 * R, c + 0.9 * R, c + 0.95 * R], 0, 180, fill=255))
        d = ImageDraw.Draw(img)
        for k in range(4):
            y = c + 0.55 * R + k * 0.08 * R
            d.line([(c - 0.75 * R + k * 0.05 * R, y), (c + 0.5 * R - k * 0.1 * R, y)], fill=(170, 170, 220, 255), width=max(2, lw // 3))
        draw_face(img, c - 0.45 * R, c + 0.1 * R, 0.65 * R, "open")
        # jet d'eau
        for sx in (-1, 0, 1):
            d.line([(c - 0.05 * R, c - 0.62 * R), (c - 0.05 * R + sx * 0.35 * R, c - 1.2 * R)], fill=(120, 210, 255, 255), width=max(3, lw))
        # couronne
        cx0 = c + 0.3 * R
        shape(img, GOLD, max(2, lw // 2), lambda md: md.polygon([(cx0 - 0.35 * R, c - 0.55 * R), (cx0 - 0.35 * R, c - 0.95 * R), (cx0 - 0.17 * R, c - 0.75 * R), (cx0, c - 1.05 * R), (cx0 + 0.17 * R, c - 0.75 * R), (cx0 + 0.35 * R, c - 0.95 * R), (cx0 + 0.35 * R, c - 0.55 * R)], fill=255))
        for (sx, sy, ss) in ((-0.5, -1.25, 0.14), (0.45, -1.3, 0.12), (1.3, 0.95, 0.11), (-1.2, -0.6, 0.1), (-1.25, 0.9, 0.1)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """UN FILET ! : filet de pêche rond, quadrillé, l'air grognon, avec des flotteurs."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    d = ImageDraw.Draw(img)
    for k in range(3):
        y = c - 0.6 * R + k * 0.5 * R
        d.line([(c + 1.0 * R, y), (c + 1.6 * R, y - 0.4 * R)], fill=(255, 255, 255, 230), width=int(0.08 * R))
    m = shape(img, NET, lw, lambda md: E(md, c, c, 1.0 * R, 1.0 * R))
    grid = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(grid)
    step = 0.28 * R
    for k in range(-8, 9):
        gd.line([(c + k * step - 1.2 * R, c - 1.2 * R), (c + k * step + 1.2 * R, c + 1.2 * R)], fill=(110, 75, 30, 255), width=max(2, lw // 2))
        gd.line([(c + k * step + 1.2 * R, c - 1.2 * R), (c + k * step - 1.2 * R, c + 1.2 * R)], fill=(110, 75, 30, 255), width=max(2, lw // 2))
    grid.putalpha(Image.fromarray(__import__("numpy").minimum(__import__("numpy").array(grid.getchannel("A")), __import__("numpy").array(m.filter(ImageFilter.MinFilter(9))))))
    img.alpha_composite(grid)
    for a in range(0, 360, 60):
        x, y = c + 1.0 * R * math.cos(math.radians(a)), c + 1.0 * R * math.sin(math.radians(a))
        shape(img, RED, max(2, lw // 2), lambda md, x=x, y=y: E(md, x, y, 0.15 * R, 0.15 * R))
    shape(img, WHITE, lw, lambda md: E(md, c, c - 0.05 * R, 0.6 * R, 0.45 * R))
    d = ImageDraw.Draw(img)
    cx, cy = c, c - 0.15 * R
    for sx in (-1, 1):
        x = cx + sx * 0.25 * R
        d.ellipse([x - 0.13 * R, cy - 0.08 * R, x + 0.13 * R, cy + 0.18 * R], fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=max(2, lw // 2))
        d.ellipse([x - 0.06 * R, cy + 0.0 * R, x + 0.06 * R, cy + 0.13 * R], fill=(10, 10, 10, 255))
        d.line([(x - sx * 0.18 * R, cy - 0.26 * R), (x + sx * 0.13 * R, cy - 0.12 * R)], fill=(20, 20, 20, 255), width=int(0.07 * R))
    d.arc([cx - 0.18 * R, cy + 0.27 * R, cx + 0.18 * R, cy + 0.5 * R], 200, 340, fill=(20, 20, 20, 255), width=int(0.06 * R))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(70, 25, 30, 255), glow=(255, 255, 255)):
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
    sheet = Image.new("RGBA", (W, H), (255, 172, 165, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
