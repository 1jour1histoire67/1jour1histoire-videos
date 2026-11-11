"""Rendu des images de la vidéo (sans état : chaque image se calcule seule)."""
import math, random, json, sys, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from theme import T, WORK
from sprites import LEVELS, build_all, star, make_bomb, silhouette, BOMB_R
from sim import W, H, FPS, CX, CY, AR, GAP

FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
POINTS = [0, 20, 60, 150, 400, 1000, 2500, 6000]

D = json.load(open(os.path.join(WORK, "simdata.json")))
FRAMES, EVENTS, UT = D["frames"], D["events"], D["ut"]
MERGES = [e for e in EVENTS if e[1] == "merge"]
REVEALS = {e[2]: e[0] for e in EVENTS if e[1] == "reveal"}
NF = len(FRAMES)
CAPS = json.load(open(os.path.join(WORK, "captions.json"), encoding="utf-8"))
BOMB_DROP = next((e[0] for e in EVENTS if e[1] == "bomb_drop"), None)
BOOM = next((e for e in EVENTS if e[1] == "boom"), None)
FINAL_NAME = LEVELS[-1][0]
BOUNCES = {}
for e in EVENTS:
    if e[1] == "bounce":
        BOUNCES.setdefault(e[5], []).append((e[0], e[6]))


def squash(u, t):
    k = 0.0
    for (tb, st) in BOUNCES.get(u, ()):
        age = t - tb
        if 0 <= age < 0.22:
            amp = min(1.0, st / 900)
            k = max(k, amp * math.exp(-age / 0.06) * math.cos(age * 28))
    return k

SPR = build_all()
BOMB = make_bomb()
SIL_FINAL = silhouette(SPR[-1].resize((640, 640), Image.LANCZOS))
SIL_SMALL = {}
_rot = {}


def sprite(level, ang, scale=1.0):
    b = int(round(math.degrees(ang) / 6)) % 60
    key = (level, b, round(scale, 2))
    if key not in _rot:
        s = SPR[level] if level >= 0 else BOMB
        if scale != 1.0:
            s = s.resize((max(2, int(s.width * scale)), max(2, int(s.height * scale))), Image.BICUBIC)
        _rot[key] = s.rotate(-b * 6, resample=Image.BICUBIC, expand=False)
        if len(_rot) > 3000:
            _rot.clear()
    return _rot[key]


_font = {}
def font(sz):
    if sz not in _font:
        _font[sz] = ImageFont.truetype(FONT, sz)
    return _font[sz]


# ---------- décor ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
ANG = np.arctan2(yy - CY, xx - CX)
RAD = np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2)
RAYFADE = (np.clip((RAD - AR * 0.6) / 200, 0, 1) * np.clip((1300 - RAD) / 500, 0, 1)).astype(np.float32)
BANDS = (np.sin(RAD / 38.0) > -0.35).astype(np.float32)  # rayons en tirets comme l'original
BASE = np.array(T["colors"]["base"], np.float32)
del yy, xx

NEON = [tuple(c) for c in T["colors"]["neon"]]


def background(t, col, boost=0.0):
    rot = t * (0.06 + boost * 0.8)
    pat = T.get("pattern", "stripes")
    if pat == "stripes":
        m = ((((RAD * np.cos(ANG) + RAD * np.sin(ANG)) / 120.0) - t * 0.7) % 1.0) < 0.5
    elif pat == "rays":
        m = (((ANG + rot) * 18 / (2 * math.pi)) % 1.0) < 0.42
    elif pat == "spiral":
        m = (((ANG + rot) * 10 / (2 * math.pi) + RAD / 140.0) % 1.0) < 0.5
    elif pat == "dots":
        X = RAD * np.cos(ANG) + t * 40; Y = RAD * np.sin(ANG)
        m = ((X % 110 - 55) ** 2 + (Y % 110 - 55) ** 2) < 26 ** 2
    else:  # checker polaire
        m = ((np.floor((ANG + rot) * 12 / (2 * math.pi)) + np.floor(RAD / 95.0 - t * 0.9)) % 2) < 1
    a = (m * RAYFADE * (0.26 + boost * 0.4))[..., None]
    c = np.array(T["colors"]["stripe"], np.float32)
    img = BASE * (1 - a) + c * a
    # intérieur de l'arène plus sombre
    inside = (RAD < AR - 4)[..., None]
    vign = np.clip(RAD / AR, 0, 1)[..., None]
    inner = np.array(T["colors"]["inner"], np.float32) - np.array(T["colors"].get("inner_edge", [40, 25, 0]), np.float32) * vign ** 4
    img = np.where(inside, inner, img)
    return Image.fromarray(img.astype(np.uint8), "RGB").convert("RGBA")


_neon = {}
def neon_layer(col):
    if col in _neon:
        return _neon[col]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    yj = CY - math.sqrt(AR ** 2 - GAP ** 2)
    a0 = math.degrees(math.asin(GAP / AR))
    box = [CX - AR, CY - AR, CX + AR, CY + AR]
    def shape(dd, w, c):
        dd.arc(box, -90 + a0, 270 - a0, fill=c, width=w)
        dd.line([(CX - GAP, -10), (CX - GAP, yj + 2)], fill=c, width=w)
        dd.line([(CX + GAP, -10), (CX + GAP, yj + 2)], fill=c, width=w)
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shape(ImageDraw.Draw(g), 26, col + (200,))
    g = g.filter(ImageFilter.GaussianBlur(18))
    lay.alpha_composite(g)
    shape(d, 9, col + (255,))
    shape(d, 3, tuple(min(255, v + 120) for v in col) + (255,))
    _neon[col] = lay
    return lay


def text_c(img, xy, s, sz, fill=(255, 255, 255, 255), stroke=(20, 10, 30, 255), sw=None, alpha=1.0, anchor="mm"):
    if alpha <= 0:
        return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    sw = sw if sw is not None else max(3, sz // 10)
    d.text(xy, s, font=font(sz), fill=fill, stroke_width=sw, stroke_fill=stroke, anchor=anchor, align="center")
    if alpha < 1:
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(lay)


def ease_back(x):
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def max_level_at(t):
    m = 0
    for lv, tr in REVEALS.items():
        if tr <= t:
            m = max(m, lv)
    return m


THUMBS = {}
def thumb(level, size):
    k = (level, size)
    if k not in THUMBS:
        s = SPR[level]
        f = size / max(s.width, s.height)
        THUMBS[k] = s.resize((max(1, int(s.width * f)), max(1, int(s.height * f))), Image.LANCZOS)
    return THUMBS[k]


def render(f):
    t = f / FPS
    ml = max_level_at(t)
    col = NEON[ml]
    fin = UT is not None and t >= UT
    boost = 0.0
    if fin:
        boost = max(0.0, 1 - (t - UT) / 3.0) * 1.0 + 0.25
    img = background(t, col, boost)
    img.alpha_composite(neon_layer(col))

    n = len(LEVELS); step = 112; x0 = CX - step * (n - 1) / 2; yb = 1712
    objs = FRAMES[f]
    # traînées scintillantes des objets qui tombent
    d = ImageDraw.Draw(img)
    prev = {o[0]: o for o in FRAMES[max(0, f - 4)]}
    for o in objs:
        u, x, y, a, lv, born = o
        if 0 <= lv <= 1 and u in prev:
            px, py = prev[u][1], prev[u][2]
            sp = math.hypot(x - px, y - py) / 4 * FPS
            if sp > 350:
                rnd = random.Random(u * 1000 + f)
                for k in range(5):
                    q = rnd.random()
                    tx = x + (px - x) * q * 1.6 + rnd.uniform(-10, 10)
                    ty = y + (py - y) * q * 1.6 + rnd.uniform(-6, 6) - 10
                    r = rnd.uniform(1.5, 3.5)
                    d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=(140, 230, 255, int(200 * (1 - q))))

    # anneaux + étincelles de fusion
    fx = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fx)
    for (te, _, lv, mx, my) in MERGES:
        age = t - te
        if 0 <= age < 0.7:
            r0 = LEVELS[lv][2]
            if age < 0.45:
                q = age / 0.45
                rr = r0 * (0.9 + 0.9 * q)
                aa = int(230 * (1 - q))
                fd.ellipse([mx - rr, my - rr, mx + rr, my + rr], outline=(170, 255, 150, aa), width=7)
                rr2 = rr * 0.75
                fd.ellipse([mx - rr2, my - rr2, mx + rr2, my + rr2], outline=(220, 255, 200, aa // 2), width=4)
            rnd = random.Random(int(te * 1000) + lv)
            npart = 10 + lv * 3
            for k in range(npart):
                ang = rnd.uniform(0, 6.283); v = rnd.uniform(180, 420) * (1 + lv * 0.12)
                px = mx + math.cos(ang) * v * age
                py = my + math.sin(ang) * v * age + 500 * age * age
                life = 1 - age / 0.7
                cc = rnd.choice([(255, 240, 120), (140, 230, 255), (255, 255, 255), (255, 150, 200)])
                s = rnd.uniform(3, 7) * life
                if k % 3 == 0:
                    star(fx, px, py, s * 2.2, cc + (int(255 * life),))
                else:
                    fd.ellipse([px - s, py - s, px + s, py + s], fill=cc + (int(255 * life),))

    # objets
    for o in sorted(objs, key=lambda o: o[4]):
        u, x, y, a, lv, born = o
        age = t - born
        sc = 1.0
        if born > 0 and age < 0.25:
            sc = 0.55 + 0.45 * ease_back(age / 0.25)
        if lv == 7:  # halo du final
            pulse = 0.75 + 0.25 * math.sin(t * 5)
            g = sprite(7, 0, 1.25 + 0.1 * pulse).filter(ImageFilter.GaussianBlur(20))
            g.putalpha(g.getchannel("A").point(lambda v: int(v * 0.8 * pulse)))
            img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
        if lv == -1:
            s = sprite(-1, a * 0.3, 1.0 + (0.12 * abs(math.sin(t * 14)) if BOOM and t > BOOM[0] - 1.2 else 0))
            if BOOM and t > BOOM[0] - 1.2 and int(t * 10) % 2 == 0:
                red = Image.new("RGBA", s.size, (255, 40, 40, 0)); red.putalpha(s.getchannel("A").point(lambda v: v // 2))
                s = s.copy(); s.alpha_composite(red)
            img.alpha_composite(s, (int(x - s.width / 2), int(y - s.height / 2)))
            rnd = random.Random(f)
            fx0, fy0 = x + 0.45 * BOMB_R, y - 1.45 * BOMB_R
            for k in range(0):
                ang = rnd.uniform(0, 6.28); rr = rnd.uniform(4, 22)
                d2 = ImageDraw.Draw(img)
                d2.ellipse([fx0 + rr * math.cos(ang) - 4, fy0 + rr * math.sin(ang) - 4, fx0 + rr * math.cos(ang) + 4, fy0 + rr * math.sin(ang) + 4], fill=(255, rnd.randint(150, 240), 60, 255))
            continue
        s = sprite(lv, a * 0.18 if lv >= 1 else a * 0.5, round(sc, 2))
        k = squash(u, t)
        if abs(k) > 0.03:
            s = s.resize((max(2, int(s.width * (1 + 0.22 * k))), max(2, int(s.height * (1 - 0.22 * k)))), Image.BILINEAR)
        img.alpha_composite(s, (int(x - s.width / 2), int(y - s.height / 2)))
    img.alpha_composite(fx)
    if BOOM and 0 <= t - BOOM[0] < 0.9:
        age = t - BOOM[0]; bx, by = BOOM[3], BOOM[4]
        ex = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ed = ImageDraw.Draw(ex)
        rr = 60 + 900 * age
        ed.ellipse([bx - rr, by - rr, bx + rr, by + rr], outline=(255, 200, 80, int(255 * (1 - age / 0.9))), width=int(40 * (1 - age / 0.9)) + 2)
        r2 = 220 * min(1, age / 0.15) * (1 - age / 0.9)
        ed.ellipse([bx - r2, by - r2, bx + r2, by + r2], fill=(255, 150, 40, int(230 * (1 - age / 0.9))))
        rnd = random.Random(99)
        for k in range(40):
            ang = rnd.uniform(0, 6.28); v = rnd.uniform(300, 1100)
            px, py = bx + math.cos(ang) * v * age, by + math.sin(ang) * v * age + 600 * age * age
            sz = rnd.uniform(6, 16) * (1 - age / 0.9)
            ed.ellipse([px - sz, py - sz, px + sz, py + sz], fill=(255, rnd.randint(120, 230), 40, 255))
        img.alpha_composite(ex.filter(ImageFilter.GaussianBlur(2)))

    # bulle de nom quand un niveau apparaît
    for lv, tr in REVEALS.items():
        age = t - tr
        newer = any(l2 > lv and tr < t2 <= t for l2, t2 in REVEALS.items())
        if 0 <= age < 1.6 and lv < 7 and not newer:
            ev = next(e for e in EVENTS if e[1] == "reveal" and e[2] == lv)
            x = min(max(ev[3], 260), W - 260); y = ev[4] - LEVELS[lv][2] - 40 - age * 60
            alpha = min(1, age / 0.12) * (1 if age < 1.2 else (1.6 - age) / 0.4)
            sz = int(58 * (0.7 + 0.3 * ease_back(min(1, age / 0.2))))
            text_c(img, (x, y), LEVELS[lv][0] + " !", min(sz, int(sz * 420 / max(1, font(58).getlength(LEVELS[lv][0] + " !")))), fill=(255, 225, 90, 255), alpha=alpha)

    # titre
    d = ImageDraw.Draw(img)

    # score animé
    sc = 0.0
    for (te, _, lv, _, _) in MERGES:
        if te <= t:
            sc += POINTS[lv] * min(1, (t - te) / 0.35)
    if not (fin and t - UT > 2.3):
      text_c(img, (CX, 1602), "SCORE : " + f"{int(round(sc / 10) * 10):,}".replace(",", " "), 64, fill=(200, 200, 215, 255), stroke=(10, 10, 25, 255), sw=5)

    # barre d'évolution
    for i in range(n):
        x = x0 + i * step
        tr = REVEALS.get(i, 0 if i == 0 else None)
        rev = tr is not None and tr <= t
        rr = 46
        if rev and i > 0 and t - tr < 0.4:
            rr = 46 * (0.8 + 0.2 * ease_back((t - tr) / 0.4)) + 10 * (1 - (t - tr) / 0.4)
        oc = (230, 230, 240, 255) if rev else (120, 120, 150, 255)
        if rev and i == ml:
            oc = col + (255,)
        d.ellipse([x - rr, yb - rr, x + rr, yb + rr], fill=(18, 18, 40, 230), outline=oc, width=5 if i == ml and rev else 3)
        if rev:
            th = thumb(i, int(rr * 1.55))
            img.alpha_composite(th, (int(x - th.width / 2), int(yb - th.height / 2)))
        else:
            if i == ml + 1:
                if i not in SIL_SMALL:
                    SIL_SMALL[i] = silhouette(thumb(i, 72), col=(0, 0, 0, 255), glow=(150, 150, 190))
                sl = SIL_SMALL[i]
                img.alpha_composite(sl, (int(x - sl.width / 2), int(yb - sl.height / 2)))
            d.text((x, yb + 2), "?", font=font(48), fill=(235, 235, 255) if i == ml + 1 else (170, 170, 200), anchor="mm")
        if fin and t - UT > 2.3:
            text_c(img, (x, yb + 72), str(i + 1), 40, fill=(255, 225, 90, 255), sw=4, alpha=min(1, (t - UT - 2.3) / 0.3))

    # accroche de départ
    if t < 1.7:  # ACCROCHE : silhouette géante du final
        k = 0 if t < 1.1 else (t - 1.1) / 0.6
        k = k * k * (3 - 2 * k)
        sc_s = 1 - 0.88 * k
        tx = CX + (x0 + (n - 1) * step - CX) * k; ty = 640 + (yb - 640) * k
        rr = 165 * sc_s * (1 + 0.04 * math.sin(t * 14))
        bub = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bub)
        bd.ellipse([tx - rr - 18, ty - rr - 18, tx + rr + 18, ty + rr + 18], fill=(255, 255, 255, 160))
        bd.ellipse([tx - rr, ty - rr, tx + rr, ty + rr], fill=(255, 205, 30, 255), outline=(120, 60, 0, 255), width=max(3, int(10 * sc_s)))
        img.alpha_composite(bub)
        text_c(img, (tx, ty + 10), "?", int(220 * sc_s), fill=(255, 255, 255, 255), stroke=(120, 60, 0, 255), sw=int(12 * sc_s) + 2)
        al = 1 if t < 1.3 else max(0, (1.7 - t) / 0.4)
        text_c(img, (CX, 250), "DEVINE LE", 84, alpha=al)
        text_c(img, (CX, 355), T["hook_title"], 104, fill=(255, 225, 90, 255), alpha=al)
    elif not fin:
        lvl_txt = f"NIVEAU {ml + 1}/{n}"
        dd = ImageDraw.Draw(img)
        dd.rounded_rectangle([CX - 175, 128, CX + 175, 212], radius=40, fill=(0, 0, 0, 150), outline=col + (255,), width=4)
        text_c(img, (CX, 170), lvl_txt, 52, fill=(255, 255, 255, 255), sw=3)
    if BOMB_DROP and not fin and BOMB_DROP <= t < BOOM[0]:
        al = min(1, (t - BOMB_DROP) / 0.2)
        bump = 1 + 0.06 * math.sin(t * 16)
        text_c(img, (CX, 300), "ATTENTION...", int(66 * bump), fill=(255, 255, 255, 255), alpha=al)
        text_c(img, (CX, 390), T["twist_title"], int(96 * bump), fill=(255, 70, 60, 255), alpha=al)
    if BOOM and BOOM[0] <= t < BOOM[0] + 1.6:
        age = t - BOOM[0]
        text_c(img, (CX, 360), T["twist_boom"], int(130 * (0.6 + 0.4 * ease_back(min(1, age / 0.25)))), fill=(255, 190, 50, 255), alpha=min(1, (1.6 - age) / 0.3))
    if not fin and UT and UT - 6 <= t < UT and t > (BOOM[0] + 2 if BOOM else 0):
        al = min(1, (t - (UT - 6)) / 0.3)
        text_c(img, (CX, 330), "LE FINAL ARRIVE...", int(68 * (1 + 0.05 * math.sin(t * 10))), alpha=al)

    if fin:
        age = t - UT
        if age > 0.3:
            k = min(1, (age - 0.3) / 0.3)
            bump = (0.6 + 0.4 * ease_back(k)) * (1 + 0.03 * math.sin(t * 6))
            text_c(img, (CX, 200), T.get("final_intro", "TU AS CRÉÉ LE"), int(64 * bump), alpha=k)
            fs = 92
            while font(fs).getlength(FINAL_NAME + " !") > 980: fs -= 4
            text_c(img, (CX, 295), FINAL_NAME + " !", int(fs * bump), fill=(255, 225, 90, 255), alpha=k)
        if age > 2.3:
            k = min(1, (age - 2.3) / 0.3)
            text_c(img, (CX, 390), "TON PRÉFÉRÉ ? COMMENTE 1 À 8", int(54 * (0.7 + 0.3 * ease_back(k))), fill=(140, 230, 255, 255), alpha=k)
        if age < 0.4:  # flash blanc
            fl = Image.new("RGBA", (W, H), (255, 255, 255, int(200 * (1 - age / 0.4))))
            img.alpha_composite(fl)
        if age < 0.7:  # secousse
            amp = 18 * (1 - age / 0.7)
            ox = int(amp * math.sin(age * 90)); oy = int(amp * math.cos(age * 77))
            sh = Image.new("RGBA", (W, H), BASE.astype(int).tolist() + [255] if False else (9, 9, 28, 255))
            sh.paste(img, (ox, oy))
            img = sh
    # SOUS-TITRES du commentateur
    for (cs, ce, ctext) in CAPS:
        if cs - 0.05 <= t < ce + 0.25:
            age = t - cs + 0.05
            sz = 60
            words = ctext.replace(" !", "\u00a0!").replace(" ?", "\u00a0?").split(" "); lines = [""]
            for wd in words:
                trial = (lines[-1] + " " + wd).strip()
                if font(sz).getlength(trial) > 960 and lines[-1]:
                    lines.append(wd)
                else:
                    lines[-1] = trial
            pop = 0.85 + 0.15 * ease_back(min(1, age / 0.18))
            y0 = 1505 - (len(lines) - 1) * 72
            for li, ln in enumerate(lines):
                text_c(img, (CX, y0 + li * 72), ln, int(sz * pop), fill=(255, 235, 90, 255) if li == 0 else (255, 255, 255, 255), stroke=(10, 6, 20, 255), sw=7)
            break
    if BOOM and 0 <= t - BOOM[0] < 0.6:
        age = t - BOOM[0]; amp = 26 * (1 - age / 0.6)
        sh = Image.new("RGBA", (W, H), tuple(T["colors"]["base"]) + (255,)); sh.paste(img, (int(amp * math.sin(age * 95)), int(amp * math.cos(age * 81)))); img = sh
        if age < 0.12:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 240, 200, int(220 * (1 - age / 0.12)))))
    if t > NF / FPS - 0.3:
        img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(255 * min(1, (t - (NF / FPS - 0.3)) / 0.3)))))
    return img.convert("RGB")


def encode(start, end, out):
    tmp = out[:-4] + ".part.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for f in range(start, end):
        p.stdin.write(render(f).tobytes())
        if (f - start) % 150 == 0:
            print(out, f, flush=True)
    p.stdin.close()
    if p.wait() == 0:
        os.replace(tmp, out)


if __name__ == "__main__":
    if sys.argv[1] == "still":
        for tt in map(float, sys.argv[2:]):
            render(int(tt * FPS)).save(os.path.join(WORK, f"still_{tt:05.1f}.png"))
    else:
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        encode(a, min(b, NF), out)
