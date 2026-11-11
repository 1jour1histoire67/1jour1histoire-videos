"""Bande son : voix de plus en plus grave + bruitages + petite musique."""
import json, math, subprocess, os, wave
import numpy as np
from theme import T, WORK
from sprites import LEVELS

SR = 44100
DUR = 62.0
OUT = WORK
os.makedirs(OUT + "/voice", exist_ok=True)
D = json.load(open(os.path.join(WORK, "simdata.json")))
EV, UT = D["events"], D["ut"]

# ---------- voix ----------
CENTS = [450, 280, 100, -120, -360, -600, -860, -1150]
TEMPO = [1.0, 0.98, 0.95, 0.93, 0.9, 0.87, 0.84, 0.8]


def load_wav(p):
    with wave.open(p) as w:
        sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
        a = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768
    if ch == 2:
        a = a.reshape(-1, 2).mean(1)
    assert sr == SR, sr
    return a


def make_voice(level, text=None, tag=None, speed="140"):
    if text is None:
        text = LEVELS[level][1] + " !"
        if level == 7:
            text = T["final_voice"]
    tag = tag or f"v{level}"
    raw = f"{OUT}/voice/raw_{tag}.wav"
    fin = f"{OUT}/voice/{tag}.wav"
    subprocess.run(["espeak-ng", "-v", T["voice"]["engine"], "-s", speed, "-p", str(T["voice"]["pitch"]), "-a", "180", "-w", raw, text], check=True)
    rev = "35" if level < 7 else "70"
    subprocess.run(["sox", raw, "-r", str(SR), "-c", "1", fin, "rate", str(SR), "gain", "-8", "pitch", str(CENTS[level]), "tempo", "-s", str(TEMPO[level]),
                    "phaser", "0.85", "0.8", "2", "0.25", "0.6", "-s",  # léger côté synthétique
                    "overdrive", "2", "lowpass", "6500", "reverb", rev, "norm", "-2", "pad", "0", "0.3"], check=True)
    return load_wav(fin)


VOICES = [make_voice(i) for i in range(len(LEVELS))]


# ---------- synthèse ----------
def env(n, a=0.005, r=0.1):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a) * np.exp(-t / r)
    return e


def pop(level):
    n = int(SR * 0.22)
    t = np.arange(n) / SR
    f0 = 820 / (1.22 ** level)
    f = f0 * (1 + 0.9 * np.exp(-t / 0.03))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * env(n, 0.002, 0.06 + level * 0.01)
    s += 0.3 * np.sin(2 * ph) * env(n, 0.002, 0.03)
    return s * (0.35 + level * 0.04)


def tick():
    n = int(SR * 0.06)
    t = np.arange(n) / SR
    f = 1500 - 6000 * t
    return 0.08 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.015)


def chime(level):
    out = np.zeros(int(SR * 1.2))
    base = 523.25 * (2 ** (level / 12))
    for k, m in enumerate((1, 1.25, 1.5, 2)):
        st = int(k * 0.07 * SR)
        n = len(out) - st
        t = np.arange(n) / SR
        tone = (np.sin(2 * np.pi * base * m * t) + 0.3 * np.sin(2 * np.pi * base * m * 2.01 * t)) * env(n, 0.003, 0.35)
        out[st:] += tone * 0.12
    return out


def boom():
    n = int(SR * 3.0)
    t = np.arange(n) / SR
    f = 40 + 90 * np.exp(-t / 0.15)
    s = 0.9 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 0.8)
    rng = np.random.default_rng(1)
    s += 0.25 * rng.standard_normal(n) * env(n, 0.001, 0.12)
    for m in (261.6, 329.6, 392.0, 523.3, 659.3):  # accord brillant
        s += 0.07 * np.sin(2 * np.pi * m * t) * np.minimum(1, t / 0.4) * np.exp(-t / 2.2)
    return s


def music():
    n = int(SR * DUR)
    out = np.zeros(n)
    bpm = T["music"]["bpm"]; beat = 60 / bpm
    chords = [tuple(c) for c in T["music"]["chords"]]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    tt = 0.0; i = 0
    while tt < DUR:
        ch = chords[(i // 8) % 4]
        note = ch[[0, 1, 2, 3, 2, 1, 3, 2][i % 8]] + 12
        st = int(tt * SR); ln = int(beat / 2 * SR)
        t = np.arange(ln) / SR
        tri = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * hz(note) * t))
        seg = 0.05 * tri * env(ln, 0.004, 0.16)
        out[st:st + ln] += seg[:max(0, min(ln, n - st))]
        if i % 2 == 0:  # basse + kick sur les temps
            bl = int(beat * SR); tb = np.arange(bl) / SR
            bass = 0.06 * np.sin(2 * np.pi * hz(ch[0] - 12) * tb) * env(bl, 0.01, 0.25)
            fk = 50 + 120 * np.exp(-tb / 0.03)
            kick = 0.16 * np.sin(2 * np.pi * np.cumsum(fk) / SR) * env(bl, 0.001, 0.09)
            e = min(bl, n - st)
            out[st:st + e] += (bass + kick)[:e]
        if i % 4 == 2:  # charleston
            hl = int(0.05 * SR)
            hh = 0.025 * np.random.default_rng(i).standard_normal(hl) * env(hl, 0.001, 0.012)
            e = min(hl, n - st); out[st:st + e] += hh[:e]
        tt += beat / 2; i += 1
    return out


N = int(SR * DUR)
fx = np.zeros(N + SR * 4)
vox = np.zeros(N + SR * 4)


def add(buf, t, s, g=1.0):
    st = int(t * SR)
    if st >= len(buf):
        return
    e = min(len(s), len(buf) - st)
    buf[st:st + e] += s[:e] * g


def boing(level, strength):
    n = int(SR * 0.16)
    t = np.arange(n) / SR
    f0 = 1000 / (1.25 ** level)
    f = f0 * (0.7 + 0.6 * np.exp(-t / 0.02)) * (1 + 0.04 * np.sin(2 * np.pi * 30 * t))
    g = 0.05 + 0.1 * min(1, strength / 1500)
    return g * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.04)


def riser(dur=1.3):
    n = int(SR * dur); t = np.arange(n) / SR
    rng = np.random.default_rng(3)
    noise = rng.standard_normal(n)
    # bruit filtré qui monte + sinus qui glisse
    k = (t / dur) ** 2
    s = 0.05 * noise * k + 0.08 * np.sin(2 * np.pi * np.cumsum(200 + 1400 * k) / SR) * k
    return s


def hiss(dur):
    n = int(SR * dur); rng = np.random.default_rng(5)
    return 0.05 * rng.standard_normal(n) * (0.6 + 0.4 * np.sin(np.arange(n) / SR * 2 * np.pi * 9))



# ================= BRUITAGES =================
def _t(d):
    return np.arange(int(SR * d)) / SR

def _env(n, a, r):
    return env(n, a, r)

def vine_boom():
    t = _t(1.6); n = len(t)
    f = 48 + 70 * np.exp(-t / 0.05)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.45)
    s += 0.6 * np.random.default_rng(1).standard_normal(n) * np.exp(-t / 0.015)
    out = s.copy()
    for k, g in ((int(0.09 * SR), 0.45), (int(0.19 * SR), 0.25), (int(0.31 * SR), 0.12)):  # écho
        out[k:] += s[:n - k] * g
    return 0.9 * np.tanh(out * 1.6)

def airhorn(d=0.55):
    t = _t(d); n = len(t)
    s = np.zeros(n)
    for f in (466, 554, 698, 932):
        for det in (-3, 0, 3):
            s += np.sign(np.sin(2 * np.pi * (f + det) * t + 0.3 * np.sin(2 * np.pi * 6 * t)))
    s = s / 12 * np.minimum(1, t / 0.01) * np.minimum(1, (d - t) / 0.04)
    return 0.32 * np.tanh(s * 2.2)

def airhorn3():
    out = np.zeros(int(SR * 1.5))
    for st, d in ((0, 0.18), (0.24, 0.18), (0.5, 0.75)):
        a = airhorn(d); i = int(st * SR); out[i:i + len(a)] += a[:len(out) - i]
    return out

def squeak(pitch=1.0):
    t = _t(0.16); n = len(t)
    f = 1100 * pitch * (1 + 0.6 * np.sin(np.pi * t / 0.16))
    return 0.22 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.16) ** 0.6

def record_scratch():
    t = _t(0.55); n = len(t)
    rng = np.random.default_rng(4)
    noise = rng.standard_normal(n)
    sp = np.abs(np.sin(2 * np.pi * 3.5 * t)) * 0.9 + 0.1
    s = np.zeros(n); acc = 0.0
    ker = np.ones(12) / 12
    filt = np.convolve(noise, ker, mode="same")
    for i in range(n):
        acc += sp[i] * 1.0; s[i] = filt[int(acc) % n]
    return 0.5 * s * np.minimum(1, (0.55 - t) / 0.05)

def slide_whistle(up=True, d=0.7):
    t = _t(d)
    k = t / d
    f = (600 + 1400 * k) if up else (2000 - 1500 * k)
    f = f * (1 + 0.02 * np.sin(2 * np.pi * 7 * t))
    return 0.18 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.05)

def clown_honk():
    t = _t(0.35)
    s = 0
    for f in (330, 392):
        s = s + np.sign(np.sin(2 * np.pi * f * t)) * 0.5
    return 0.22 * s * np.exp(-t / 0.2) * np.minimum(1, t / 0.01)

def fart():
    t = _t(0.7); n = len(t)
    rng = np.random.default_rng(9)
    f = 85 + 25 * np.sin(2 * np.pi * 3 * t) + 15 * rng.standard_normal(n).cumsum() / np.sqrt(np.arange(1, n + 1))
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    am = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 9 * t + rng.uniform(0, 3)))
    s = np.convolve(saw * am, np.ones(25) / 25, mode="same")
    return 0.55 * s * np.minimum(1, t / 0.02) * np.minimum(1, (0.7 - t) / 0.15)

def drumroll(d=1.8):
    n = int(SR * d); out = np.zeros(n)
    rng = np.random.default_rng(2)
    rate = 26
    for k in range(int(d * rate)):
        i = int(k / rate * SR); L = int(0.05 * SR)
        hit = rng.standard_normal(L) * np.exp(-np.arange(L) / SR / 0.012)
        g = 0.05 + 0.2 * (k / (d * rate)) ** 2
        out[i:i + L] += hit[:n - i] * g
    return out

def crash():
    t = _t(2.2); n = len(t)
    noise = np.random.default_rng(6).standard_normal(n)
    hp = noise - np.convolve(noise, np.ones(6) / 6, mode="same")
    return 0.35 * hp * np.exp(-t / 0.7)

def cheer():
    t = _t(2.5); n = len(t)
    rng = np.random.default_rng(8)
    s = np.convolve(rng.standard_normal(n), np.ones(40) / 40, mode="same") * 3
    for k in range(10):
        st = rng.uniform(0, 1.6); f0 = rng.uniform(500, 900)
        m = (t > st) & (t < st + 0.6)
        tt = t[m] - st
        s[m] += 0.15 * np.sin(2 * np.pi * np.cumsum(f0 + 400 * tt) / SR) * np.sin(np.pi * tt / 0.6)
    return 0.3 * s * np.minimum(1, t / 0.3) * np.minimum(1, (2.5 - t) / 0.8)

def howl():
    t = _t(2.2)
    f = 380 + 420 * np.sin(np.pi * np.clip(t / 1.6, 0, 1)) ** 0.7
    f = f * (1 + 0.025 * np.sin(2 * np.pi * 5.5 * t))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return 0.22 * s * np.minimum(1, t / 0.2) * np.minimum(1, (2.2 - t) / 0.6)

def dun_dun_dun():
    out = np.zeros(int(SR * 1.9))
    for k, (st, f, d) in enumerate(((0, 98, 0.3), (0.38, 92.5, 0.3), (0.76, 82.4, 1.0))):
        t = _t(d)
        s = sum(np.sign(np.sin(2 * np.pi * f * m * t)) / m for m in (1, 2, 3)) * np.exp(-t / (0.25 + 0.4 * (k == 2)))
        i = int(st * SR); out[i:i + len(t)] += 0.25 * s
    return out

def sad_trombone():
    out = np.zeros(int(SR * 2.4))
    for k, (st, f, d) in enumerate(((0, 294, 0.4), (0.45, 277, 0.4), (0.9, 262, 0.4), (1.35, 247, 1.0))):
        t = _t(d)
        ff = f * (1 + 0.03 * np.sin(2 * np.pi * 5 * t) * (k == 3))
        saw = 2 * ((np.cumsum(ff) / SR) % 1) - 1
        s = np.convolve(saw, np.ones(8) / 8, mode="same") * np.minimum(1, t / 0.04) * np.minimum(1, (d - t) / 0.08)
        i = int(st * SR); out[i:i + len(t)] += 0.2 * s
    return out

def pew():
    t = _t(0.18)
    f = 1800 * np.exp(-t / 0.05) + 200
    return 0.15 * np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / 0.08)

def ding():
    t = _t(1.0)
    return 0.25 * (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 2637 * t)) * np.exp(-t / 0.3)

def _sfx(spec):
    name, _, arg = spec.partition(":")
    f = globals()[name]
    return f(float(arg)) if arg else f()
SFX_REVEAL = {int(k): [_sfx(x) for x in v] for k, v in T["sfx_reveal"].items()}

TICK = tick()
POPS = [pop(i) for i in range(8)]
# ---------- planning du commentateur ----------
REV_T = {e[2]: e[0] for e in EV if e[1] == "reveal"}
BD = next((e[0] for e in EV if e[1] == "bomb_drop"), None)
BM = next((e[0] for e in EV if e[1] == "boom"), None)

def level_at(t):
    m = 0
    for lv, tr in REV_T.items():
        if tr <= t: m = max(m, lv)
    return m

_vcache = {}
def say(text, lvl, speed="160"):
    key = (text, lvl)
    if key not in _vcache:
        spoken = text
        for k_, v_ in T.get("say_replace", {}).items():
            spoken = spoken.replace(k_, v_)
        _vcache[key] = make_voice(lvl, spoken, f"l{len(_vcache)}", str(T["voice"].get("speed", 170)))
    return _vcache[key]

# (temps souhaité, priorité, texte affiché, niveau de voix)
plan = [(0.35, 0, T["hook_voice"], 0)]
EXTRA = {int(k): v for k, v in T["extra"].items()}
for lv, tr in sorted(REV_T.items(), key=lambda x: x[1]):
    if lv == 7:
        plan.append((tr + 0.35, 0, T["final_voice"], 7))
        plan.append((tr + 2.0, 1, "Incroyable !", 7))
    elif tr > 1.0:
        plan.append((tr + 0.08, 0, LEVELS[lv][1] + " !", lv))
        for x in EXTRA.get(lv, []):
            plan.append((tr + 1.4, 1, x, lv))
if BD:
    tv = T["twist_voice"]
    plan += [(BD + 0.15, 0, tv[0], 4), (BM + 0.6, 0, tv[1], 5), (BM + 2.6, 0, tv[2], 5)]
plan += [(UT - 4.5, 1, "Le final arrive...", 6), (UT + 2.5, 0, "Ton préféré ? Dis-le en commentaire !", 4),
         (UT + 5.3, 0, "Abonne-toi pour le prochain !", 4)]
FILL = T["fill"]

placed = []   # (start, end, texte, wav)
def free(st, en):
    return all(en + 0.15 <= a or st >= b + 0.15 for a, b, _, _ in placed)
for want, pr, txt, lv in sorted([p for p in plan if p[1] == 0]):
    w = say(txt, lv); d = len(w) / SR
    st = want
    while not free(st, st + d):
        st += 0.1
    placed.append((st, st + d, txt, w))
for want, pr, txt, lv in sorted([p for p in plan if p[1] == 1]):
    w = say(txt, lv); d = len(w) / SR
    for dt in (0, 0.3, 0.6, 1.0):
        if free(want + dt, want + dt + d):
            placed.append((want + dt, want + dt + d, txt, w)); break
# remplissage : une réplique dès qu'il y a un trou de plus de 2,6 s
k = 0
t = 2.0
end_fill = UT - 1.0
while t < end_fill:
    placed.sort()
    nxt = min([a for a, b, _, _ in placed if a > t] + [end_fill])
    busy = any(a <= t < b + 0.15 for a, b, _, _ in placed)
    if busy:
        t = max(b for a, b, _, _ in placed if a <= t) + 0.2; continue
    if nxt - t > 2.6:
        txt = FILL[k % len(FILL)]; k += 1
        w = say(txt, level_at(t + 0.6)); d = len(w) / SR
        st = t + 0.6
        if st + d < nxt - 0.2 and not (BD and BD - 0.5 < st < BM + 3):
            placed.append((st, st + d, txt, w))
        t = st + d + 0.9
    else:
        t = nxt + 0.05
placed.sort()
for st, en, txt, w in placed:
    add(vox, st, w, 1.0)
json.dump([(round(st, 2), round(en, 2), txt) for st, en, txt, w in placed], open(os.path.join(WORK, "captions.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("répliques :", len(placed), " temps de parole :", round(sum(en - st for st, en, _, _ in placed), 1), "s")

# ---- placement des bruitages ----
add(fx, 0.0, vine_boom(), 1.2)
add(fx, 0.05, airhorn3(), 0.9)
for lv, tr in REV_T.items():
    if 3 <= lv < 7:
        add(fx, max(0, tr - 1.3), riser(1.3), 0.8)
    for k, x in enumerate(SFX_REVEAL.get(lv, [])):
        add(fx, tr + 0.02 + k * 0.18, x, 1.1)
if UT:
    add(fx, UT - 1.9, drumroll(1.9), 1.0)
    add(fx, UT, crash(), 1.0)
    add(fx, UT + 0.05, airhorn3(), 1.0)
    add(fx, UT + 0.1, vine_boom(), 1.1)
    add(fx, UT + 0.6, cheer(), 1.0)
if BD:
    add(fx, BD, dun_dun_dun(), 1.0)
    add(fx, BD + 0.9, howl(), 1.0)
    add(fx, BM, boom(), 1.0)
    add(fx, BM + 0.05, record_scratch(), 1.0)
    add(fx, BM + 0.4, slide_whistle(False, 0.9), 1.0)
    add(fx, BM + 2.2, sad_trombone(), 0.8)
add(fx, (UT or 55) + 2.5, ding(), 1.0)
last_b = -1.0
rngs = np.random.default_rng(12)
SQ = [squeak(p) for p in (1.6, 1.4, 1.2, 1.0, 0.85, 0.7, 0.6, 0.5)]
for e in EV:
    t, typ, lv, x, y = e[:5]
    if typ == "bounce":
        if e[6] > 650 and t - last_b > 0.12 and lv >= 0:
            add(fx, t, SQ[lv] if rngs.random() < 0.6 else boing(lv, e[6]), 0.7)
            last_b = t
        continue
    if typ == "drop":
        add(fx, t + 0.25, TICK)
    elif typ == "merge":
        add(fx, t, POPS[lv])
        is_reveal = REV_T.get(lv) is not None and abs(REV_T[lv] - t) < 1e-6
        if lv == 7:
            add(fx, t, boom(), 0.9)
        elif is_reveal:
            add(fx, t + 0.02, chime(lv))
        else:
            add(fx, t + 0.01, [pew(), SQ[lv], clown_honk()][int(rngs.integers(0, 3))] if rngs.random() < 0.45 else SQ[lv], 0.8)

mus = music()
# baisse de la musique quand la voix parle
envv = np.convolve(np.abs(vox[:N]), np.ones(2205) / 2205, mode="same")
duck = 1 - 0.7 * np.clip(envv * 14, 0, 1)
fduck = 1 - 0.45 * np.clip(envv * 14, 0, 1)
mix = mus * duck * 0.7 + fx[:N] * 0.75 * fduck + vox[:N] * 1.6
# fin en fondu
fade = np.clip((DUR - np.arange(N) / SR) / 1.5, 0, 1)
mix *= fade
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix /= max(1e-6, np.abs(mix).max()) / 0.92
st = np.stack([mix, mix], 1)
with wave.open(OUT + "/mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok")
