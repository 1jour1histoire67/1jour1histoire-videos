# MERGE quotidien — mode d'emploi de la tâche automatique

Objectif : chaque jour, fabriquer **un nouvel épisode** de la série MERGE (jeu de fusion brainrot) et le **publier vers 15:00 (Europe/Paris)** en Reel Instagram, sur TikTok et en Short YouTube, **uniquement sur les comptes de la chaîne**. Le tout sans aide humaine. Noé a choisi le mode **100 % automatique** : on ne lui demande pas de valider. On le prévient seulement à la fin, ou si quelque chose casse.

**Plus de Metricool** (offre gratuite épuisée) : la publication passe par le navigateur dédié de Noé, piloté avec les outils Claude in Chrome (`mcp__claude-in-chrome__*` ; charger d'abord le skill `chrome-browser`). La méthode est la même que pour la série histoire (`pipeline/PUBLISH.md`).

Comptes autorisés, et rien d'autre (jamais les comptes perso de Noé) :
- YouTube : chaîne « 1jour1histoire », ID `UCH1FzaGfLC2x_jAUzU9i5NQ` (studio.youtube.com)
- TikTok : `@1jour1histoire676` (tiktok.com/tiktokstudio)
- Instagram : `1jour1histoire67`
- Navigateur : navigateur connecté `deviceId 1f793a53-2c61-41ee-bd69-3d158ec821c5` (`select_browser`). L'autre navigateur connecté est le profil perso de Noé : **ne jamais l'utiliser**.

## 0. Installation (environnement neuf à chaque fois)
```bash
# add_repo(owner="1jour1histoire67", repo="1jour1histoire-videos", access="push"), puis :
git clone --depth 1 https://github.com/1jour1histoire67/1jour1histoire-videos repo && cd repo/merge
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

## 4. Préparer le fichier à importer
- `run_episode.py` produit aussi `themes/NN-slug/<slug>_web.mp4`, une copie de moins de 10 Mo (limite de l'extension).
- **La copier dans le dossier de travail de la session** : `cp themes/NN-slug/<slug>_web.mp4 $HOME/upload_merge.mp4`. L'extension refuse les fichiers de `/mnt/user-data/outputs/`. Seul le dossier de travail (`$HOME`) fonctionne.

## 5. Publier via le navigateur dédié (une plateforme après l'autre)
1. `list_connected_browsers`. Si `1f793a53-2c61-41ee-bd69-3d158ec821c5` n'est pas connecté (PC éteint ou navigateur fermé) : ne rien publier. Envoyer à Noé la vidéo (`SendUserFile`) et les textes (`SendUserMessage`), puis s'arrêter.
2. `select_browser` sur ce deviceId, puis `tabs_context_mcp`, puis **ouvrir un nouvel onglet**. Ne jamais toucher aux onglets existants : la série histoire peut en utiliser un.
3. **Vérifier le compte avant chaque plateforme**. YouTube Studio : `#entity-name` = « 1jour1histoire » et l'URL contient `UCH1FzaGfLC2x_jAUzU9i5NQ`. TikTok Studio, page `/tiktokstudio/content` : les liens `/@1jour1histoire676`. Instagram, page `/accounts/edit/` : le lien `/1jour1histoire67/`. Si le compte n'est pas le bon, ne rien publier sur cette plateforme et prévenir Noé.
4. Ne jamais cliquer sur un champ de fichier. Trouver l'`input type=file` avec `find` (« file input ») puis utiliser `file_upload` avec `$HOME/upload_merge.mp4`.
- **YouTube** : ouvrir `https://studio.youtube.com/channel/UCH1FzaGfLC2x_jAUzU9i5NQ/videos/upload?d=ud`, puis `file_upload` sur l'input `Filedata`. Remplir le titre et la description en JavaScript dans `ytcp-uploads-dialog` : `#textbox[0]` = `post.title + " #shorts"`, `#textbox[1]` = `post.caption`. Pour chacun : `el.focus(); document.execCommand('selectAll'); document.execCommand('insertText', false, txt)`. Cliquer `tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]`, puis 3 fois `#next-button`, puis `tp-yt-paper-radio-button[name="PUBLIC"]`, puis `#done-button`. Relever le lien `youtube.com/shorts/...` dans la fenêtre de confirmation.
- **TikTok** : ouvrir `https://www.tiktok.com/tiktokstudio/upload`, puis `file_upload`. Ne pas toucher au bandeau « vidéo non enregistrée… Supprimer / Continuer ». Pour la description : clic sur la zone de texte, `ctrl+a`, `Delete`, taper le texte, puis chaque hashtag suivi d'une espace avec 1 s d'attente entre chaque. **Ne jamais remplir l'éditeur avec execCommand** : la page plante. Garder « Maintenant » et « Tout le monde », puis cliquer sur le bouton « Publier ». Dans la liste, la vidéo apparaît « en cours d'examen / Moi uniquement » quelques minutes : c'est normal.
- **Instagram** : sur `instagram.com`, cliquer sur le lien « Nouvelle publication Créer », puis « Publication ». Faire `file_upload`. Ouvrir le recadrage (icône en bas à gauche de l'aperçu) et choisir « Original ». Cliquer 2 fois sur « Suivant ». Écrire la légende (clic puis taper `post.caption`). Le bouton « Ajouter une mention IA » doit rester désactivé. Cliquer sur « Partager » et attendre « Votre reel a été partagé ».
- Si une plateforme bloque après 2 ou 3 essais : passer à la suivante et noter l'échec.
5. Fermer les onglets ouverts par la tâche.

## 6. Garder la trace
- Ajouter l'épisode dans `history.json` : numéro, slug, date, thème, pattern, couleur de base, voix, seed_range, lien YouTube, et l'état TikTok et Instagram.
- Cocher le thème dans `BACKLOG.md`.
- `git add themes/NN-slug/theme.json themes/NN-slug/sprites.py history.json BACKLOG.md && git commit && git push`. Ne pas committer `work/` ni les mp4 : ils sont dans `.gitignore`. Si le push est refusé : `git pull --rebase origin main`, puis repousser. Le dépôt est partagé avec la série histoire.

## 7. Prévenir Noé (SendUserMessage)
Une ou deux lignes : épisode N, thème, liens et état sur les 3 plateformes. En cas d'échec avant la publication, **ne rien publier**. Envoyer un message qui dit ce qui a échoué. Si la vidéo est prête mais que le navigateur est absent, joindre la vidéo et les textes pour que Noé publie lui-même.

## Règles de contenu (toujours)
- **Aucune personne réelle** (politicien, célébrité, influenceur), ni en caricature ni en fausse voix. Pas de personnage, de marque ou de mème protégé (Skibidi, Pokémon, Mario, logos…). Tout doit être inventé.
- Humour bon enfant, qui ne vise ni une origine, ni une religion, ni un handicap, etc. Pas de violence réaliste : le rebondissement reste un gag de dessin animé.
- Chaque épisode doit vraiment changer : thème, personnages, couleurs, motif, voix, musique, rebondissement. YouTube refuse de monétiser le contenu « produit en série avec un template ».
- Toujours **61 à 63 s** (le Creator Rewards de TikTok exige plus d'une minute), un commentateur qui parle en continu, des sous-titres et des bruitages.
