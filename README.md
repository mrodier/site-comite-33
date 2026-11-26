# Site vitrine du Comité de basket de la Gironde (CD33)

Site statique, sans base de données ni cookie, pensé pour GitHub Pages.

## Contenu

| Fichier | Rôle |
| --- | --- |
| `index.html` | La page du site : accueil, comité, pratiquer, compétitions, se former, clubs, assistant, documents, contact |
| `mentions-legales.html` | Mentions légales et confidentialité (passages surlignés à compléter avant la mise en ligne) |
| `assets/style.css` | Mise en forme (couleurs dans le bloc `:root` en haut du fichier) |
| `assets/app.js` | Menu, liste des clubs, zone documents et assistant |
| `assets/config.js` | Réglage de l'assistant (mode recherche ou relais IA) |
| `data/kb.json` | Contenu des pages publiques du site girondebasket.com (relevé du 24/11/2026) |
| `data/documents.json` | Liste et texte des documents officiels (règlements, dispositions financières, calendrier…) |
| `worker/` | Relais IA facultatif, à déployer sur Cloudflare (voir plus bas) |

Les données ne contiennent que des informations publiques : pas de coordonnées personnelles, pas de listes de joueurs, pas de CV.

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
- **Le contenu des pages** : modifier le texte dans `index.html`.
- **Les couleurs** : modifier les variables en haut de `assets/style.css`.
