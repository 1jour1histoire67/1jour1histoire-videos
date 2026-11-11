"""Fabrique un épisode complet : python3 run_episode.py <dossier_du_thème>
Sortie : <thème>/<slug>.mp4 + <thème>/work/contact.jpg (planche de contrôle)."""
import os, sys, json, subprocess, time
from multiprocessing import Pool

ENGINE = os.path.dirname(os.path.abspath(__file__))
THEME_DIR = os.path.abspath(sys.argv[1])
os.environ["THEME_DIR"] = THEME_DIR
sys.path.insert(0, ENGINE)
from theme import T, WORK  # noqa
from sim import run, TARGETS  # noqa


def job(a):
    s, de = a
    fr, ev, ut = run(s, de, verbose=False, bomb_t=39.0)
    if ut is None:
        return None
    rv = {e[2]: e[0] for e in ev if e[1] == "reveal"}
    err = sum((rv.get(k, 99) - v) ** 2 for k, v in TARGETS.items())
    return (err, s, de, ut)


def sh(cmd):
    print("+", " ".join(cmd) if isinstance(cmd, list) else cmd, flush=True)
    subprocess.run(cmd, check=True, cwd=ENGINE, env=os.environ, shell=isinstance(cmd, str))


if __name__ == "__main__":
    t0 = time.time()
    a, b = T.get("seed_range", [1, 30])
    args = [(s, de) for s in range(a, b) for de in (0.30, 0.34)]
    with Pool(max(1, os.cpu_count() - 1)) as p:
        res = [r for r in p.imap_unordered(job, args) if r and 50 <= r[3] <= 56]
    if not res:
        sys.exit("Aucune partie avec le final entre 50 et 56 s : élargir seed_range")
    err, seed, de, ut = sorted(res)[0]
    print(f"partie retenue : seed={seed} drop={de} final={ut:.1f}s err={err:.0f}", flush=True)
    fr, ev, ut = run(seed, de, verbose=True, bomb_t=39.0)
    json.dump({"frames": fr, "events": ev, "ut": ut}, open(os.path.join(WORK, "simdata.json"), "w"))
    sh([sys.executable, "audio.py"])
    boom = next(e[0] for e in ev if e[1] == "boom")
    keys = [0.0, 0.6, 8.0, 25.0, boom - 1.5, boom + 0.3, ut + 3.0, 61.8]
    sh([sys.executable, "render.py", "still"] + [f"{k:.1f}" for k in keys])
    from PIL import Image
    ims = [Image.open(os.path.join(WORK, f"still_{k:05.1f}.png")).resize((270, 480)) for k in keys]
    cs = Image.new("RGB", (270 * len(ims), 480))
    for i, im in enumerate(ims):
        cs.paste(im, (270 * i, 0))
    cs.save(os.path.join(WORK, "contact.jpg"), quality=85)
    # rendu vidéo en 2 moitiés parallèles
    pa = subprocess.Popen([sys.executable, "render.py", "enc", "0", "930", os.path.join(WORK, "a.mp4")], cwd=ENGINE, env=os.environ)
    pb = subprocess.Popen([sys.executable, "render.py", "enc", "930", "1860", os.path.join(WORK, "b.mp4")], cwd=ENGINE, env=os.environ)
    assert pa.wait() == 0 and pb.wait() == 0, "rendu vidéo échoué"
    lst = os.path.join(WORK, "list.txt")
    open(lst, "w").write(f"file '{WORK}/a.mp4'\nfile '{WORK}/b.mp4'\n")
    vid = os.path.join(WORK, "video.mp4")
    out = os.path.join(THEME_DIR, T["slug"] + ".mp4")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid])
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", os.path.join(WORK, "mix.wav"), "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-af", "loudnorm=I=-13:TP=-1.0:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", out])
    # copie « web » < 10 Mo pour l'import via l'extension Claude du navigateur
    web = os.path.join(THEME_DIR, T["slug"] + "_web.mp4")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-c:v", "libx264", "-preset", "medium", "-b:v", "1050k", "-pass", "1",
        "-passlogfile", os.path.join(WORK, "p"), "-an", "-f", "mp4", "/dev/null"])
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-c:v", "libx264", "-preset", "medium", "-b:v", "1050k", "-pass", "2",
        "-passlogfile", os.path.join(WORK, "p"), "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", web])
    assert os.path.getsize(web) < 10_000_000, "copie web trop lourde (> 10 Mo)"
    print("OK", out, web, f"{os.path.getsize(web) / 1e6:.1f} Mo", f"{time.time() - t0:.0f}s", flush=True)
