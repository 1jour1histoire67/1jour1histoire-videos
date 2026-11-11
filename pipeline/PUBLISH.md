# 1jour1histoire — publication de 10h via Edge (exécution automatique)

But : publier vers 10h00 (Europe/Paris) l'épisode du jour préparé par l'exécution de 6h17, sur les **comptes de la chaîne uniquement**, dans le profil Edge « 1jour1histoire » de Noé, piloté avec les outils Claude in Chrome (`mcp__claude-in-chrome__*`, charger le skill `chrome-browser` d'abord).

Comptes autorisés (et rien d'autre, jamais les comptes perso de Noé) :
- YouTube : chaîne « 1jour1histoire » (ID `UCH1FzaGfLC2x_jAUzU9i5NQ`), via studio.youtube.com
- TikTok : `1jour1histoire676`, via tiktok.com/tiktokstudio
- Instagram : `1jour1histoire67`, via instagram.com
Navigateur : le profil Edge dédié = navigateur connecté `deviceId 1f793a53-2c61-41ee-bd69-3d158ec821c5` (`select_browser`). L'autre navigateur connecté est le profil perso de Noé : **ne jamais l'utiliser**.

## 1. Récupérer le travail du jour
1. `add_repo(owner="1jour1histoire67", repo="1jour1histoire-videos", access="push")`, clone `--depth 1`.
2. Lire `pipeline/a-publier.json`. Si `date` ≠ aujourd'hui ou si les trois plateformes sont déjà `true` dans `published` : ne rien faire et s'arrêter (prévenir Noé si la vidéo du jour manque).
3. Copier le fichier `upload` (vidéo ≤ 10 Mo) dans le dossier de travail de la session (ex. `$HOME/upload.mp4`) : seul un fichier du dossier de travail peut être envoyé à la page.

## 2. Vérifier navigateur et comptes (obligatoire)
1. `list_connected_browsers` → si `1f793a53-2c61-41ee-bd69-3d158ec821c5` n'est pas connecté : le PC est éteint ou Edge fermé → envoyer à Noé (`SendUserMessage`) la vidéo (`SendUserFile`) et le kit de publication (textes de `a-publier.json`) pour qu'il publie lui-même, puis s'arrêter.
2. `select_browser` sur ce deviceId, `tabs_context_mcp` (createIfEmpty), travailler dans un nouvel onglet.
3. Pour chaque plateforme, avant d'importer : lire la page (`get_page_text` / capture) et confirmer le compte affiché (YouTube Studio : « 1jour1histoire » et l'URL contient `UCH1FzaGfLC2x_jAUzU9i5NQ` ; TikTok Studio : `1jour1histoire676` ; Instagram : `instagram.com/accounts/edit/` affiche `1jour1histoire67`). Si ce n'est pas le bon compte : **ne rien publier sur cette plateforme**, ne pas changer de compte soi-même, prévenir Noé.

## 3. Publier (une plateforme après l'autre, cocher dans `published` à chaque réussite)
Règles : ne jamais cliquer sur un champ de fichier (ouvre une fenêtre système invisible) — trouver l'`input type=file` avec `find`/`read_page` puis `file_upload` avec le chemin du dossier de travail. Ne pas toucher aux brouillons existants. Pas de boutons qui déclenchent des alertes navigateur.
- **YouTube** : studio.youtube.com → Créer → Importer des vidéos → `file_upload` → Titre = `youtube.title`, Description = `youtube.description` → « Non, ce n'est pas une vidéo conçue pour les enfants » → Suivant ×3 → Visibilité « Public » → Publier. Attendre la confirmation et relever le lien.
- **TikTok** : tiktok.com/tiktokstudio/upload → `file_upload` sur l'input caché → remplacer la description par `caption` → « Qui peut voir » = Tout le monde → Publier. (Un avertissement « contenu pourrait être restreint » n'empêche pas de publier.)
- **Instagram** : instagram.com → Créer (+) → Publication → `file_upload` → recadrage « Original » / 9:16 → Suivant → Suivant → légende = `caption` → Partager. Confirmer que c'est publié en Reel.
- Si une plateforme bloque après 2-3 essais : passer à la suivante et noter l'échec.

## 4. Après publication
1. Si possible, poster `comment` en commentaire sous chaque publication (Noé l'épinglera).
2. Mettre `published.<plateforme>` à `true` dans `pipeline/a-publier.json`, commit + push (si refusé : `git pull --rebase` puis repousser).
3. Fermer les onglets ouverts.
4. `SendUserMessage` à Noé : où c'est publié (liens), ce qui a échoué éventuellement, rappel d'épingler le commentaire.
