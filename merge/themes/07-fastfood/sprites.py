"""FAST-FOOD MERGE (épisode 7) : frite → burger cosmique + BROCOLI (rebondissement)."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from sprites_base import gradient_fill, draw_body, draw_face, star, blob_points

SS = 3
LEVELS = [
    ("FRITE",             "Frite",             24),
    ("CORNET DE FRITES",  "Cornet de frites",  36),
    ("BURGER",            "Burger",            50),
    ("DOUBLE BURGER",     "Double burger",     64),
    ("MENU XXL",          "Menu XXL",          80),
    ("CAMION À BURGERS",  "Camion à burgers",  98),
    ("RESTAURANT",        "Restaurant",       120),
    ("BURGER COSMIQUE",   "Burger cosmique",  150),
]
BOMB_R = 46
OUT = (70, 35, 15, 255)

BUN = ((255, 225, 150), (240, 165, 60), (180, 95, 25))
FRY = ((255, 245, 160), (255, 205, 60), (215, 145, 20))


def poly_body(img, pts, cols, outline=OUT, lw=None):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    img.alpha_composite(gradient_fill(img.size, m, *cols))
    xs = [p[0] for p in pts]
    w = lw or max(2, int((max(xs) - min(xs)) * 0.04))
    ImageDraw.Draw(img).line(pts + [pts[0]], fill=outline, width=w, joint="curve")
    return m


def rrect(img, box, rad, cols, outline=OUT, lw=6):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle(box, rad, fill=255)
    img.alpha_composite(gradient_fill(img.size, m, *cols))
    ImageDraw.Draw(img).rounded_rectangle(box, rad, outline=outline, width=lw)
    return m


def fries(img, cx, top, bottom, width, n, seed, lw):
    rnd = random.Random(seed)
    d = ImageDraw.Draw(img)
    fw = width / n * 1.15
    for k in range(n):
        x = cx - width / 2 + (k + 0.5) * width / n + rnd.uniform(-0.1, 0.1) * fw
        t = top + rnd.uniform(0, 0.25) * (bottom - top)
        ang = rnd.uniform(-8, 8)
        f = Image.new("RGBA", img.size, (0, 0, 0, 0))
        rrect(f, [x - fw / 2, t, x + fw / 2, bottom], fw * 0.25, FRY, OUT, lw)
        img.alpha_composite(f.rotate(ang, resample=Image.BICUBIC, center=(x, bottom)))


def burger(img, c, cy, R, layers=1, face=True, seed=0):
    """Burger centré : pain haut, salade, steak(s), fromage, pain bas."""
    lw = max(2, int(0.06 * R))
    W = 1.0 * R
    h_total = 1.7 * R
    top = cy - h_total / 2
    # pain bas
    rrect(img, [c - W * 0.95, cy + 0.45 * R, c + W * 0.95, cy + 0.85 * R], 0.18 * R, BUN, OUT, lw)
    y = cy + 0.45 * R
    for i in range(layers):
        th = 0.28 * R / max(1, layers * 0.7)
        rrect(img, [c - W * 1.0, y - th, c + W * 1.0, y + 0.02 * R], th * 0.5, ((150, 90, 60), (110, 60, 35), (70, 35, 20)), OUT, lw)
        y -= th
        # fromage
        ch = [(c - W * 1.02, y - 0.02 * R), (c + W * 1.02, y - 0.02 * R), (c + W * 0.95, y + 0.06 * R), (c + W * 0.55, y + 0.22 * R),
              (c + W * 0.35, y + 0.05 * R), (c - W * 0.2, y + 0.06 * R), (c - W * 0.4, y + 0.24 * R), (c - W * 0.6, y + 0.05 * R), (c - W * 0.95, y + 0.06 * R)]
        poly_body(img, ch, ((255, 240, 120), (255, 200, 30), (230, 150, 0)), OUT, max(2, lw // 2))
        y -= 0.04 * R
    # salade
    pts = []
    for k in range(25):
        x = c - W * 1.08 + k * (2.16 * W / 24)
        pts.append((x, y - 0.03 * R + (0.07 * R if k % 2 else 0)))
    pts += [(c + W * 1.0, y - 0.13 * R), (c - W * 1.0, y - 0.13 * R)]
    poly_body(img, pts, ((180, 255, 120), (90, 210, 60), (40, 140, 30)), OUT, max(2, lw // 2))
    # tomate
    rrect(img, [c - W * 0.85, y - 0.24 * R, c + W * 0.85, y - 0.1 * R], 0.07 * R, ((255, 140, 120), (240, 60, 50), (170, 30, 30)), OUT, max(2, lw // 2))
    # pain haut (dôme)
    yb = y - 0.18 * R
    m = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(m)
    md.pieslice([c - W * 1.0, yb - 0.95 * R, c + W * 1.0, yb + 0.25 * R], 180, 360, fill=255)
    md.rectangle([c - W * 1.0, yb - 0.36 * R, c + W * 1.0, yb + 0.02 * R], fill=0)
    md.rounded_rectangle([c - W * 1.0, yb - 0.4 * R, c + W * 1.0, yb + 0.04 * R], 0.15 * R, fill=255)
    img.alpha_composite(gradient_fill(img.size, m, *BUN))
    edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(max(3, (lw // 2) * 2 + 1)))
    img.alpha_composite(Image.composite(Image.new("RGBA", img.size, OUT), Image.new("RGBA", img.size, (0, 0, 0, 0)), edge))
    d = ImageDraw.Draw(img)
    rnd = random.Random(seed + 3)
    for _ in range(9):  # sésame
        x = c + rnd.uniform(-0.75, 0.75) * W; yy = yb - rnd.uniform(0.45, 0.8) * R
        if ((x - c) / W) ** 2 + ((yy - (yb - 0.35 * R)) / (0.6 * R)) ** 2 > 0.85:
            continue
        d.ellipse([x - 0.05 * R, yy - 0.025 * R, x + 0.05 * R, yy + 0.025 * R], fill=(255, 250, 225, 255))
    if face:
        draw_face(img, c, yb - 0.22 * R, 0.6 * R, "happy")


def make_sprite(level):
    _, _, r = LEVELS[level]
    margin = 1.65 if level >= 4 else 1.45
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    lw = max(3, int(0.07 * R))
    if level == 0:  # frite
        f = Image.new("RGBA", img.size, (0, 0, 0, 0))
        rrect(f, [c - 0.6 * R, c - 1.1 * R, c + 0.6 * R, c + 1.1 * R], 0.2 * R, FRY, OUT, lw)
        draw_face(f, c, c - 0.1 * R, 0.85 * R, "happy")
        img.alpha_composite(f.rotate(-12, resample=Image.BICUBIC, center=(c, c)))
    elif level == 1:  # cornet de frites
        fries(img, c, c - 1.1 * R, c + 0.1 * R, 1.4 * R, 6, 2, max(2, lw // 2))
        pts = [(c - 0.95 * R, c - 0.2 * R), (c + 0.95 * R, c - 0.2 * R), (c + 0.7 * R, c + 1.0 * R), (c - 0.7 * R, c + 1.0 * R)]
        poly_body(img, pts, ((255, 120, 120), (230, 40, 40), (160, 20, 20)), OUT, lw)
        draw_face(img, c, c + 0.35 * R, 0.6 * R, "open")
    elif level == 2:
        burger(img, c, c, R, 1, seed=2)
    elif level == 3:
        burger(img, c, c, R, 2, seed=3)
        star(img, c + 0.95 * R, c - 0.85 * R, 0.14 * R, (255, 255, 255, 255))
    elif level == 4:  # menu XXL : plateau avec burger, frites, soda
        rrect(img, [c - 1.2 * R, c + 0.55 * R, c + 1.2 * R, c + 0.85 * R], 0.12 * R, ((255, 150, 150), (230, 60, 60), (160, 30, 30)), OUT, lw)
        # soda
        cup = [(c + 0.35 * R, c - 0.7 * R), (c + 1.1 * R, c - 0.7 * R), (c + 1.0 * R, c + 0.6 * R), (c + 0.45 * R, c + 0.6 * R)]
        ImageDraw.Draw(img).line([(c + 0.85 * R, c - 0.7 * R), (c + 1.0 * R, c - 1.25 * R)], fill=(255, 255, 255, 255), width=int(0.08 * R))
        ImageDraw.Draw(img).line([(c + 0.85 * R, c - 0.7 * R), (c + 1.0 * R, c - 1.25 * R)], fill=(230, 50, 120, 255), width=int(0.04 * R))
        poly_body(img, cup, ((150, 220, 255), (40, 150, 240), (20, 80, 170)), OUT, lw)
        rrect(img, [c + 0.3 * R, c - 0.8 * R, c + 1.15 * R, c - 0.66 * R], 0.05 * R, ((255, 255, 255), (230, 230, 240), (180, 180, 200)), OUT, max(2, lw // 2))
        # frites
        fries(img, c - 0.85 * R, c - 0.75 * R, c, 0.6 * R, 4, 5, max(2, lw // 3))
        poly_body(img, [(c - 1.2 * R, c - 0.1 * R), (c - 0.5 * R, c - 0.1 * R), (c - 0.6 * R, c + 0.6 * R), (c - 1.1 * R, c + 0.6 * R)],
                  ((255, 120, 120), (230, 40, 40), (160, 20, 20)), OUT, lw)
        burger(img, c - 0.05 * R, c + 0.08 * R, 0.55 * R, 1, face=True, seed=4)
        d = ImageDraw.Draw(img)
        from PIL import ImageFont
        try:
            fnt = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", int(0.32 * R))
            d.text((c, c - 1.2 * R), "XXL", font=fnt, fill=(255, 220, 0, 255), anchor="mm", stroke_width=int(0.05 * R), stroke_fill=OUT)
        except Exception:
            pass
    elif level == 5:  # camion à burgers
        # roues
        d = ImageDraw.Draw(img)
        body = rrect(img, [c - 1.25 * R, c - 0.65 * R, c + 1.25 * R, c + 0.55 * R], 0.18 * R, ((255, 200, 220), (255, 110, 170), (200, 50, 120)), OUT, lw)
        # toit avec burger géant
        burger(img, c, c - 0.95 * R, 0.42 * R, 1, face=False, seed=5)
        # fenêtre de service
        rrect(img, [c - 0.95 * R, c - 0.45 * R, c + 0.2 * R, c + 0.05 * R], 0.08 * R, ((255, 255, 230), (255, 245, 190), (230, 210, 140)), OUT, max(2, lw // 2))
        d = ImageDraw.Draw(img)
        for k in range(6):  # store rayé
            x0 = c - 1.0 * R + k * 0.21 * R
            d.rectangle([x0, c - 0.6 * R, x0 + 0.21 * R, c - 0.47 * R], fill=(255, 255, 255, 255) if k % 2 else (255, 60, 60, 255))
        draw_face(img, c - 0.38 * R, c - 0.18 * R, 0.5 * R, "open")
        # cabine
        rrect(img, [c + 0.35 * R, c - 0.45 * R, c + 1.05 * R, c - 0.05 * R], 0.08 * R, ((210, 240, 255), (150, 210, 250), (90, 150, 210)), OUT, max(2, lw // 2))
        d = ImageDraw.Draw(img)
        for x in (c - 0.7 * R, c + 0.75 * R):
            d.ellipse([x - 0.3 * R, c + 0.3 * R, x + 0.3 * R, c + 0.9 * R], fill=(50, 45, 55, 255), outline=OUT, width=lw)
            d.ellipse([x - 0.12 * R, c + 0.48 * R, x + 0.12 * R, c + 0.72 * R], fill=(200, 200, 210, 255))
    elif level == 6:  # restaurant
        rrect(img, [c - 1.1 * R, c - 0.45 * R, c + 1.1 * R, c + 1.0 * R], 0.1 * R, ((255, 250, 235), (250, 230, 200), (210, 180, 140)), OUT, lw)
        d = ImageDraw.Draw(img)
        for k in range(8):  # auvent
            x0 = c - 1.25 * R + k * 2.5 * R / 8
            d.pieslice([x0, c - 0.75 * R, x0 + 2.5 * R / 8, c - 0.35 * R], 0, 180, fill=(255, 60, 60, 255) if k % 2 == 0 else (255, 255, 255, 255), outline=OUT, width=max(2, lw // 2))
            d.rectangle([x0, c - 0.75 * R, x0 + 2.5 * R / 8, c - 0.55 * R], fill=(255, 60, 60, 255) if k % 2 == 0 else (255, 255, 255, 255))
        d.line([(c - 1.25 * R, c - 0.75 * R), (c + 1.25 * R, c - 0.75 * R)], fill=OUT, width=lw)
        # enseigne : grand burger
        burger(img, c, c - 1.05 * R, 0.33 * R, 1, face=False, seed=6)
        # porte
        rrect(img, [c - 0.25 * R, c + 0.35 * R, c + 0.25 * R, c + 1.0 * R], 0.08 * R, ((150, 220, 255), (80, 170, 240), (30, 100, 180)), OUT, max(2, lw // 2))
        # visage sur la façade
        draw_face(img, c, c - 0.02 * R, 0.75 * R, "happy")
        for x in (c - 0.8 * R, c + 0.8 * R):
            rrect(img, [x - 0.2 * R, c + 0.4 * R, x + 0.2 * R, c + 0.75 * R], 0.05 * R, ((220, 245, 255), (160, 215, 250), (90, 150, 210)), OUT, max(2, lw // 2))
    elif level == 7:  # burger cosmique
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(16):
            a = k / 16 * 6.283
            gd.polygon([(c + 0.5 * R * math.cos(a - 0.12), c + 0.5 * R * math.sin(a - 0.12)), (c + 1.45 * R * math.cos(a), c + 1.45 * R * math.sin(a)),
                        (c + 0.5 * R * math.cos(a + 0.12), c + 0.5 * R * math.sin(a + 0.12))], fill=(255, 210, 60, 200) if k % 2 else (190, 110, 255, 200))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(R * 0.03)))
        burger(img, c, c, 1.0 * R, 2, face=False, seed=7)
        # couronne
        cr = [(c - 0.45 * R, c - 1.0 * R), (c - 0.5 * R, c - 1.4 * R), (c - 0.25 * R, c - 1.18 * R), (c, c - 1.5 * R),
              (c + 0.25 * R, c - 1.18 * R), (c + 0.5 * R, c - 1.4 * R), (c + 0.45 * R, c - 1.0 * R)]
        poly_body(img, cr, ((255, 250, 180), (255, 210, 40), (210, 140, 0)), OUT, lw)
        draw_face(img, c, c - 0.4 * R, 0.62 * R, "open")
        for (sx, sy, ss) in ((-1.25, -0.9, 0.14), (1.2, -1.0, 0.12), (1.25, 0.85, 0.11), (-1.2, 0.95, 0.1)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 255, 255, 255))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def make_bomb():
    """Le BROCOLI : petit arbre vert aux sourcils froncés, très sérieux sur le régime."""
    R = BOMB_R * SS
    side = int(2 * BOMB_R * 1.8) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    lw = max(3, int(0.06 * R))
    # tige
    stem = [(c - 0.3 * R, c + 0.1 * R), (c + 0.3 * R, c + 0.1 * R), (c + 0.22 * R, c + 1.1 * R), (c - 0.22 * R, c + 1.1 * R)]
    poly_body(img, stem, ((210, 255, 170), (140, 210, 90), (80, 150, 50)), (25, 70, 20, 255), lw)
    # bouquet de boules
    m = Image.new("L", img.size, 0); md = ImageDraw.Draw(m)
    for (x, y, rr) in ((-0.6, -0.1, 0.45), (0.6, -0.1, 0.45), (0, -0.55, 0.55), (-0.35, -0.75, 0.4), (0.38, -0.75, 0.4), (0, -0.05, 0.45)):
        md.ellipse([c + (x - rr) * R, c + (y - rr) * R, c + (x + rr) * R, c + (y + rr) * R], fill=255)
    img.alpha_composite(gradient_fill(img.size, m, (150, 230, 110), (60, 170, 50), (20, 100, 30)))
    edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(lw | 1))
    img.alpha_composite(Image.composite(Image.new("RGBA", img.size, (25, 70, 20, 255)), Image.new("RGBA", img.size, (0, 0, 0, 0)), edge))
    tex = Image.new("RGBA", img.size, (0, 0, 0, 0)); td = ImageDraw.Draw(tex)
    rnd = random.Random(11)
    for _ in range(60):
        x = c + rnd.uniform(-1, 1) * R; y = c + rnd.uniform(-1.2, 0.3) * R; rr = rnd.uniform(0.04, 0.09) * R
        td.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(30, 110, 30, 110))
    tex.putalpha(ImageChops.multiply(tex.getchannel("A"), m))
    img.alpha_composite(tex)
    d = ImageDraw.Draw(img)
    cy = c - 0.3 * R
    for sx in (-1, 1):
        x = c + sx * 0.25 * R
        d.ellipse([x - 0.13 * R, cy - 0.1 * R, x + 0.13 * R, cy + 0.16 * R], fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=max(2, lw // 2))
        d.ellipse([x - 0.06 * R, cy - 0.0 * R, x + 0.06 * R, cy + 0.12 * R], fill=(10, 10, 10, 255))
        d.line([(x - sx * 0.18 * R, cy - 0.28 * R), (x + sx * 0.14 * R, cy - 0.14 * R)], fill=(20, 40, 10, 255), width=int(0.07 * R))
    d.arc([c - 0.16 * R, cy + 0.22 * R, c + 0.16 * R, cy + 0.42 * R], 200, 340, fill=(20, 40, 10, 255), width=int(0.05 * R))
    return img.resize((side // SS, side // SS), Image.LANCZOS)


def silhouette(img, col=(60, 30, 10, 255), glow=(255, 255, 255)):
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
    sheet = Image.new("RGBA", (W, H), (255, 205, 90, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2)); x += s.width + 40
    sheet.convert("RGB").save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"))
