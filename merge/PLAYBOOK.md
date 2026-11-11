# MERGE quotidien — mode d'emploi de la tâche automatique

Objectif : chaque jour, fabriquer **un nouvel épisode** de la série MERGE (jeu de fusion brainrot, chaîne 1jour1histoire) et le programmer dans Metricool à **15:00 (Europe/Paris)** sur Instagram (Reel), TikTok et YouTube (Short). Le tout sans aide humaine. Noé a choisi le mode **100 % automatique** : on ne lui demande pas de valider. On le prévient seulement à la fin, ou si quelque chose casse.

## 0. Installation (environnement neuf à chaque fois)
```bash
git clone https://github.com/<OWNER>/<REPO>.git merge && cd merge
pip install --break-system-packages -q pymunk
apt-get update -q && apt-get install -y -q espeak-ng mbrola mbrola-fr1 mbrola-fr4 sox ffmpeg
ls /usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf   # police utilisée par le rendu
```
Si la police manque, installer Poppins depuis le dépôt `google/fonts` (GitHub), ou mettre une autre police grasse dans `engine/render.py` (FONT) et dans le `sprites.py` du thème.

## 1. Choisir le thème
- Lire `history.json` pour trouver le numéro d'épisode suivant N et les thèmes, couleurs, motifs et voix des 3 derniers épisodes.
- Prendre le premier thème « à faire » de `BACKLOG.md`. Si la liste est vide, inventer un nouveau thème qui respecte les règles ci-dessous et l'ajouter à la liste.

## 2. Créer `themes/NN-slug/`
Prendre `themes/05-ferme/` comme modèle.
- **`theme.json`** : tous les textes (accroche, rebondissement, final, vannes `extra` pour les niveaux 2 à 6, 14 phrases de relance `fill`), les couleurs, le motif, la voix, la musique, les bruitages et les champs de publication. Règles de variation :
  - `pattern` différent de l'épisode précédent. Choix possibles : `stripes`, `rays`, `spiral`, `dots`, `checker`.
  - Palette nettement différente des 3 derniers épisodes. Le fond doit rester **clair et coloré** : un fond sombre fait swiper dès la 1re seconde (épisode 3 : 4,5 s de visionnage moyen ; épisode 5, fond clair : 8 s).
  - `voice.engine` : alterner `mb-fr1` (voix d'homme) et `mb-fr4` (voix de femme). `pitch` entre 55 et 70, `speed` entre 165 et 180.
  - `music` : un `bpm` et des accords différents de l'épisode précédent.
  - `sfx_reveal` : un bruitage marquant par nouveau niveau. Fonctions disponibles dans `engine/audio.py` : `vine_boom`, `airhorn`, `airhorn3`, `squeak:<hauteur>`, `record_scratch`, `slide_whistle:1` (montée) ou `slide_whistle:0` (descente), `clown_honk`, `fart`, `drumroll`, `crash`, `cheer`, `howl`, `dun_dun_dun`, `sad_trombone`, `pew`, `ding`, `boom`.
  - `seed_range` : une plage de 12 graines jamais utilisée (voir `history.json`).
  - `final_intro` : « TU AS CRÉÉ LE » ou « TU AS CRÉÉ LA » selon le genre du nom final.
  - `say_replace` : corrections de prononciation pour espeak (sigles, mots anglais…).
- **`sprites.py`** : `LEVELS` (8 niveaux : nom affiché, nom prononcé, rayon), `BOMB_R`, `make_sprite(level)`, `make_bomb()` (le personnage du rebondissement), `silhouette()` et `build_all()`.
  - Rayons conseillés : 24, 36, 50, 64, 80, 98, 120, 150. Les niveaux 0 à 3 doivent passer dans l'entonnoir (rayon < 85).
  - Style kawaii, avec un contour épais. Les fonctions `gradient_fill`, `draw_body`, `draw_face`, `star` et `blob_points` sont dans `engine/sprites_base.py`.
  - Lancer `cd themes/NN-slug && PYTHONPATH=../../engine python3 sprites.py` (qui écrit `sheet.png`), **regarder l'image**, et corriger jusqu'à ce que chaque personnage soit lisible et reconnaissable à petite taille.

## 3. Fabriquer la vidéo
```bash
cd engine && python3 run_episode.py ../themes/NN-slug     # environ 4 minutes
```
- **Regarder `themes/NN-slug/work/contact.jpg`** (8 images clés). Vérifier :
  - Image 0 : fond clair, « DEVINE LE … » bien lisible, arène déjà pleine.
  - Les personnages sont droits et reconnaissables.
  - Aucun texte ne déborde de l'écran.
  - Le rebondissement et le final sont bien visibles.
- Corriger puis relancer si besoin.
- Contrôles automatiques : durée = 62 s, et loudness ≈ −13 LUFS (`ffmpeg -i X.mp4 -af ebur128=framelog=quiet -f null -`).

## 4. Mettre la vidéo en ligne (lien public pour Metricool)
```bash
gh release create ep-NN themes/NN-slug/<slug>.mp4 --title "Épisode NN" --notes "MERGE épisode NN"
```
URL à donner à Metricool : `https://github.com/<OWNER>/<REPO>/releases/download/ep-NN/<slug>.mp4`

## 5. Programmer dans Metricool
- Marque `blogId = 7944960` (« 1jour1histoire67 », reliée à Instagram, TikTok et YouTube). Fuseau horaire : Europe/Paris.
- Date : **aujourd'hui à 15:00**. S'il est déjà plus de 14:30, programmer le lendemain à 15:00 et le signaler.
- Avant de programmer, appeler `getScheduledPosts` pour ce jour-là : aucun autre post MERGE ne doit déjà être prévu. Les séries « histoire » (10:00) et « foot » (soir) ne gênent pas.
- Gabarit `info` (remplacer les champs entre chevrons) :
```json
{"autoPublish": true, "draft": false, "descendants": [], "firstCommentText": "", "hasNotReadNotes": false,
 "media": ["<URL release>"], "mediaAltText": [],
 "providers": [{"network": "instagram"}, {"network": "tiktok"}, {"network": "youtube"}],
 "publicationDate": {"dateTime": "<YYYY-MM-DD>T15:00:00", "timezone": "Europe/Paris"},
 "shortener": false, "smartLinkData": {"ids": []},
 "text": "<post.caption>",
 "instagramData": {"type": "REEL", "showReelOnFeed": true},
 "tiktokData": {"title": "<post.title>", "privacyOption": "PUBLIC_TO_EVERYONE", "disableComment": false, "disableDuet": false, "disableStitch": false, "autoAddMusic": false},
 "youtubeData": {"title": "<post.title> #shorts", "type": "short", "privacy": "public", "madeForKids": false, "category": "<post.youtube_category>", "tags": <post.tags>}}
```
- `tiktokData.title` est **obligatoire**. Les liens Google Drive `/view` ne marchent pas, ceux de GitHub oui.
- Légende : une question, puis « Ton préféré ? Commente 1 à 8 👇 », puis 3 à 5 hashtags (thème + `#jeudefusion #brainrot`). Titre : « J'ai créé le/la [FINAL] [emoji] ».

## 6. Garder la trace
- Ajouter l'épisode dans `history.json` : numéro, slug, date, thème, pattern, couleur de base, voix, seed_range, URL de la release, id du post Metricool.
- Cocher le thème dans `BACKLOG.md`.
- `git add themes/NN-slug/theme.json themes/NN-slug/sprites.py history.json BACKLOG.md && git commit && git push`. Ne pas committer `work/` ni les mp4 : ils sont dans `.gitignore`.

## 7. Prévenir Noé (SendUserMessage)
Une ligne : épisode N, thème, heure de publication, lien vers le post Metricool. En cas d'échec à n'importe quelle étape, **ne rien programmer** : envoyer un message qui dit ce qui a échoué.

## Règles de contenu (toujours)
- **Aucune personne réelle** (politicien, célébrité, influenceur), ni en caricature ni en fausse voix. Pas de personnage, de marque ou de mème protégé (Skibidi, Pokémon, Mario, logos…). Tout doit être inventé.
- Humour bon enfant, qui ne vise ni une origine, ni une religion, ni un handicap, etc. Pas de violence réaliste : le rebondissement reste un gag de dessin animé.
- Chaque épisode doit vraiment changer : thème, personnages, couleurs, motif, voix, musique, rebondissement. YouTube refuse de monétiser le contenu « produit en série avec un template ».
- Toujours **61 à 63 s** (le Creator Rewards de TikTok exige plus d'une minute), un commentateur qui parle en continu, des sous-titres et des bruitages.
