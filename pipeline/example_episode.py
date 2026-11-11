"""EXEMPLE COMPLET — Épisode 4 « Miss Insubmersible » (Violet Jessop), publié le 10/11/2026.
À copier dans le dossier de l'épisode (à côté de lines.json / timeline.json / voice.wav), sous le nom episode.py,
puis à réécrire : titre, badge, dessins, scènes et liste SFX pour la nouvelle histoire.
Une scène = fonction (t, t0, t1) -> (image RGBA plein écran, zoom, tremblement). Les mots-clés de ep.wt(ligne, "mot")
doivent exister dans la ligne correspondante de lines.json.
"""
import os, sys, math, random
EP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("PIPELINE", os.path.join(os.path.dirname(EP), "pipeline")))
from lib_video import *

ep = Episode(EP, title="MISS INSUBMERSIBLE", badge="ÉP. 4")
wt, L_ = ep.wt, ep.L

# ---------- dessins propres à l'épisode ----------
def ship_layer(w=900, hospital=False, lights=False):
    h = int(w * 0.36)
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    hull_top = h * 0.55; wl = h * 0.86
    hull = (240, 240, 236, 255) if hospital else (22, 22, 26, 255)
    d.polygon([(w * 0.03, hull_top), (w * 0.97, hull_top - h * 0.03), (w * 0.93, h * 0.97), (w * 0.08, h * 0.97)], fill=hull)
    d.polygon([(w * 0.075, wl), (w * 0.94, wl), (w * 0.93, h * 0.97), (w * 0.08, h * 0.97)], fill=(150, 30, 26, 255))
    if hospital:
        d.rectangle([w * 0.05, h * 0.7, w * 0.95, h * 0.74], fill=(40, 140, 70, 255))
        for cx in (0.3, 0.7):
            x, y, s = w * cx, h * 0.66, h * 0.07
            d.rectangle([x - s, y - s * 0.3, x + s, y + s * 0.3], fill=RED + (255,)); d.rectangle([x - s * 0.3, y - s, x + s * 0.3, y + s], fill=RED + (255,))
    sup = (246, 244, 236, 255)
    d.rectangle([w * 0.18, h * 0.42, w * 0.82, hull_top], fill=sup)
    d.rectangle([w * 0.24, h * 0.35, w * 0.76, h * 0.43], fill=sup)
    win = (255, 220, 120, 255) if lights else (60, 60, 70, 255)
    for x in np.linspace(w * 0.2, w * 0.8, 26): d.rectangle([x, h * 0.46, x + w * 0.008, h * 0.5], fill=win)
    for fx in [0.3, 0.43, 0.56, 0.69]:
        x = w * fx
        d.polygon([(x - w * 0.028, h * 0.36), (x - w * 0.02, h * 0.06), (x + w * 0.034, h * 0.06), (x + w * 0.03, h * 0.36)], fill=(220, 160, 70, 255))
        d.polygon([(x - w * 0.021, h * 0.06), (x + w * 0.034, h * 0.06), (x + w * 0.033, h * 0.13), (x - w * 0.02, h * 0.13)], fill=(20, 20, 20, 255))
    return L

def iceberg_layer(w=620):
    h = w; L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.polygon([(0, h), (w * 0.15, h * 0.4), (w * 0.35, h * 0.5), (w * 0.5, h * 0.05), (w * 0.7, h * 0.45), (w * 0.85, h * 0.35), (w, h)], fill=(220, 240, 250, 255))
    d.polygon([(w * 0.5, h * 0.05), (w * 0.7, h * 0.45), (w * 0.6, h), (w * 0.4, h)], fill=(170, 210, 235, 255))
    return L

def sea(night=True):
    top, mid, bot = ((8, 12, 30), (30, 40, 70), (6, 14, 30)) if night else ((120, 180, 225), (220, 230, 240), (30, 80, 120))
    hz = 1000
    img = Image.new("RGBA", (W, H)); img.paste(vgrad(W, hz, top, mid), (0, 0))
    img.paste(vgrad(W, H - hz, (bot[0] + 20, bot[1] + 30, bot[2] + 40), bot), (0, hz))
    if night:
        d = ImageDraw.Draw(img); rng = random.Random(3)
        for _ in range(90):
            x, y = rng.randint(0, W), rng.randint(0, 900); r = rng.choice([1, 2, 2, 3])
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 200))
    return vignette(img, 0.5).convert("RGBA")

A = {}
def build():
    A["night"] = sea(True); A["day"] = sea(False); A["paper"] = paper()
    A["ship"] = ship_layer(980, lights=True); A["ship_s"] = ship_layer(300); A["hosp_s"] = ship_layer(300, hospital=True)
    A["ice"] = iceberg_layer(); A["woman"] = woman_layer(760)
    A["titanic"] = pill("TITANIC", fill=WHITE, size=96)
    A["violet"] = pill("VIOLET JESSOP", fill=GOLD, size=96)
    A["t1912"] = pill("1912 · TITANIC", fill=GOLD, size=84)
    A["insub"] = pill("« INSUBMERSIBLE »", fill=WHITE, size=84)
    A["iceberg"] = stamp_layer("ICEBERG", size=200, seed=6)

# ---------- scènes (extrait : 3 scènes + fin, l'original en avait 12) ----------
def S_hook(t, t0, t1, stamps=True):
    img = A["night"].copy()
    put_bottom(img, A["ship"], W / 2, 1130 + math.sin(t * 1.4) * 8); waves(img, t)
    if stamps:
        pop_in(img, A["titanic"], t, wt(0, "Titanic") - 0.2, W / 2, 560, rot=-3)
        tj = wt(1, "jumeaux") - 0.35
        for k, (x, L) in enumerate([(220, A["ship_s"]), (860, A["hosp_s"])]):
            pop_in(img, L, t, tj + k * 0.12, x, 760)
    return img, 1.0 + 0.06 * prog(t, t0, t1 - t0), 0

def S_intro(t, t0, t1):
    img = A["paper"].copy()
    slide_in(img, A["woman"], t, t0, W / 2, 1080, from_dy=600)
    pop_in(img, A["violet"], t, wt(2, "Violet") - 0.1, W / 2, 560, rot=-3)
    return img, 1.0 + 0.05 * prog(t, t0, t1 - t0), 0

def S_titanic(t, t0, t1):
    img = A["night"].copy()
    ti = wt(9, "iceberg")
    tilt = 0 if t < ti else min(4, (t - ti) * 3)
    put_bottom(img, A["ship"].rotate(-tilt, Image.BICUBIC, expand=True), W / 2 - 80, 1130 + math.sin(t * 1.4) * 8)
    pi_ = ease_out(prog(t, L_(9), 1.6))
    if pi_ > 0: put_bottom(img, A["ice"], W + 400 - pi_ * 480, 1180)
    waves(img, t)
    pop_in(img, A["t1912"], t, t0 + 0.05, W / 2, 560, rot=-3)
    if t < ti - 0.1: pop_in(img, A["insub"], t, wt(8, "insubmersible") - 0.4, W / 2, 720, rot=3)
    sh = stamp_in(img, A["iceberg"], t, ti - 0.1, W / 2, 800, -10)   # tampon -> tremblement
    return img, 1.0 + 0.04 * prog(t, t0, t1 - t0), sh

def S_end(t, t0, t1):
    # dernière ligne = « Et dire que, » : on revient exactement sur l'image d'ouverture pour la boucle
    img, z, sh = S_hook(t, 0, 1, stamps=False)
    return img, 1.08 - 0.08 * ease_out(prog(t, t0, 0.5)), 0

# Les scènes doivent couvrir 0 -> ep.TOTAL sans trou (ici on saute des lignes pour l'exemple)
SC = [(S_hook, 0.0, L_(2)), (S_intro, L_(2), L_(7)), (S_titanic, L_(7), L_(22)), (S_end, L_(22), ep.TOTAL)]
SFX = dict(stamps=[wt(9, "iceberg") - 0.1],
           pops=[wt(0, "Titanic") - 0.2, wt(1, "jumeaux") - 0.35, wt(2, "Violet") - 0.1, wt(8, "insubmersible") - 0.4],
           whooshes=[(L_(9), 1.6)])

if __name__ == "__main__":
    ep.main(SC, build, SFX)
