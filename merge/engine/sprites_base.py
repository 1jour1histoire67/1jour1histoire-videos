"""Personnages kawaii dessinés en code pour NUGGET MERGE."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

SS = 3  # suréchantillonnage

LEVELS = [
    # nom affiché, texte de la voix (orthographe phonétique), rayon physique (px)
    ("MIETTE",            "Miette",              24),
    ("NUGGET",            "Neuguette",           36),
    ("NUGGET SAUCE",      "Neuguette sauce",     50),
    ("NUGGET ÉPICÉ",      "Neuguette épicé",     64),
    ("BOÎTE DE NUGGETS",  "Boîte de neuguettes", 80),
    ("ROI NUGGET",        "Roi neuguette",       98),
    ("PLANÈTE NUGGET",    "Planète neuguette",  120),
    ("UNIVERS NUGGET",    "Univers neuguette",  150),
]


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def blob_points(cx, cy, rx, ry, seed, wobble=0.06, n=90, squish=0.0):
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(4)]
    amp = [wobble * rnd.uniform(0.4, 1.0) for _ in range(4)]
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 1.0
        for k in range(4):
            r += amp[k] * math.sin((k + 2) * a + ph[k]) / (k + 1)
        # base légèrement aplatie
        yy = math.sin(a)
        if yy > 0:
            r *= 1 - squish * yy ** 4
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return pts


def gradient_fill(size, mask, c_light, c_mid, c_dark, light_pos=(0.32, 0.28)):
    """Remplissage radial (lumière en haut à gauche) découpé par le masque."""
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    lx, ly = light_pos[0] * w, light_pos[1] * h
    d = np.sqrt((xx - lx) ** 2 + (yy - ly) ** 2) / (0.95 * max(w, h))
    d = np.clip(d, 0, 1)
    cl, cm, cd = [np.array(c, np.float32) for c in (c_light, c_mid, c_dark)]
    t1 = np.clip(d / 0.5, 0, 1)[..., None]
    t2 = np.clip((d - 0.5) / 0.5, 0, 1)[..., None]
    col = np.where(d[..., None] < 0.5, cl + (cm - cl) * t1, cm + (cd - cm) * t2)
    arr = np.dstack([col, np.array(mask, np.float32)]).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def draw_body(img, pts, seed, c_light, c_mid, c_dark, outline, crumbs=True):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    body = gradient_fill((w, h), mask, c_light, c_mid, c_dark)
    img.alpha_composite(body)
    d = ImageDraw.Draw(img)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    bw = max(xs) - min(xs)
    if crumbs:  # chapelure
        rnd = random.Random(seed + 7)
        tex = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        td = ImageDraw.Draw(tex)
        for _ in range(int(bw * 0.9)):
            x = rnd.uniform(min(xs), max(xs)); y = rnd.uniform(min(ys), max(ys))
            r = rnd.uniform(0.006, 0.02) * bw
            if rnd.random() < 0.5:
                td.ellipse([x - r, y - r, x + r, y + r], fill=c_dark + (70,))
            else:
                td.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 190, 60))
        tex.putalpha(ImageChops.multiply(tex.getchannel("A"), mask))
        img.alpha_composite(tex)
    d.line(pts + [pts[0]], fill=outline, width=max(2, int(bw * 0.028)), joint="curve")
    # reflet
    hl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    cx0, cy0 = min(xs) + bw * 0.3, min(ys) + (max(ys) - min(ys)) * 0.22
    hd.ellipse([cx0 - bw * 0.13, cy0 - bw * 0.07, cx0 + bw * 0.13, cy0 + bw * 0.07], fill=(255, 255, 255, 120))
    hl = hl.filter(ImageFilter.GaussianBlur(bw * 0.025))
    img.alpha_composite(hl)
    return mask


def draw_face(img, cx, cy, s, mood="happy"):
    """Visage kawaii : yeux brillants, joues roses, petite bouche."""
    d = ImageDraw.Draw(img)
    ex, ey, er = 0.37 * s, -0.04 * s, 0.165 * s
    for sx in (-1, 1):
        x = cx + sx * ex
        d.ellipse([x - er * 0.85, cy + ey - er, x + er * 0.85, cy + ey + er], fill=(28, 18, 20, 255))
        d.ellipse([x - er * 0.5 + er * 0.15, cy + ey - er * 0.75, x + er * 0.15, cy + ey - er * 0.2], fill=(255, 255, 255, 255))
        d.ellipse([x + er * 0.2, cy + ey + er * 0.2, x + er * 0.45, cy + ey + er * 0.45], fill=(255, 255, 255, 220))
    blush = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(blush)
    for sx in (-1, 1):
        x = cx + sx * 0.6 * s
        bd.ellipse([x - 0.15 * s, cy + 0.17 * s - 0.08 * s, x + 0.15 * s, cy + 0.17 * s + 0.08 * s], fill=(255, 110, 130, 150))
    blush = blush.filter(ImageFilter.GaussianBlur(0.04 * s))
    img.alpha_composite(blush)
    lw = max(2, int(0.045 * s))
    if mood == "open":
        d.ellipse([cx - 0.1 * s, cy + 0.1 * s, cx + 0.1 * s, cy + 0.3 * s], fill=(120, 30, 40, 255), outline=(28, 18, 20, 255), width=lw)
    elif mood == "sweat":
        d.arc([cx - 0.12 * s, cy + 0.08 * s, cx + 0.12 * s, cy + 0.28 * s], 200, 340, fill=(28, 18, 20, 255), width=lw)
    else:
        d.arc([cx - 0.13 * s, cy + 0.02 * s, cx + 0.13 * s, cy + 0.24 * s], 20, 160, fill=(28, 18, 20, 255), width=lw)


GOLD = ((255, 222, 120), (236, 160, 50), (170, 92, 25))
OUTL = (110, 55, 15, 255)


def make_sprite(level):
    """Image RGBA carrée (côté = 2 * rayon * marge) du niveau donné (0..7)."""
    name, _, r = LEVELS[level]
    margin = 1.55 if level in (3, 5, 6, 7) else 1.25
    side = int(2 * r * margin) * SS
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    c = side / 2
    R = r * SS
    seed = level * 31 + 5

    if level == 0:  # miette : triangle arrondi pâle
        pts = []
        for i in range(3):
            a = -math.pi / 2 + i * 2 * math.pi / 3
            pts.append((c + 1.08 * R * math.cos(a), c + 1.0 * R * math.sin(a) + 0.12 * R))
        mask = Image.new("L", (side, side), 0)
        ImageDraw.Draw(mask).polygon(pts, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(R * 0.12)).point(lambda v: 255 if v > 110 else 0)
        body = gradient_fill((side, side), mask, (255, 240, 170), (240, 195, 95), (190, 130, 50))
        img.alpha_composite(body)
        edge = mask.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(5))
        img.alpha_composite(Image.composite(Image.new("RGBA", (side, side), OUTL), Image.new("RGBA", (side, side), (0, 0, 0, 0)), edge))
        draw_face(img, c, c + 0.18 * R, 0.62 * R)

    elif level in (1, 2, 3):
        pal = GOLD if level != 3 else ((255, 190, 110), (232, 110, 40), (160, 45, 20))
        if level == 3:  # flammes derrière
            fl = Image.new("RGBA", (side, side), (0, 0, 0, 0))
            fd = ImageDraw.Draw(fl)
            rnd = random.Random(9)
            for k in range(9):
                a = -math.pi / 2 + (k - 4) * 0.33
                L = R * rnd.uniform(1.35, 1.7)
                bx, by = c + 0.75 * R * math.cos(a), c + 0.75 * R * math.sin(a)
                tx, ty = c + L * math.cos(a), c + L * math.sin(a)
                nx, ny = -math.sin(a) * R * 0.22, math.cos(a) * R * 0.22
                fd.polygon([(bx + nx, by + ny), (tx, ty), (bx - nx, by - ny)], fill=(255, 80, 20, 235))
                tx2, ty2 = c + (L * 0.8) * math.cos(a), c + (L * 0.8) * math.sin(a)
                fd.polygon([(bx + nx * 0.5, by + ny * 0.5), (tx2, ty2), (bx - nx * 0.5, by - ny * 0.5)], fill=(255, 210, 60, 255))
            fl = fl.filter(ImageFilter.GaussianBlur(R * 0.03))
            img.alpha_composite(fl)
        pts = blob_points(c, c, R * 1.08, R * 0.9, seed, wobble=0.07, squish=0.15)
        draw_body(img, pts, seed, *pal, OUTL)
        if level == 2:  # sauce ketchup qui coule
            d = ImageDraw.Draw(img)
            top = c - 0.9 * R
            sauce = [(c - 0.75 * R, top + 0.35 * R)]
            for i in range(9):
                x = c - 0.75 * R + i * 0.19 * R
                y = top + (0.05 if i % 2 == 0 else 0.0) * R
                sauce.append((x, y))
            sauce.append((c + 0.85 * R, top + 0.4 * R))
            for x, L in ((0.6, 0.55), (0.2, 0.75), (-0.25, 0.45), (-0.6, 0.62)):
                sauce.append((c + (x + 0.07) * R, top + 0.35 * R))
                sauce.append((c + (x + 0.07) * R, top + L * R))
                sauce.append((c + (x - 0.07) * R, top + L * R))
                sauce.append((c + (x - 0.07) * R, top + 0.35 * R))
            d.polygon(sauce, fill=(205, 25, 30, 255))
            for x, L in ((0.6, 0.55), (0.2, 0.75), (-0.25, 0.45), (-0.6, 0.62)):
                d.ellipse([c + (x - 0.085) * R, top + (L - 0.09) * R, c + (x + 0.085) * R, top + (L + 0.08) * R], fill=(205, 25, 30, 255))
            d.ellipse([c - 0.4 * R, top + 0.08 * R, c - 0.15 * R, top + 0.2 * R], fill=(255, 140, 140, 200))
            draw_face(img, c, c + 0.12 * R, 0.75 * R, "open")
        elif level == 3:
            draw_face(img, c, c + 0.08 * R, 0.75 * R, "sweat")
            d = ImageDraw.Draw(img)  # goutte de sueur
            x, y = c + 0.78 * R, c - 0.45 * R
            d.polygon([(x, y - 0.22 * R), (x - 0.1 * R, y), (x + 0.1 * R, y)], fill=(130, 210, 255, 255))
            d.ellipse([x - 0.1 * R, y - 0.08 * R, x + 0.1 * R, y + 0.12 * R], fill=(130, 210, 255, 255))
        else:
            draw_face(img, c, c + 0.05 * R, 0.75 * R)

    elif level == 4:  # boîte à nuggets
        d = ImageDraw.Draw(img)
        # nuggets qui dépassent
        for dx, dy, s in ((-0.45, -0.55, 0.42), (0.42, -0.6, 0.4)):
            pts = blob_points(c + dx * R, c + dy * R, s * R * 1.05, s * R * 0.85, seed + int(dx * 10), 0.08)
            draw_body(img, pts, seed + 3, *GOLD, OUTL)
        pts = blob_points(c, c - 0.42 * R, 0.55 * R, 0.46 * R, seed + 11, 0.06)
        draw_body(img, pts, seed + 4, *GOLD, OUTL)
        draw_face(img, c, c - 0.42 * R, 0.4 * R)
        box = [(c - 0.92 * R, c - 0.2 * R), (c + 0.92 * R, c - 0.2 * R), (c + 0.72 * R, c + 0.95 * R), (c - 0.72 * R, c + 0.95 * R)]
        m = Image.new("L", (side, side), 0)
        ImageDraw.Draw(m).polygon(box, fill=255)
        img.alpha_composite(gradient_fill((side, side), m, (255, 110, 100), (220, 35, 40), (140, 15, 25)))
        d = ImageDraw.Draw(img)
        d.polygon([(c - 0.88 * R, c + 0.02 * R), (c + 0.88 * R, c + 0.02 * R), (c + 0.84 * R, c + 0.22 * R), (c - 0.84 * R, c + 0.22 * R)], fill=(255, 235, 200, 255))
        d.line(box + [box[0]], fill=(110, 10, 20, 255), width=int(0.05 * R))
        # petit cœur sur la boîte
        hx, hy, hs = c, c + 0.58 * R, 0.16 * R
        d.ellipse([hx - hs * 1.05, hy - hs * 0.8, hx + hs * 0.05, hy + hs * 0.2], fill=(255, 220, 90, 255))
        d.ellipse([hx - hs * 0.05, hy - hs * 0.8, hx + hs * 1.05, hy + hs * 0.2], fill=(255, 220, 90, 255))
        d.polygon([(hx - hs * 1.0, hy - hs * 0.15), (hx + hs * 1.0, hy - hs * 0.15), (hx, hy + hs * 1.0)], fill=(255, 220, 90, 255))

    elif level == 5:  # roi nugget
        # cape
        d = ImageDraw.Draw(img)
        d.pieslice([c - 1.2 * R, c - 0.75 * R, c + 1.2 * R, c + 1.0 * R], 200, 340, fill=(140, 30, 160, 255))
        d.chord([c - 1.15 * R, c - 0.35 * R, c + 1.15 * R, c + 0.98 * R], 0, 180, fill=(150, 35, 170, 255))
        pts = blob_points(c, c + 0.05 * R, R * 1.0, R * 0.88, seed, 0.06, squish=0.12)
        draw_body(img, pts, seed, *GOLD, OUTL)
        draw_face(img, c, c + 0.12 * R, 0.72 * R)
        # couronne
        top = c - 0.78 * R
        cw = 0.62 * R
        crown = [(c - cw, top + 0.05 * R), (c - cw, top - 0.42 * R), (c - cw * 0.5, top - 0.15 * R), (c, top - 0.58 * R),
                 (c + cw * 0.5, top - 0.15 * R), (c + cw, top - 0.42 * R), (c + cw, top + 0.05 * R)]
        m = Image.new("L", (side, side), 0)
        ImageDraw.Draw(m).polygon(crown, fill=255)
        img.alpha_composite(gradient_fill((side, side), m, (255, 250, 170), (255, 200, 40), (190, 120, 10)))
        d = ImageDraw.Draw(img)
        d.line(crown + [crown[0]], fill=(140, 80, 0, 255), width=int(0.04 * R))
        for x, col in ((-0.33, (230, 40, 70)), (0, (60, 140, 255)), (0.33, (40, 200, 110))):
            d.ellipse([c + (x - 0.07) * R, top - 0.1 * R, c + (x + 0.07) * R, top + 0.04 * R], fill=col + (255,))
        for x, y in ((-cw, -0.42), (0, -0.58), (cw, -0.42)):
            d.ellipse([c + x - 0.07 * R, top + y * R - 0.07 * R, c + x + 0.07 * R, top + y * R + 0.07 * R], fill=(255, 245, 200, 255))

    elif level == 6:  # planète nugget
        d = ImageDraw.Draw(img)
        ring_back = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring_back)
        rw, rh = 1.62 * R, 0.42 * R
        rd.ellipse([c - rw, c - rh, c + rw, c + rh], outline=(255, 190, 70, 255), width=int(0.14 * R))
        ring_back = ring_back.rotate(-14, resample=Image.BICUBIC, center=(c, c))
        img.alpha_composite(ring_back)
        pts = blob_points(c, c, R * 0.98, R * 0.98, seed, 0.025)
        mask = draw_body(img, pts, seed, (255, 225, 140), (240, 150, 45), (165, 75, 20), OUTL)
        # bandes de planète
        bands = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bands)
        for y, hgt in ((-0.45, 0.1), (0.35, 0.14), (0.62, 0.08)):
            bd.ellipse([c - 1.3 * R, c + (y - hgt) * R, c + 1.3 * R, c + (y + hgt) * R], fill=(200, 100, 30, 90))
        bands.putalpha(ImageChops.multiply(bands.getchannel("A"), mask))
        img.alpha_composite(bands)
        draw_face(img, c, c + 0.05 * R, 0.7 * R)
        # anneau avant (moitié basse)
        ring_front = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        fd = ImageDraw.Draw(ring_front)
        fd.arc([c - rw, c - rh, c + rw, c + rh], 5, 175, fill=(255, 215, 110, 255), width=int(0.14 * R))
        ring_front = ring_front.rotate(-14, resample=Image.BICUBIC, center=(c, c))
        img.alpha_composite(ring_front)
        # étoiles + lunes
        for (sx, sy, ss) in ((-1.15, -0.85, 0.16), (1.1, -0.95, 0.13), (1.3, 0.55, 0.11), (-1.3, 0.7, 0.12), (0.2, -1.3, 0.1)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 235, 90, 255))
        for (mx, my, ms) in ((1.25, -0.25, 0.14), (-0.9, 1.05, 0.1)):
            d = ImageDraw.Draw(img)
            d.ellipse([c + (mx - ms) * R, c + (my - ms) * R, c + (mx + ms) * R, c + (my + ms) * R], fill=(240, 160, 60, 255), outline=OUTL, width=int(0.03 * R))

    elif level == 7:  # univers nugget
        gal = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        w = side
        yy, xx = np.mgrid[0:w, 0:w].astype(np.float32)
        dx, dy = (xx - c) / R, (yy - c) / R
        rr = np.sqrt(dx ** 2 + dy ** 2)
        th = np.arctan2(dy, dx)
        spiral = 0.5 + 0.5 * np.cos(2 * th - 4.2 * np.log(rr + 0.15))
        disk = np.clip(1.25 - rr, 0, 1)
        inten = np.clip(disk * (0.12 + 1.0 * spiral ** 3) + np.clip(0.5 - rr, 0, 1), 0, 1)
        col_in = np.array([255, 170, 255], np.float32)
        col_out = np.array([60, 40, 190], np.float32)
        t = np.clip(rr / 1.15, 0, 1)[..., None]
        col = col_in + (col_out - col_in) * t
        alpha = np.clip(inten * 2.0, 0, 1) * (rr < 1.25)
        arr = np.dstack([col * (0.55 + 0.45 * inten[..., None]), alpha[..., None] * 255]).astype(np.uint8)
        gal = Image.fromarray(arr, "RGBA").filter(ImageFilter.GaussianBlur(R * 0.015))
        glow = gal.filter(ImageFilter.GaussianBlur(R * 0.12))
        img.alpha_composite(glow)
        img.alpha_composite(gal)
        rnd = random.Random(42)
        d = ImageDraw.Draw(img)
        for _ in range(70):
            a = rnd.uniform(0, 6.28); rad = rnd.uniform(0.2, 1.2) * R
            x, y = c + rad * math.cos(a), c + rad * math.sin(a)
            s = rnd.uniform(0.008, 0.022) * R
            d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 255, 255, 230))
        for (sx, sy, ss) in ((-0.8, -0.7, 0.12), (0.85, -0.55, 0.1), (0.7, 0.8, 0.09), (-0.75, 0.75, 0.1)):
            star(img, c + sx * R, c + sy * R, ss * R, (255, 250, 200, 255))
        # nugget cosmique au centre
        pts = blob_points(c, c, R * 0.52, R * 0.45, seed, 0.06, squish=0.1)
        draw_body(img, pts, seed, (255, 235, 150), (245, 170, 60), (180, 95, 30), OUTL)
        draw_face(img, c, c + 0.03 * R, 0.38 * R, "open")
        # petite auréole
        d = ImageDraw.Draw(img)
        d.ellipse([c - 0.3 * R, c - 0.68 * R, c + 0.3 * R, c - 0.55 * R], outline=(255, 250, 180, 255), width=int(0.04 * R))

    out = img.resize((side // SS, side // SS), Image.LANCZOS)
    return out


def star(img, x, y, s, col):
    d = ImageDraw.Draw(img)
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = s if i % 2 == 0 else s * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d.polygon(pts, fill=col)


def build_all():
    return [make_sprite(i) for i in range(len(LEVELS))]


if __name__ == "__main__":
    sprites = build_all()
    W = sum(s.width for s in sprites) + 40 * len(sprites)
    H = max(s.height for s in sprites) + 40
    sheet = Image.new("RGBA", (W, H), (10, 10, 30, 255))
    x = 20
    for s in sprites:
        sheet.alpha_composite(s, (x, (H - s.height) // 2))
        x += s.width + 40
    sheet.convert("RGB").save("/home/claude/merge/sheet.png")
    print(sheet.size)
