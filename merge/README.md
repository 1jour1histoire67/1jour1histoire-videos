# MERGE — générateur de Shorts « jeu de fusion » (chaîne 1jour1histoire)

- `engine/` : moteur commun (physique pymunk, rendu PIL, voix espeak-ng/mbrola, bruitages synthétisés, mixage).
- `themes/NN-slug/` : un épisode = `theme.json` (textes, couleurs, voix, musique, bruitages, publication) + `sprites.py` (dessins).
- `python3 engine/run_episode.py themes/NN-slug` → `themes/NN-slug/<slug>.mp4` (62 s, 1080×1920, −13 LUFS).
- `PLAYBOOK.md` : procédure complète de la tâche quotidienne automatique (fabrication + publication Metricool).
- `BACKLOG.md` : thèmes à venir · `history.json` : épisodes déjà faits.
