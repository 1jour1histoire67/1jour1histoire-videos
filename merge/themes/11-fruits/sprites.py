"""FRUITS MERGE (épisode 11) : pépin → pastèque dorée + UN MIXEUR ! (rebondissement).
Tous les personnages sont inventés."""
import math
from PIL import Image, ImageDraw, ImageFilter
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("PÉPIN",           "Pépin",           24),
    ("CERISE",          "Cerise",          36),
    ("FRAISE",          "Fraise",          50),
    ("CITRON",          "Citron",          64),
    ("ORANGE",          "Orange",          80),
    ("POMME",           "Pomme",           98),
    ("ANANAS",          "Ananas",         120),
    ("PASTÈQUE DORÉE",  "Pastèque dorée", 150),
]
BOMB_R = 48
OUT = (45, 30, 40, 255)

SEED = ((200, 150, 110), (130, 80, 45), (75, 40, 20))
CHERRY = ((255, 160, 170), (225, 30, 55), (140, 10, 30))
STRAW = ((255, 150, 140), (240, 50, 60), (165, 20, 35))
LEMON = ((255, 255, 190), (255, 230, 50), (220, 170, 0))
ORANGE = ((255, 215, 150), (255, 145, 30), (215, 85, 0))
APPLE = ((215, 255, 170), (125, 210, 60), (60, 140, 30))
PINE = ((255, 240, 160), (240, 180, 40), (180, 115, 10))
LEAF = ((190, 255, 170), (70, 185, 70), (25, 115, 40))
MELON = ((200, 255, 180), (60, 175, 70), (20, 105, 40))
FLESH = ((255, 190, 200), (250, 85, 110), (200, 40, 70))
GOLD = ((255, 250, 190), (255, 205, 50), (205, 135, 0))
STEEL = ((245, 250, 255), (185, 200, 220), (110, 125, 150))
GLASS = ((230, 245, 255), (170, 210, 240), (110, 160, 210))
WHITE = ((255, 255, 255), (245, 248, 252), (205, 215, 230))


def shape(img, cols, lw, draw):
    m = Image.new("L", img.size, 0)
    draw(ImageDraw.Draw(m))
    img.alpha_composite(gradient_fill(img.size, m, *cols))
    edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(max(3, (lw // 2) * 2 + 1)))
    img.alpha_composite(Image.composite(Image.new("RGBA", img.size, OUT), Image.new("RGBA", img.size, (0, 0, 0, 0)), edge))
    return m


def E(md, x, y, rx, ry):
    md.ellipse([x - rx, y - ry, x + rx, y + ry], fill=255)


def leaf(img, x, y, R, ang, lw, size=0.35):
    a = math.radians(ang)
    tx, ty = x + size * 2 * R * math.cos(a), y + size * 2 * R * math.sin(a)
    nx, ny = -math.sin(a) * size * 0.6 * R, math.cos(a) * size * 0.6 * R
    mx, my = (x + tx) / 2, (y + ty) / 2
    shape(img, LEAF, lw, lambda md: md.polygon([(x, y), (mx + nx, my + ny), (tx, ty), (mx - nx, my - ny)], fill=255))


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.65 if level >= 4 else 1.55
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    if level == 0:  # pépin en goutte
        shape(img, SEED, lw, lambda md: (E(md, c, c + 0.15 * R, 0.85 * R, 0.85 * R),
                                          md.polygon([(c - 0.6 * R, c - 0.3 * R), (c, c - 1.15 * R), (c + 0.6 * R, c - 0.3 * R)], fill=255)))
        draw_face(img, c, c + 0.2 * R, 0.8 * R, "happy")
    elif level == 1:  # deux cerises
        d = ImageDraw.Draw(img)
        d.line([(c - 0.45 * R, c + 0.1 * R), (c + 0.1 * R, c - 1.05 * R)], fill=(70, 120, 40, 255), width=max(3, lw))
        d.line([(c + 0.5 * R, c + 0.2 * R), (c + 0.1 * R, c - 1.05 * R)], fill=(70, 120, 40, 255), width=max(3, lw))
        leaf(img, c + 0.1 * R, c - 1.0 * R, R, -15, max(2, lw // 2), 0.3)
        shape(img, CHERRY, lw, lambda md: E(md, c + 0.5 * R, c + 0.5 * R, 0.55 * R, 0.55 * R))
        shape(img, CHERRY, lw, lambda md: E(md, c - 0.45 * R, c + 0.42 * R, 0.62 * R, 0.62 * R))
        draw_face(img, c - 0.45 * R, c + 0.45 * R, 0.55 * R, "happy")
        draw_face(img, c + 0.5 * R, c + 0.55 * R, 0.45 * R, "open")
    elif level == 2:  # fraise
        shape(img, STRAW, lw, lambda md: md.polygon(
            [(c + 0.95 * R * math.cos(math.radians(a)), c - 0.15 * R + 0.75 * R * math.sin(math.radians(a))) for a in range(180, 361, 10)]
            + [(c + 0.5 * R, c + 0.6 * R), (c, c + 1.05 * R), (c - 0.5 * R, c + 0.6 * R)], fill=255))
        d = ImageDraw.Draw(img)
        for (x, y) in ((-0.55, 0.0), (0.55, 0.0), (-0.3, 0.45), (0.3, 0.45), (0, 0.75), (-0.7, -0.35), (0.7, -0.35)):
            d.ellipse([c + x * R - 0.05 * R, c + y * R - 0.08 * R, c + x * R + 0.05 * R, c + y * R + 0.08 * R], fill=(255, 230, 120, 255))
        for ang in (-150, -110, -70, -30):
            leaf(img, c, c - 0.75 * R, R, ang, max(2, lw // 2), 0.25)
        draw_face(img, c, c + 0.05 * R, 0.6 * R, "happy")
    elif level == 3:  # citron
        shape(img, LEMON, lw, lambda md: (E(md, c, c, 1.0 * R, 0.78 * R),
                                           E(md, c - 1.0 * R, c, 0.14 * R, 0.12 * R), E(md, c + 1.0 * R, c, 0.14 * R, 0.12 * R)))
        leaf(img, c + 0.2 * R, c - 0.72 * R, R, -40, max(2, lw // 2), 0.3)
        draw_face(img, c, c + 0.05 * R, 0.7 * R, "open")
    elif level == 4:  # orange
        shape(img, ORANGE, lw, lambda md: E(md, c, c, 1.0 * R, 1.0 * R))
        d = ImageDraw.Draw(img)
        for (x, y) in ((-0.55, -0.5), (0.6, -0.45), (-0.7, 0.3), (0.7, 0.35), (0.1, -0.75)):
            d.ellipse([c + x * R - 0.04 * R, c + y * R - 0.04 * R, c + x * R + 0.04 * R, c + y * R + 0.04 * R], fill=(220, 100, 0, 255))
        leaf(img, c, c - 0.95 * R, R, -30, max(2, lw // 2), 0.35)
        ImageDraw.Draw(img).ellipse([c - 0.08 * R, c - 1.02 * R, c + 0.08 * R, c - 0.88 * R], fill=(90, 120, 40, 255))
        draw_face(img, c, c + 0.1 * R, 0.8 * R, "happy")
    elif level == 5:  # pomme verte
        d = ImageDraw.Draw(img)
        d.line([(c, c - 0.7 * R), (c + 0.12 * R, c - 1.15 * R)], fill=(110, 70, 30, 255), width=max(3, lw))
        leaf(img, c + 0.1 * R, c - 1.0 * R, R, -10, max(2, lw // 2), 0.35)
        shape(img, APPLE, lw, lambda md: (E(md, c - 0.42 * R, c, 0.62 * R, 0.85 * R), E(md, c + 0.42 * R, c, 0.62 * R, 0.85 * R),
                                           E(md, c, c + 0.15 * R, 0.8 * R, 0.75 * R)))
        d = ImageDraw.Draw(img)
        d.ellipse([c - 0.75 * R, c - 0.55 * R, c - 0.45 * R, c - 0.3 * R], fill=(255, 255, 255, 190))
        draw_face(img, c, c + 0.1 * R, 0.75 * R, "open")
    elif level == 6:  # ananas
        for ang, s in ((-90, 0.5), (-60, 0.42), (-120, 0.42), (-35, 0.33), (-145, 0.33)):
            leaf(img, c, c - 0.75 * R, R, ang, lw, s)
        m = shape(img, PINE, lw, lambda md: E(md, c, c + 0.15 * R, 0.78 * R, 0.95 * R))
        grid = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(grid)
        step = 0.3 * R
        for k in range(-7, 8):
            gd.line([(c + k * step - 1.2 * R, c - 1.2 * R), (c + k * step + 1.2 * R, c + 1.2 * R)], fill=(190, 120, 20, 255), width=max(2, lw // 2))
            gd.line([(c + k * step + 1.2 * R, c - 1.2 * R), (c + k * step - 1.2 * R, c + 1.2 * R)], fill=(190, 120, 20, 255), width=max(2, lw // 2))
        import numpy as np
        grid.putalpha(Image.fromarray(np.minimum(np.array(grid.getchannel("A")), np.array(m.filter(ImageFilter.MinFilter(9))))))
        img.alpha_composite(grid)
        shape(img, ((255, 250, 220), (255, 235, 160), (230, 190, 90)), max(2, lw // 2), lambda md: E(md, c, c + 0.2 * R, 0.5 * R, 0.38 * R))
        draw_face(img, c, c + 0.2 * R, 0.55 * R, "happy")
    elif level == 7:  # pastèque dorée : tranche, halo, couronne
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(16):
            a = k / 16 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.12), c + 0.5 * R * math.sin(a - 0.12)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.12), c + 0.5 * R * math.sin(a + 0.12))], fill=(255, 240, 130, 210) if k % 2 else (255, 170, 190, 210))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        mm = shape(img, MELON, lw, lambda md: E(md, c, c + 0.05 * R, 1.1 * R, 1.0 * R))
        st = Image.new("RGBA", img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        for k in range(-4, 5):
            sd.line([(c + k * 0.28 * R, c - 1.0 * R), (c + k * 0.28 * R, c + 1.1 * R)], fill=(25, 110, 40, 255), width=max(3, lw))
        import numpy as np
        st.putalpha(Image.fromarray(np.minimum(np.array(st.getchannel("A")), np.array(mm.filter(ImageFilter.MinFilter(9))))))
        img.alpha_composite(st)
        shape(img, GOLD, max(2, lw // 2), lambda md: E(md, c, c + 0.12 * R, 0.92 * R, 0.82 * R))
        shape(img, FLESH, max(2, lw // 2), lambda md: E(md, c, c + 0.15 * R, 0.8 * R, 0.7 * R))
        d = ImageDraw.Draw(img)
        for (x, y) in ((-0.5, -0.2), (0.5, -0.2), (-0.55, 0.35), (0.55, 0.35), (-0.2, 0.6), (0.2, 0.6)):
            d.ellipse([c + x * R - 0.04 * R, c + y * R - 0.07 * R, c + x * R + 0.04 * R, c + y * R + 0.07 * R], fill=(40, 20, 20, 255))
        draw_face(img, c, c + 0.15 * R, 0.62 * R, "open")
        shape(img, GOLD, max(2, lw // 2), lambda md: md.polygon([(c - 0.4 * R, c - 0.85 * R), (c - 0.4 * R, c - 1.3 * R), (c - 0.2 * R, c - 1.08 * R), (c, c - 1.42 * R),
                                                                 (c + 0.2 * R, c - 1.08 * R), (c + 0.4 * R, c - 1.3 * R), (c + 0.4 * R, c - 0.85 * R)], fill=255))
        for (sx, sy, ss) in ((-1.2, -0.9, 0.14), (1.2, -0.85, 0.12), (1.3, 0.95, 0.11), (-1.3, 0.8, 0.1)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """UN MIXEUR ! : blender gris avec lame, l'air malicieux."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    d = ImageDraw.Draw(img)
    for k in range(3):
        y = c - 0.6 * R + k * 0.5 * R
        d.line([(c + 0.9 * R, y), (c + 1.5 * R, y - 0.4 * R)], fill=(255, 255, 255, 230), width=int(0.08 * R))
    shape(img, GLASS, lw, lambda md: md.polygon([(c - 0.75 * R, c - 0.95 * R), (c + 0.75 * R, c - 0.95 * R), (c + 0.5 * R, c + 0.45 * R), (c - 0.5 * R, c + 0.45 * R)], fill=255))
    shape(img, STEEL, lw, lambda md: md.rounded_rectangle([c - 0.82 * R, c - 1.15 * R, c + 0.82 * R, c - 0.9 * R], 0.08 * R, fill=255))
    shape(img, ((255, 170, 170), (230, 60, 70), (150, 20, 30)), lw, lambda md: md.rounded_rectangle([c - 0.75 * R, c + 0.4 * R, c + 0.75 * R, c + 1.05 * R], 0.15 * R, fill=255))
    d = ImageDraw.Draw(img)
    d.ellipse([c - 0.12 * R, c + 0.6 * R, c + 0.12 * R, c + 0.84 * R], fill=(255, 255, 255, 255), outline=OUT, width=max(2, lw // 2))
    d.line([(c - 0.35 * R, c + 0.25 * R), (c + 0.35 * R, c + 0.15 * R)], fill=(120, 130, 150, 255), width=max(3, lw))
    cx, cy = c, c - 0.4 * R
    for sx in (-1, 1):
        x = cx + sx * 0.25 * R
        d.ellipse([x - 0.13 * R, cy - 0.08 * R, x + 0.13 * R, cy + 0.18 * R], fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=max(2, lw // 2))
        d.ellipse([x - 0.06 * R, cy + 0.0 * R, x + 0.06 * R, cy + 0.13 * R], fill=(10, 10, 10, 255))
        d.line([(x - sx * 0.18 * R, cy - 0.26 * R), (x + sx * 0.13 * R, cy - 0.12 * R)], fill=(20, 20, 20, 255), width=int(0.07 * R))
    d.arc([cx - 0.22 * R, cy + 0.15 * R, cx + 0.22 * R, cy + 0.45 * R], 20, 160, fill=(20, 20, 20, 255), width=int(0.06 * R))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(80, 50, 10, 255), glow=(255, 255, 255)):
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
    sheet = Image.new("RGBA", (W, H), (255, 225, 95, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
