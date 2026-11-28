"""HIVER MERGE (épisode 20) : flocon → yéti royal + UN RADIATEUR ! (rebondissement).
Tous les personnages sont inventés."""
import math
from PIL import Image, ImageDraw, ImageFilter
from sprites_base import gradient_fill, draw_face, star

SS = 3
LEVELS = [
    ("FLOCON",            "Flocon",            24),
    ("GLAÇON",            "Glaçon",            36),
    ("BOULE DE NEIGE",    "Boule de neige",    50),
    ("BONHOMME DE NEIGE", "Bonhomme de neige", 64),
    ("PINGOUIN",          "Pingouin",          80),
    ("IGLOO",             "Igloo",             98),
    ("OURS POLAIRE",      "Ours polaire",     120),
    ("YÉTI ROYAL",        "Yéti royal",       150),
]
BOMB_R = 48
OUT = (30, 45, 85, 255)

ICE = ((235, 250, 255), (150, 215, 250), (70, 140, 215))
CYAN = ((225, 255, 255), (120, 225, 240), (40, 150, 190))
SNOW = ((255, 255, 255), (235, 242, 252), (175, 195, 225))
CARROT = ((255, 215, 160), (255, 140, 40), (200, 80, 10))
BLACK = ((120, 130, 160), (50, 55, 80), (20, 22, 35))
YEL = ((255, 250, 200), (255, 205, 55), (215, 140, 0))
RED = ((255, 205, 195), (240, 75, 70), (160, 30, 35))
GREEN = ((215, 255, 200), (110, 205, 90), (40, 130, 45))
FUR = ((255, 255, 255), (238, 240, 250), (190, 200, 225))
YETI = ((235, 245, 255), (175, 205, 245), (95, 130, 205))
PURP = ((240, 215, 255), (190, 120, 245), (110, 50, 190))
GOLDC = ((255, 250, 200), (255, 205, 55), (210, 130, 0))
GREY = ((240, 245, 255), (170, 180, 200), (100, 110, 135))
HOT = ((255, 225, 200), (250, 120, 70), (190, 50, 30))


def shape(img, cols, lw, draw):
    m = Image.new("L", img.size, 0)
    draw(ImageDraw.Draw(m))
    img.alpha_composite(gradient_fill(img.size, m, *cols))
    if lw == 0:
        return m
    edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(max(3, (lw // 2) * 2 + 1)))
    img.alpha_composite(Image.composite(Image.new("RGBA", img.size, OUT), Image.new("RGBA", img.size, (0, 0, 0, 0)), edge))
    return m


def E(md, x, y, rx, ry):
    md.ellipse([x - rx, y - ry, x + rx, y + ry], fill=255)


def RR(md, x0, y0, x1, y1, r):
    md.rounded_rectangle([x0, y0, x1, y1], r, fill=255)


def snowflake_arms(img, c, cy, R, lw, col=(255, 255, 255, 255)):
    d = ImageDraw.Draw(img)
    for k in range(6):
        a = k / 6 * 6.283 - 1.5708
        x1, y1 = c + R * math.cos(a), cy + R * math.sin(a)
        d.line([(c, cy), (x1, y1)], fill=OUT, width=int(lw * 3.6))
    for k in range(6):
        a = k / 6 * 6.283 - 1.5708
        x1, y1 = c + R * math.cos(a), cy + R * math.sin(a)
        d.line([(c, cy), (x1, y1)], fill=col, width=int(lw * 2.0))
        for t, s in ((0.62, 0.28),):
            xm, ym = c + t * R * math.cos(a), cy + t * R * math.sin(a)
            for da in (-0.8, 0.8):
                d.line([(xm, ym), (xm + s * R * math.cos(a + da), ym + s * R * math.sin(a + da))], fill=col, width=int(lw * 1.6))


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.7 if level >= 4 else 1.6
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    if level == 0:  # flocon : étoile à 6 branches + cœur bleu
        snowflake_arms(img, c, c, 1.0 * R, lw, (190, 230, 255, 255))
        shape(img, ICE, lw, lambda md: E(md, c, c, 0.55 * R, 0.55 * R))
        draw_face(img, c, c + 0.03 * R, 0.45 * R, "happy")
    elif level == 1:  # glaçon : cube translucide
        shape(img, CYAN, lw, lambda md: RR(md, c - 0.82 * R, c - 0.82 * R, c + 0.82 * R, c + 0.82 * R, 0.25 * R))
        d = ImageDraw.Draw(img)
        d.line([(c - 0.55 * R, c - 0.5 * R), (c - 0.2 * R, c - 0.62 * R)], fill=(255, 255, 255, 255), width=max(2, lw))
        d.line([(c - 0.6 * R, c - 0.25 * R), (c - 0.6 * R, c + 0.05 * R)], fill=(255, 255, 255, 255), width=max(2, lw))
        draw_face(img, c, c + 0.1 * R, 0.6 * R, "happy")
    elif level == 2:  # boule de neige
        shape(img, SNOW, lw, lambda md: E(md, c, c, 0.95 * R, 0.92 * R))
        d = ImageDraw.Draw(img)
        for (x, y, s) in ((-0.5, -0.5, 0.08), (0.55, -0.4, 0.06), (0.6, 0.45, 0.07), (-0.6, 0.4, 0.05)):
            d.ellipse([c + (x - s) * R, c + (y - s) * R, c + (x + s) * R, c + (y + s) * R], fill=(200, 215, 240, 255))
        draw_face(img, c, c + 0.05 * R, 0.62 * R, "open")
    elif level == 3:  # bonhomme de neige : 2 boules, chapeau, carotte, écharpe
        shape(img, SNOW, lw, lambda md: E(md, c, c + 0.5 * R, 0.78 * R, 0.6 * R))
        shape(img, SNOW, lw, lambda md: E(md, c, c - 0.25 * R, 0.6 * R, 0.55 * R))
        shape(img, RED, lw, lambda md: RR(md, c - 0.62 * R, c + 0.14 * R, c + 0.62 * R, c + 0.34 * R, 0.1 * R))
        shape(img, RED, lw, lambda md: RR(md, c + 0.2 * R, c + 0.2 * R, c + 0.45 * R, c + 0.75 * R, 0.08 * R))
        shape(img, BLACK, lw, lambda md: RR(md, c - 0.55 * R, c - 0.82 * R, c + 0.55 * R, c - 0.68 * R, 0.05 * R))
        shape(img, BLACK, lw, lambda md: RR(md, c - 0.35 * R, c - 1.2 * R, c + 0.35 * R, c - 0.75 * R, 0.06 * R))
        draw_face(img, c, c - 0.3 * R, 0.5 * R, "happy")
        shape(img, CARROT, max(2, lw // 2), lambda md: md.polygon([(c - 0.02 * R, c - 0.27 * R), (c + 0.4 * R, c - 0.2 * R), (c - 0.02 * R, c - 0.13 * R)], fill=255))
    elif level == 4:  # pingouin : corps noir, ventre blanc, bec et pattes jaunes
        for sx in (-1, 1):
            shape(img, YEL, lw, lambda md: E(md, c + sx * 0.32 * R, c + 0.95 * R, 0.28 * R, 0.13 * R))
            shape(img, BLACK, lw, lambda md: E(md, c + sx * 0.78 * R, c + 0.15 * R, 0.2 * R, 0.45 * R))
        shape(img, BLACK, lw, lambda md: E(md, c, c + 0.05 * R, 0.75 * R, 0.92 * R))
        shape(img, SNOW, 0, lambda md: E(md, c, c + 0.2 * R, 0.52 * R, 0.68 * R))
        shape(img, SNOW, 0, lambda md: E(md, c, c - 0.35 * R, 0.5 * R, 0.35 * R))
        draw_face(img, c, c - 0.3 * R, 0.5 * R, "happy")
        shape(img, YEL, max(2, lw // 2), lambda md: md.polygon([(c - 0.13 * R, c - 0.18 * R), (c + 0.13 * R, c - 0.18 * R), (c, c - 0.02 * R)], fill=255))
    elif level == 5:  # igloo : dôme de blocs, porte sombre
        shape(img, SNOW, lw, lambda md: md.chord([c - 1.0 * R, c - 0.95 * R, c + 1.0 * R, c + 1.05 * R], 180, 360, fill=255))
        shape(img, SNOW, lw, lambda md: RR(md, c - 1.0 * R, c - 0.02 * R, c + 1.0 * R, c + 0.7 * R, 0.08 * R))
        d = ImageDraw.Draw(img)
        bl = (150, 180, 220, 255)
        for y in (-0.55, -0.2, 0.15, 0.45):
            w = math.sqrt(max(0, 1 - ((y + 0.0) / 1.0) ** 2)) if y < 0 else 1.0
            d.line([(c - 0.95 * w * R, c + y * R), (c + 0.95 * w * R, c + y * R)], fill=bl, width=max(2, lw // 2))
        shape(img, BLACK, lw, lambda md: md.chord([c + 0.3 * R, c + 0.1 * R, c + 0.85 * R, c + 1.25 * R], 180, 360, fill=255))
        shape(img, BLACK, 0, lambda md: RR(md, c + 0.3 * R, c + 0.6 * R, c + 0.85 * R, c + 0.7 * R, 0.01 * R))
        draw_face(img, c - 0.3 * R, c - 0.3 * R, 0.55 * R, "happy")
    elif level == 6:  # ours polaire : tête ronde, oreilles, museau
        for sx in (-1, 1):
            shape(img, FUR, lw, lambda md: E(md, c + sx * 0.68 * R, c - 0.72 * R, 0.27 * R, 0.27 * R))
            shape(img, ((255, 220, 230), (250, 170, 190), (210, 110, 140)), 0, lambda md: E(md, c + sx * 0.68 * R, c - 0.72 * R, 0.13 * R, 0.13 * R))
        shape(img, FUR, lw, lambda md: E(md, c, c, 0.98 * R, 0.9 * R))
        draw_face(img, c, c - 0.2 * R, 0.62 * R, "happy")
        shape(img, SNOW, lw, lambda md: E(md, c, c + 0.32 * R, 0.36 * R, 0.25 * R))
        shape(img, BLACK, max(2, lw // 2), lambda md: E(md, c, c + 0.22 * R, 0.13 * R, 0.08 * R))
        shape(img, ((210, 240, 255), (110, 180, 240), (50, 110, 190)), lw, lambda md: RR(md, c - 0.75 * R, c + 0.68 * R, c + 0.75 * R, c + 0.88 * R, 0.1 * R))
    elif level == 7:  # yéti royal : grosse boule de poils bleutée, couronne, cape violette
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(18):
            a = k / 18 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.11), c + 0.5 * R * math.sin(a - 0.11)), (c + 1.5 * R * math.cos(a), c + 1.5 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.11), c + 0.5 * R * math.sin(a + 0.11))], fill=(255, 240, 120, 190) if k % 2 else (170, 220, 255, 200))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        shape(img, PURP, lw, lambda md: md.polygon([(c - 0.6 * R, c - 0.1 * R), (c + 0.6 * R, c - 0.1 * R), (c + 1.05 * R, c + 1.0 * R), (c - 1.05 * R, c + 1.0 * R)], fill=255))
        def furball(md):
            n = 26
            pts = []
            for k in range(n * 2):
                a = k / (n * 2) * 6.283
                rr = (0.9 if k % 2 == 0 else 0.78) * R
                pts.append((c + rr * math.cos(a), c - 0.05 * R + rr * 0.95 * math.sin(a)))
            md.polygon(pts, fill=255)
        shape(img, YETI, lw, furball)
        shape(img, ((235, 245, 255), (200, 220, 250), (150, 175, 225)), 0, lambda md: E(md, c, c, 0.55 * R, 0.5 * R))
        draw_face(img, c, c - 0.02 * R, 0.6 * R, "open")
        shape(img, GOLDC, lw, lambda md: md.polygon(
            [(c - 0.4 * R, c - 0.75 * R), (c - 0.45 * R, c - 1.2 * R), (c - 0.2 * R, c - 0.98 * R), (c, c - 1.3 * R),
             (c + 0.2 * R, c - 0.98 * R), (c + 0.45 * R, c - 1.2 * R), (c + 0.4 * R, c - 0.75 * R)], fill=255))
        shape(img, ICE, max(2, lw // 2), lambda md: E(md, c, c - 0.9 * R, 0.08 * R, 0.08 * R))
        for (sx, sy, ss) in ((-1.2, -0.9, 0.16), (1.2, -0.85, 0.14), (1.25, 0.6, 0.12), (-1.25, 0.55, 0.11)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
            star(img, c + sx * R, c + sy * R, ss * 0.55 * R, (90, 170, 255, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """UN RADIATEUR ! : radiateur rouge brûlant à ailettes, avec des yeux et des vapeurs."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    d = ImageDraw.Draw(img)
    for k, x in enumerate((-0.5, 0, 0.5)):
        pts = [(c + x * R + 0.12 * R * math.sin(t / 3), c - 0.95 * R - t * 0.07 * R) for t in range(8)]
        d.line(pts, fill=(255, 255, 255, 230), width=int(0.08 * R))
    for sx in (-1, 1):
        shape(img, GREY, lw, lambda md: RR(md, c + sx * 0.6 * R - 0.12 * R, c + 0.75 * R, c + sx * 0.6 * R + 0.12 * R, c + 1.05 * R, 0.04 * R))
    for x in (-0.75, -0.375, 0, 0.375, 0.75):
        shape(img, HOT, lw, lambda md: RR(md, c + (x - 0.19) * R, c - 0.85 * R, c + (x + 0.19) * R, c + 0.85 * R, 0.16 * R))
    shape(img, HOT, lw, lambda md: RR(md, c - 0.95 * R, c - 0.3 * R, c + 0.95 * R, c + 0.3 * R, 0.1 * R))
    shape(img, GREY, lw, lambda md: E(md, c + 1.05 * R, c + 0.55 * R, 0.13 * R, 0.13 * R))
    draw_face(img, c, c - 0.05 * R, 0.65 * R, "sweat")
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(40, 80, 150, 255), glow=(255, 255, 255)):
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
    sheet = Image.new("RGBA", (W, H), (255, 195, 165, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
