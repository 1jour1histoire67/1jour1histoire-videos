"""voice.py EP_DIR ['{"1":0.4,"5":0.35}']
Lit EP_DIR/lines.json (liste de phrases), génère la voix Microsoft « Henri » (fr-FR-HenriNeural, +6 %, -2 Hz),
puis écrit EP_DIR/timeline.json (temps de chaque mot) et EP_DIR/voice.wav.
Le 2e argument optionnel donne la pause (s) AVANT certaines lignes (défaut 0.2 s) : mettre 0.3-0.45 aux changements de partie,
0.08 quand une phrase continue la précédente. Affiche la durée totale : viser 61 à 70 s.
Nécessite : pip install edge-tts ; SSL_CERT_FILE=/root/.ccr/ca-bundle.crt ; domaine speech.platform.bing.com autorisé.
"""
import asyncio, json, os, subprocess, sys, wave
import numpy as np
import edge_tts

VOICE, RATE, PITCH = "fr-FR-HenriNeural", "+6%", "-2Hz"
EP = sys.argv[1]
PAUSES = {int(k): v for k, v in json.loads(sys.argv[2]).items()} if len(sys.argv) > 2 else {}
lines = json.load(open(os.path.join(EP, "lines.json")))

async def one(i, text):
    kw = dict(rate=RATE, pitch=PITCH, boundary="WordBoundary")
    if os.environ.get("HTTPS_PROXY"): kw["proxy"] = os.environ["HTTPS_PROXY"]
    c = edge_tts.Communicate(text, VOICE, **kw)
    audio = bytearray(); words = []
    async for ch in c.stream():
        if ch["type"] == "audio": audio += ch["data"]
        elif ch["type"] == "WordBoundary": words.append({"w": ch["text"], "o": ch["offset"] / 1e7, "d": ch["duration"] / 1e7})
    mp3 = os.path.join(EP, f"e_{i:02d}.mp3"); wav = os.path.join(EP, f"seg_{i:02d}.wav")
    open(mp3, "wb").write(audio)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ar", "24000", "-ac", "1", wav], check=True)
    return {"i": i, "text": text, "bw": words}

async def main():
    return [await one(i, t) for i, t in enumerate(lines)]
segs = asyncio.run(main())

A = 0.1; out = []; sr = 24000; prev_end = 0
for o in segs:
    i, bw = o["i"], o["bw"]
    if not bw: sys.exit(f"pas de mots renvoyés pour la ligne {i}")
    if i > 0: A = prev_end + PAUSES.get(i, 0.2) - bw[0]["o"]
    toks = []
    for x in o["text"].split():
        if x in (":", ",", ".") and toks: toks[-1] += (" " + x) if x == ":" else x
        else: toks.append(x)
    use = toks if len(toks) == len(bw) else [b["w"] for b in bw]
    ws = [{"w": use[k], "s": round(A + b["o"], 3), "e": round(A + b["o"] + b["d"], 3)} for k, b in enumerate(bw)]
    out.append({"i": i, "text": o["text"], "s": ws[0]["s"], "e": ws[-1]["e"], "a": round(A, 3), "words": ws})
    prev_end = ws[-1]["e"]
total = round(prev_end + 0.45, 2)
json.dump({"total": total, "lines": out}, open(os.path.join(EP, "timeline.json"), "w"), ensure_ascii=False, indent=1)

buf = np.zeros(int((total + 1) * sr), np.float32)
for L in out:
    with wave.open(os.path.join(EP, f"seg_{L['i']:02d}.wav")) as r:
        a = np.frombuffer(r.readframes(r.getnframes()), np.int16).astype(np.float32) / 32768
    a = a[:int((L["e"] - L["a"] + 0.25) * sr)].copy(); f = int(0.06 * sr); a[-f:] *= np.linspace(1, 0, f)
    s = int(L["a"] * sr); buf[s:s + len(a)] += a
buf = buf[:int(total * sr)]; buf = buf / np.abs(buf).max() * 0.89
with wave.open(os.path.join(EP, "voice.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((buf * 32767).astype(np.int16).tobytes())
print("TOTAL", total, "s")
for L in out: print(L["i"], L["s"], L["e"], " ".join(x["w"] for x in L["words"]))
