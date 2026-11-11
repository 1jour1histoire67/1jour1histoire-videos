"""Charge le thème courant (dossier THEME_DIR) : theme.json + sprites.py du thème."""
import os, sys, json
THEME_DIR = os.path.abspath(os.environ.get("THEME_DIR", "."))
WORK = os.path.join(THEME_DIR, "work")
os.makedirs(os.path.join(WORK, "voice"), exist_ok=True)
sys.path.insert(0, THEME_DIR)
T = json.load(open(os.path.join(THEME_DIR, "theme.json"), encoding="utf-8"))
