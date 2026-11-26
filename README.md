# Site vitrine du Comité de basket de la Gironde (CD33)

Site statique, sans base de données ni cookie, pensé pour GitHub Pages.

## Contenu

Le site est organisé d'après l'audit du site actuel et ses statistiques 2026 : les pages les plus consultées (règlements, championnats jeunes, Coupes 33, détections, championnats seniors, mini-basket, 3x3, licences) sont accessibles en un clic depuis l'accueil, et 63 % des visites se faisant sur mobile, une barre d'accès rapide reste en bas de l'écran sur téléphone.

| Page | Contenu |
| --- | --- |
| `index.html` | Question à l'assistant, 8 accès rapides, prochaines dates, documents les plus téléchargés |
| `competitions.html` | Championnats jeunes et seniors, Coupes 33, 3x3, engagements |
| `joueurs.html` | Détections 2014/2015 par secteur, sélections, camps |
| `mini-basket.html` | Projet 2025-2028, règlements et outils U9/U11 |
| `licences.html` | Tarifs, modes opératoires, surclassement |
| `clubs.html` | Clubs par district, labels, démarches |
| `formations.html` | Arbitres, officiels de table, entraîneurs |
| `comite.html` | Missions, commissions, finances, contact |
| `documents.html` | Tous les documents officiels, avec recherche et filtres |
| `assistant.html` | L'assistant (accepte `?q=` dans l'adresse) |
| `mentions-legales.html` | Mentions légales et confidentialité (passages surlignés à compléter) |
| `sitemap.xml`, `robots.txt` | Référencement (89 % des visites viennent des moteurs de recherche) |
| `assets/` | Styles, scripts, logo, réglage de l'assistant (`config.js`) |
| `data/` | Pages publiques (`kb.json`) et documents officiels (`documents.json`) pour l'assistant et la zone documents |
| `_build/build.py` | Génère toutes les pages : modifier le contenu ici, puis lancer `python3 _build/build.py` |
| `worker/` | Relais IA facultatif (voir plus bas) |

Les données ne contiennent que des informations publiques : pas de coordonnées personnelles, pas de listes de joueurs, pas de CV.

> Si l'adresse finale change (nom de domaine du comité), modifier `BASE_URL` dans `_build/build.py` et relancer le script.

## Mettre le site en ligne avec GitHub Pages

1. Le dépôt doit être **public** (ou un compte GitHub payant pour un dépôt privé).
2. Dans le dépôt : **Settings → Pages → Source : Deploy from a branch → Branch : `main`, dossier `/ (root)`**.
3. Le site est disponible quelques minutes plus tard à l'adresse indiquée sur cette page.
4. Pour un nom de domaine du comité (par exemple `www.basket33.fr`), le renseigner dans **Custom domain** et ajouter l'enregistrement DNS indiqué par GitHub.

## L'assistant

- **Mode recherche (par défaut, gratuit)** : l'assistant cherche dans les pages et documents et affiche les passages les plus pertinents avec leur source. Tout se passe dans le navigateur du visiteur.
- **Mode IA (facultatif)** : l'assistant rédige une vraie réponse avec Claude. Il faut :
  1. un compte sur console.anthropic.com au nom du comité et une clé API (paiement à l'usage) ;
  2. un compte Cloudflare gratuit, créer un Worker avec le code de `worker/worker.js` ;
  3. dans le Worker, définir les variables `ANTHROPIC_API_KEY` (en secret) et `ALLOWED_ORIGIN` (l'adresse du site, ex. `https://mrodier.github.io`) ;
  4. coller l'adresse du Worker dans `assets/config.js` (`assistantEndpoint`).
  La clé API ne doit **jamais** être mise dans les fichiers du site. Compléter alors la mention correspondante dans `mentions-legales.html`.

## Mettre à jour

- **Un document** : modifier `data/documents.json` (titre `t`, lien `u`, catégorie `cat`).
- **Le contenu des pages** : modifier le texte dans `_build/build.py`, puis lancer `python3 _build/build.py`.
- **Le carrousel de l'accueil** : les visuels sont dans `assets/carrousel/` (format 16:9, 1600 × 900). Pour mettre une affiche ou une photo, déposer l'image dans ce dossier puis modifier la liste `SLIDES` dans `_build/build.py` (image, texte alternatif, lien) et relancer le script.
- **Les couleurs** : modifier les variables en haut de `assets/style.css`.
