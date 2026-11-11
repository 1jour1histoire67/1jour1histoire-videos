# 1jour1histoire — mode d'emploi de l'épisode quotidien (exécution automatique)

Objectif : chaque jour, produire **un nouvel épisode** « histoire vraie incroyable » (Short vertical 61–70 s) pour une sortie à **10h00 (Europe/Paris)** sur YouTube Shorts, Instagram (Reel) et TikTok. Noé a demandé une production et une publication automatiques : ne pas lui demander de valider, sauf blocage.

**IMPORTANT (11/11/2026) : Noé ne veut plus passer par Metricool. N'utiliser AUCUN outil Metricool.** La publication se fait par les API officielles quand les accès sont configurés (voir étape 7), sinon Noé publie lui-même avec le kit envoyé.

Constantes :
- Comptes : `1jour1histoire67` sur Instagram, TikTok et YouTube. Fuseau `Europe/Paris`.
- Hébergement vidéo + chaîne de montage : dépôt GitHub public **`1jour1histoire67/1jour1histoire-videos`** (dossier `pipeline/`, vidéos dans `videos/`).
- Voix : Microsoft « Henri » via edge-tts (domaine `speech.platform.bing.com` autorisé par Noé).
- Fichiers de la chaîne de montage (documents du projet) : `claude/pipeline/lib_video.py`, `claude/pipeline/voice.py`, `claude/pipeline/setup.sh`, `claude/pipeline/example_episode.py`.
- Liste des épisodes déjà faits : `claude/episodes-publies.md` (à lire pour le numéro N et pour éviter les doublons, à compléter à la fin).
- Règles de format/croissance : `claude/strategie-croissance.md` (durée 61–70 s, sous-titres à y≈74 %, rien d'important dans les 20 % du bas ni à droite, badge « ÉP. N »).

## 1. Installer
Source préférée : le dossier `pipeline/` du dépôt GitHub `1jour1histoire-videos` (copie exacte des fichiers).
1. `list_repos` (query `1jour1histoire-videos`) → `add_repo(owner, repo, access="push")` → cloner comme indiqué, puis `W=$HOME/1j1h; mkdir -p $W; cp -r <clone>/pipeline $W/pipeline`.
2. Secours seulement si le dépôt est introuvable : lire chaque fichier de la chaîne avec `Projects` → `project_read` et l'écrire dans `$W/pipeline/` en recopiant le contenu caractère pour caractère (puis `python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" fichier.py` pour vérifier chaque .py).
Puis :
```
bash $W/pipeline/setup.sh $W/pipeline
export SSL_CERT_FILE=/root/.ccr/ca-bundle.crt PIPELINE=$W/pipeline
```

## 2. Choisir l'histoire (N = dernier numéro de episodes-publies.md + 1)
- Histoire **vraie, vérifiable, surprenante**, avec un retournement fort. Varier époques, pays et thèmes (escroqueries, survivants, inventions, animaux, exploits, coïncidences, erreurs militaires, records…).
- Interdits : sujet déjà dans `episodes-publies.md`, personnes privées vivantes, drames récents (moins de 30 ans), récits très gores, politique actuelle, légendes non prouvées.
- **Vérifier chaque fait** (dates, chiffres, noms, citations) avec `WebSearch` puis `WebFetch` sur au moins 2 sources fiables (encyclopédies, musées, presse reconnue). Un fait non confirmé est retiré ou reformulé (« selon ses mémoires… »). Garder la liste des URL.

## 3. Écrire le script
Créer `$W/epN/lines.json` : liste de 20 à 26 phrases courtes, en français parlé.
- Ligne 0 : l'accroche (le fait le plus fou en une phrase). Ligne 1 : relance (« Et il a recommencé. »).
- Un rebondissement toutes les 8–10 s ; couper les phrases de liaison ; années en chiffres.
- **Dernière ligne = pont de boucle** (« Et dire que, » / « C'est pour ça qu'on raconte encore aujourd'hui que, ») qui s'enchaîne avec la ligne 0.
Puis : `python3 $W/pipeline/voice.py $W/epN '{"1":0.35,"2":0.4}'` (pauses avant certaines lignes). **TOTAL doit être entre 61 et 70 s** : sinon ajouter/retirer un fait vérifié et relancer (supprimer `seg_*.wav e_*.mp3` avant).

## 4. Animer
Copier `example_episode.py` en `$W/epN/episode.py` et le réécrire entièrement pour l'histoire :
- `Episode(EP, title="TITRE COURT EN MAJUSCULES (≤ 22 car.)", badge="ÉP. N")`.
- 10 à 12 scènes qui couvrent 0 → `ep.TOTAL` sans trou ; découpage par lignes (`ep.L(i)`). Dernière scène = image d'ouverture sans textes (boucle).
- Un changement visuel toutes les 1–2 s : `pop_in` (étiquettes `pill`), `stamp_in` (tampons, renvoie le tremblement), `slide_in`, `typed`, cartes, trajets `map_route`, compteurs, silhouettes (`man_layer`, `soldier_layer`, `woman_layer`) et dessins maison simples (formes PIL).
- Synchroniser chaque texte sur le mot prononcé : `ep.wt(ligne, "mot")` (le mot doit exister dans la ligne).
- Zone utile y = 450 → 1300 ; titre en haut (y 230–334) ; sous-titres auto à y 1420 ; rien d'important sous y = 1536 ni collé au bord droit. Pas d'emoji dans les images. Pas de visage réaliste de vraies personnes : silhouettes uniquement.
- Remplir `SFX = dict(stamps=[...], pops=[...], whooshes=[(t, durée)])` avec les instants des tampons/étiquettes.

## 5. Vérifier puis rendre
```
cd $W/epN && python3 episode.py stills <16 à 22 instants aux moments les plus chargés>
```
Regarder **chaque** planche `sheet*.jpg` avec `Read`. Corriger tout chevauchement de textes, élément coupé, écran vide ou illisible, puis revérifier. Ensuite :
```
python3 episode.py render && python3 episode.py sfx && python3 episode.py final EpisodeN_Slug.mp4
ffprobe -v error -show_entries format=duration,size -of compact final/EpisodeN_Slug.mp4
```
Extraire 3 images du MP4 final (ffmpeg -ss) et les regarder avant de publier.

## 6. Héberger sur GitHub
`gh` n'est pas authentifié : passer par git. Dans le clone du dépôt (fait à l'étape 1) :
```
cd <clone> && git fetch -q origin main && git reset -q --hard origin/main
mkdir -p videos && cp $W/epN/final/EpisodeN_Slug.mp4 videos/
git add videos && git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -qm "Ép. N" && git push -q origin main
```
URL publique : `https://raw.githubusercontent.com/1jour1histoire67/1jour1histoire-videos/main/videos/EpisodeN_Slug.mp4`. Vérifier avec `curl -sIL <URL> | grep -iE "^HTTP|content-length"` (200 et bonne taille).

## 7. Publier (sans Metricool)
Préparer les textes :
- **YouTube** — titre « <question/accroche ≤ 70 car.> 😳 Ép. N #shorts » ; description de 3–4 phrases qui résument sans tout dévoiler + « Tu aurais fait quoi ? 👇 » + « Abonne-toi : une histoire vraie incroyable chaque jour. » + 6 hashtags dont #histoirevraie #lesaviezvous #shorts ; non destiné aux enfants.
- **Instagram / TikTok** — légende courte : accroche + « Ép. N » + question + 6 hashtags dont #histoirevraie #pourtoi.
- **Commentaire à épingler** — une question qui fait réagir.
Puis :
- Si le document `claude/secrets/acces-api.md` du projet existe et contient des accès valides : publier par API selon la section « Publication par API » de ce document, à 10h00 (si la plateforme permet la programmation) ou dès que la vidéo est prête après 9h55.
- Sinon (cas actuel) : envoyer à Noé la vidéo (`SendUserFile`) puis un `SendUserMessage` contenant le « kit de publication » prêt à copier-coller (titre YouTube, description, légende Instagram/TikTok, commentaire, instant conseillé pour la miniature) et lui rappeler de publier à 10h.

## 8. Clore
1. Ajouter une ligne à la liste des épisodes : `pipeline/episodes-publies.md` du dépôt (commit + push) ET `claude/episodes-publies.md` du projet (project_read puis project_write du contenu complet) : N, date, sujet, titre YouTube, sources principales.
2. Si ce n'est pas déjà fait à l'étape 7 : envoyer à Noé le MP4 (`SendUserFile`) + un message court (titre, où et quand c'est publié, ou le kit à publier).
3. En cas d'échec à n'importe quelle étape : ne rien publier d'incomplet, expliquer à Noé ce qui a bloqué (`SendUserMessage`).
