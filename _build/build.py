"""Génère les pages HTML du site à partir d'un gabarit commun.
Usage : python3 _build/build.py   (depuis la racine du dépôt)
Modifier le contenu dans PAGES ci-dessous, puis relancer le script et pousser les fichiers produits."""
import os, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://mrodier.github.io/site-comite-33/"
MAJ = "26/11/2026"
GP = "https://girondebasket.com/wp-content/uploads/"

NAV = [
    ("competitions", "Compétitions"), ("joueurs", "Joueurs"), ("mini-basket", "Mini-basket"),
    ("licences", "Licences"), ("clubs", "Clubs"), ("formations", "Se former"),
    ("comite", "Le comité"), ("documents", "Documents"),
]

def doc(label, url, meta=""):
    m = f'<span class="doc-cat">{meta}</span>' if meta else ""
    return f'<a class="doc" href="{url}" target="_blank" rel="noopener"><span class="doc-title">{label}</span>{m}<span class="doc-open">Ouvrir ↗</span></a>'

def page(slug, title, desc, kicker, h1, lead, body, wide_head=False):
    nav = "".join(
        f'<a href="{s}.html"{" aria-current=\"page\"" if s == slug else ""}>{l}</a>' for s, l in NAV)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} · Comité de basket de la Gironde</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE_URL}{'' if slug == 'index' else slug + '.html'}">
<link rel="icon" href="assets/ballon-33.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/style.css">
</head>
<body class="p-{slug}">
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="topbar" id="topbar">
  <div class="container topbar-inner">
    <a class="brand" href="index.html" aria-label="Comité de basket de la Gironde, accueil">
      <img src="assets/ballon-33.svg" alt="" width="34" height="36"><span>Gironde <em>Basket</em></span>
    </a>
    <button type="button" class="menu-toggle" id="menu-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Sommaire">{nav}<a href="assistant.html" class="nav-cta"{' aria-current="page"' if slug == 'assistant' else ''}>Une question ?</a></nav>
  </div>
</header>
<main id="contenu">
{hero(slug, kicker, h1, lead)}
{body}
</main>
{FOOTER}
<nav class="mobilebar" aria-label="Accès rapide mobile">
  <a href="index.html"{' aria-current="page"' if slug == 'index' else ''}><span aria-hidden="true">⌂</span>Accueil</a>
  <a href="competitions.html"{' aria-current="page"' if slug == 'competitions' else ''}><span aria-hidden="true">◎</span>Compétitions</a>
  <a href="documents.html"{' aria-current="page"' if slug == 'documents' else ''}><span aria-hidden="true">▤</span>Documents</a>
  <a href="assistant.html"{' aria-current="page"' if slug == 'assistant' else ''}><span aria-hidden="true">?</span>Question</a>
</nav>
<script src="assets/config.js"></script>
<script src="assets/app.js"></script>
</body>
</html>
"""

COURT = '<svg class="court" viewBox="0 0 1440 520" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><line x1="1010" y1="0" x2="1010" y2="520"/><circle cx="1010" cy="260" r="100"/><circle cx="1010" cy="260" r="34"/><path d="M1442 40 L1290 40 A220 220 0 0 0 1290 480 L1442 480"/><rect x="1250" y="180" width="192" height="160"/></svg>'

def hero(slug, kicker, h1, lead):
    if slug == "index":
        return ""
    return f"""<section class="phead">{COURT}
  <div class="container phead-inner">
    <p class="crumbs"><a href="index.html">Accueil</a> / {kicker}</p>
    <h1>{h1}</h1>
    {f'<p class="lead">{lead}</p>' if lead else ''}
    <p class="updated">Mis à jour le {MAJ}</p>
  </div>
</section>"""

FOOTER = """<footer class="footer">
  <div class="container footer-inner">
    <img src="assets/logo.svg" alt="Gironde Basketball" width="64" height="92">
    <div class="footer-id">
      <p><strong>Comité départemental de basket-ball de la Gironde</strong></p>
      <p class="muted">4 allée Annie Fratellini, 33140 Villenave d'Ornon · <a href="mailto:secretariat@basket33.fr">secretariat@basket33.fr</a> · <a href="tel:+33619863771">06 19 86 37 71</a></p>
    </div>
    <ul class="footer-links">
      <li><a href="https://www.facebook.com/Cd33Basket" rel="noopener">Facebook</a></li>
      <li><a href="https://www.instagram.com/girondebasket" rel="noopener">Instagram</a></li>
      <li><a href="https://www.youtube.com/@comitedegirondedebasketbal7366" rel="noopener">YouTube</a></li>
      <li><a href="mentions-legales.html">Mentions légales et confidentialité</a></li>
    </ul>
  </div>
</footer>"""

def section(id_, kicker, title, inner, alt=False, lead=""):
    return f"""<section class="section{' alt' if alt else ''}" id="{id_}">
  <div class="container">
    <div class="section-head"><p class="kicker">{kicker}</p><h2>{title}</h2>{f'<p class="section-lead">{lead}</p>' if lead else ''}</div>
    {inner}
  </div>
</section>"""

def rows(items):
    return '<div class="rows">' + "".join(f'<div class="row"><h3>{h}</h3><div>{t}</div></div>' for h, t in items) + "</div>"

def docs(items):
    return '<div class="doc-list">' + "".join(doc(*i) for i in items) + "</div>"

# ---------------------------------------------------------------- Accueil
QUICK = [  # classés selon les pages les plus vues en 2026 (statistiques WordPress)
    ("documents.html#reglements", "Règlements", "Règlements sportifs, jeunes, pré-région, 3x3"),
    ("competitions.html#jeunes", "Championnats jeunes", "U13 à U21, calendrier, phases finales"),
    ("competitions.html#coupes", "Coupes 33", "Seniors et jeunes, notices et finales"),
    ("joueurs.html", "Détections et sélections", "Génération 2014/2015, dates et lieux"),
    ("competitions.html#seniors", "Championnats seniors", "Pré-région et départementales"),
    ("mini-basket.html", "Mini-basket", "U7, U9, U11 : règlements et outils"),
    ("competitions.html#trois", "3x3", "Stops 2026-2027 et inscription"),
    ("licences.html", "Licences et tarifs", "Tarifs, modes opératoires, surclassement"),
]
TOPDOCS = [  # les plus téléchargés en 2026
    ("Cahier des charges des phases finales championnats (06/02/2026)", GP + "2026/02/2026_02_06-cahier_charges-chpt.pdf", "Compétitions"),
    ("Cahier des charges des phases finales des Coupes 33 (06/02/2026)", GP + "2026/02/2026_02_06-cahier_charges-_coupes.pdf", "Compétitions"),
    ("Statuts du comité (24/06/2023)", GP + "2024/01/2023-06-24-statuts-cd33.pdf", "Le comité"),
    ("Règlement sportif particulier des championnats jeunes 2026-2027", "https://docs.google.com/document/d/1Cj-tsL1w77xI0HiB4HxjuI6cfWdVFXMK/edit", "Règlements"),
    ("Mode opératoire engagements FBI (30/06/2026)", GP + "2026/06/2026_06_30_mode_operatoire_engagements-fbi.pdf", "Compétitions"),
    ("Fiche rencontre U9 / U9-U11 championnat", GP + "2025/11/fiche-rencontre-u9u9championnatu11.pdf", "Mini-basket"),
]
home_body = f"""<section class="hero">{COURT}
  <div class="container hero-inner">
    <div>
      <p class="eyebrow">Comité départemental de basket-ball · Saison 2026-2027</p>
      <h1>Le basket<br>en <em>Gironde</em></h1>
      <form class="ask hero-ask" action="assistant.html" method="get" role="search">
        <label for="home-q" class="sr">Votre question</label>
        <input id="home-q" name="q" type="search" placeholder="Une question ? Ex. : tarif licence U13" autocomplete="off" required>
        <button type="submit" class="btn btn-primary">Demander</button>
      </form>
    </div>
    <img class="hero-logo" src="assets/ballon-33.svg" alt="" width="280" height="300">
  </div>
</section>
<section class="quick" aria-labelledby="quick-title">
  <div class="container">
    <h2 id="quick-title" class="sr">Accès rapides</h2>
    <div class="quick-grid">{''.join(f'<a class="qtile" href="{h}"><span class="qtile-t">{t}</span><span class="qtile-d">{d}</span><span class="qtile-a" aria-hidden="true">→</span></a>' for h, t, d in QUICK)}</div>
  </div>
</section>
{section("agenda", "Cette saison", "Les prochaines dates", rows([
    ("Détections 2014/2015", "Novembre et décembre 2026 dans les quatre secteurs. <a href='joueurs.html'>Dates et lieux</a>."),
    ("3x3 · Stop 2", "19 et 20 décembre 2026, Halle des sports de Talence. <a href='competitions.html#trois'>Tous les stops</a>."),
    ("3x3 · Stops 3 et 4", "Du 22 au 25 février 2027, puis du 19 au 22 avril 2027, à Talence."),
    ("Finales des Coupes 33", "Samedi 12 juin 2027, toutes catégories. <a href='competitions.html#coupes'>Les Coupes 33</a>."),
]) + '<p class="note">Calendrier général 2026-2027 provisoire : <a href="https://drive.google.com/file/d/1ml0u5hERsjXXAmbd_6r5MFnAS_rRXM9-/view" target="_blank" rel="noopener">le consulter</a>.</p>')}
{section("top-docs", "Documents", "Les plus téléchargés", docs(TOPDOCS) + '<p class="note"><a href="documents.html">Tous les documents officiels →</a></p>', alt=True)}
{section("nous", "Le comité", "Au service des clubs girondins", '''<div class="split-2">
  <p class="big">Le CD33 organise et développe le basket en Gironde : compétitions départementales et pré-régionales, soutien aux clubs, formation des joueurs, entraîneurs, arbitres, officiels de table et dirigeants.</p>
  <ul class="facts-light"><li><strong>6</strong><span>districts</span></li><li><strong>5</strong><span>salariés</span></li><li><strong>50+</strong><span>bénévoles</span></li></ul>
</div><p class="note"><a href="comite.html">Le comité, ses commissions et son équipe →</a> · <a href="clubs.html">Trouver un club →</a></p>''')}
"""

# ---------------------------------------------------------------- Compétitions
STOPS = [
    ("Stop 1", "Salle omnisport de Rocquencourt, Pessac", "26/10 U13M · 27/10 U13-U15-U18 F · 28/10 U15M · 29/10 U18M (2026)"),
    ("Stop 2", "Halle des sports, Talence", "19/12 U13F et U13M (9h30-12h30), U15F et U18F (14h-17h) · 20/12 U15M (9h30-12h30), U18M (14h-17h)"),
    ("Stop 3", "Halle des sports, Talence", "22/02 U13M · 23/02 U15M · 24/02 U18M · 25/02 U13-U15-U18 F (2027)"),
    ("Stop 4", "Halle des sports, Talence", "19/04 U13M · 20/04 U15M · 21/04 U18M · 22/04 U13-U15-U18 F (2027)"),
]
comp_body = (
    '<nav class="subnav container" aria-label="Dans cette page"><a href="#jeunes">Jeunes</a><a href="#seniors">Seniors</a><a href="#coupes">Coupes 33</a><a href="#trois">3x3</a><a href="#engager">Engager ses équipes</a></nav>'
    + section("jeunes", "Championnats jeunes", "U13 à U21", rows([
        ("Catégories", "U13F, U15F, U18F · U13M, U15M, U18M, U21M."),
        ("Listes de brûlés", "À remplir par formulaire, une par catégorie, transmis automatiquement à la commission sportive."),
        ("Phases finales", "Organisation encadrée par le cahier des charges des phases finales jeunes et seniors."),
    ]) + docs([
        ("Calendrier sportif 2026-2027 (provisoire)", "https://drive.google.com/file/d/1ml0u5hERsjXXAmbd_6r5MFnAS_rRXM9-/view", "Calendrier"),
        ("Règlement sportif particulier des championnats jeunes", "https://docs.google.com/document/d/1Cj-tsL1w77xI0HiB4HxjuI6cfWdVFXMK/edit", "Règlement"),
        ("Règlement de la pré-région jeunes", "https://drive.google.com/file/d/1uodrxuyqmTCb6Rs1ggJmeiIPpnxyNhlx/view", "Règlement"),
        ("Cahier des charges des phases finales (06/02/2026)", GP + "2026/02/2026_02_06-cahier_charges-chpt.pdf", "Phases finales"),
    ]))
    + section("seniors", "Championnats seniors", "Pré-région et départementales", rows([
        ("Engagements", "Pré-régional et seniors : engagements via FBI uniquement."),
        ("Listes de brûlés", "Par formulaire (seniors féminines et masculins), transmis à la commission compétitions."),
    ]) + docs([
        ("Mode opératoire engagements FBI (30/06/2026)", GP + "2026/06/2026_06_30_mode_operatoire_engagements-fbi.pdf", "Engagements"),
        ("Règlements sportifs généraux du CD33", "https://drive.google.com/file/d/1zeO1xUafOou85uP7nhwm-Cz5NN1wYTfU/view", "Règlement"),
    ]), alt=True)
    + section("coupes", "Coupes 33", "Seniors et jeunes", rows([
        ("Coupe seniors", "48 équipes masculines, 24 équipes féminines."),
        ("Coupe jeunes", "U15F, U15M, U18F, U18M."),
        ("Finales", "Samedi 12 juin 2027, toutes les Coupes 33."),
        ("Contact", "Commission des coupes 33 : <a href='mailto:secretariat@basket33.fr'>secretariat@basket33.fr</a>."),
    ]) + docs([
        ("Notices Coupe 33 seniors 2026-2027 (tours, dates)", GP + "2026/10/notices-seniors-3.docx", "Notice"),
        ("Notice Coupe 33 jeunes 2026-2027", GP + "2026/10/notice-jeunes-3.docx", "Notice"),
        ("Cahier des charges des phases finales des Coupes 33", GP + "2026/02/2026_02_06-cahier_charges-_coupes.pdf", "Phases finales"),
    ]))
    + section("trois", "3x3", "Championnat départemental 2026-2027", '<div class="table-wrap"><table class="tbl"><thead><tr><th>Stop</th><th>Lieu</th><th>Dates et catégories</th></tr></thead><tbody>'
        + "".join(f"<tr><th scope='row'>{a}</th><td>{b}</td><td>{c}</td></tr>" for a, b, c in STOPS)
        + "</tbody></table></div>" + rows([
        ("Ouvert à", "U13 à seniors. Effectif de 3 à 7 joueurs, 4 au maximum par stop."),
        ("Tarif", "40 € par équipe (U13 à U18) ; à partir du 3e engagement dans une catégorie, les suivants sont offerts."),
        ("Qualification", "Vainqueurs des 4 stops et 4 meilleures équipes au classement pour le Master départemental, puis Master régional et finales nationales."),
        ("Avant le premier stop", "Chaque joueur crée son profil sur <a href='https://play.fiba3x3.com/?lang=fr-FR' target='_blank' rel='noopener'>PlayFIBA 3X3</a>."),
        ("Contact", "<a href='mailto:developpement@basket33.fr'>developpement@basket33.fr</a>"),
    ]) + docs([
        ("Formulaire d'inscription 3x3", "https://docs.google.com/forms/d/e/1FAIpQLSeOoPaNeZO1yskBizRBk1AGCH0p0N6wbBR_PsVDKE_x0u-C7g/viewform", "Inscription"),
        ("Règlements sportifs généraux 3x3 FFBB 2026-2027", GP + "2026/09/01-refbfbdglements-sportifs-gefbfbdnefbfbdraux-3x3-vdef.pdf", "Règlement"),
    ]), alt=True)
    + section("engager", "Engager ses équipes", "Championnats et coupes", rows([
        ("Jeunes départemental", "Une feuille d'engagement par catégorie, à télécharger sur le site actuel du comité."),
        ("Pré-région et seniors", "Via FBI uniquement (voir le mode opératoire)."),
        ("Mini-basket", "<a href='https://docs.google.com/forms/d/e/1FAIpQLSc67OBv3uym-eVDTCE97Ozq6PkiMFjwh1efUysndh6rxMpPhA/viewform' target='_blank' rel='noopener'>Formulaire en ligne</a>."),
        ("Coupes 33", "Fiches d'engagement jeunes, seniors féminines et seniors masculins."),
        ("Tarifs", "Dans les <a href='licences.html#tarifs'>dispositions financières 2026-2027</a>."),
    ]))
)

# ---------------------------------------------------------------- Joueurs
DET = [
    ("Arcachonnais · Sud Gironde", "Dim. 15/11/2026, gymnase Paul Langevin, Bègles · Dim. 06/12/2026 (lieu à confirmer)", "Filles 9h30-11h, garçons 11h-12h30 (le 15/11)"),
    ("District de Bordeaux", "Dim. 15/11 et dim. 29/11/2026, gymnase Jean Bouin, Talence", "15/11 : filles 9h30-11h, garçons 11h-12h30 · 29/11 : garçons 9h30-11h, filles 11h-12h30"),
    ("Rive droite", "Dim. 15/11/2026 et sam. 21/11/2026, gymnase municipal, Tresses", "15/11 : filles 9h30-11h, garçons 11h-12h30 · 21/11 : garçons 14h-15h30, filles 15h30-17h"),
    ("Médoc", "Dim. 22/11/2026 et dim. 06/12/2026, Le Taillan", "22/11 : filles 9h30-11h, garçons 11h-12h30 · 06/12 : garçons 9h30-11h, filles 11h-12h30"),
]
joueurs_body = (
    section("detections", "Détections", "Génération 2014/2015", '<div class="table-wrap"><table class="tbl"><thead><tr><th>Secteur</th><th>Dates et lieux</th><th>Horaires</th></tr></thead><tbody>'
        + "".join(f"<tr><th scope='row'>{a}</th><td>{b}</td><td>{c}</td></tr>" for a, b, c in DET)
        + "</tbody></table></div><p class='note'>Les convocations sont transmises par le comité aux clubs. Rendez-vous 15 minutes avant chaque créneau.</p>")
    + section("selections", "Sélections", "Du district à l'inter-comités", rows([
        ("Parcours", "Détections par secteur, tournoi inter-districts, puis sélections départementales (Tournoi des Étoiles, Tournoi inter-comités)."),
        ("Espoirs girondins", "Stages et entraînements pour les jeunes repérés."),
        ("Camps du comité", "Stages en internat pour les 11-15 ans à Villenave d'Ornon : <a href='https://girondebasketcamp.wixsite.com/girondebasketcamp' target='_blank' rel='noopener'>site des camps</a>."),
    ]), alt=True)
)

# ---------------------------------------------------------------- Mini-basket
mini_body = (
    section("projet", "Projet 2025-2028", "Un mini-basket éducatif", rows([
        ("Les principes", "Plaisir de jouer, temps de jeu équilibré pour chaque enfant, règles adaptées à l'âge."),
        ("Le projet complet", "<a href='https://www.canva.com/design/DAGxvoTcSIc/6ZKWF5lo8krE9HBEn_To-Q/view' target='_blank' rel='noopener'>Présentation du projet mini-basket 2025-2028</a>."),
        ("Contact", "Commission mini-basket : <a href='mailto:secretariat@basket33.fr'>secretariat@basket33.fr</a>."),
    ]))
    + section("outils", "U9 et U11", "Règlements et outils de match", docs([
        ("Règlement simplifié U9 et U9/U11 (octobre 2026)", GP + "2026/10/reglement-simplifie-u9-championnat-et-u9u11.pdf", "Règlement"),
        ("Règlement championnat U9 et U11", GP + "2025/09/u09_u11-reglements.pdf", "Règlement"),
        ("Fiche rencontre U9 / U9-U11 championnat", GP + "2025/11/fiche-rencontre-u9u9championnatu11.pdf", "Match"),
        ("Application de rotations des joueurs", "https://cd33-basketball.web.app/teams", "Outil"),
        ("Feuille de rotations (Excel)", GP + "2025/09/feuille-dorganisation-mini1-1.xlsx", "Outil"),
    ]), alt=True)
    + section("labels", "Labels", "École de mini-basket", rows([
        ("École française de mini-basket", "Label fédéral pour les clubs qui accueillent les plus jeunes dans les meilleures conditions."),
        ("École départementale (EDMB)", "Label du comité. <a href='clubs.html#labels'>Clubs labellisés</a>."),
    ]))
)

# ---------------------------------------------------------------- Licences
lic_body = (
    section("tarifs", "Tarifs", "Saison 2026-2027", rows([
        ("Licence", "Obligatoire pour pratiquer en club, même en loisir. Elle donne aussi accès aux compétitions 3x3."),
        ("Montants", "Cotisations licences, mutations, engagements, amendes et forfaits : dans les dispositions financières."),
    ]) + docs([
        ("Dispositions financières 2026-2027", "https://drive.google.com/file/d/13SY2D7ZyJ06w_t-XtJUsXBWPZEqjPHBg/view", "Tarifs"),
        ("Tarifs des licences 2026-2027 (image)", GP + "2026/09/image_tarifs_licences_26_27-2.png", "Tarifs"),
    ]))
    + section("modes", "Démarches", "Modes opératoires", docs([
        ("Création de licence", GP + "2023/08/mode-operatoire-creation.pdf", "Mode opératoire"),
        ("Renouvellement de licence", GP + "2023/08/mode-operatoire-renouvellement.pdf", "Mode opératoire"),
        ("Renouvellement, base historique", GP + "2023/08/mode-operatoire-renouvellement-base-historique.pdf", "Mode opératoire"),
        ("Mutation", GP + "2023/08/mode-operatoire-mutation.pdf", "Mode opératoire"),
        ("Validation des licences par le club", GP + "2023/08/mode-operatoire-validation-clubs.pdf", "Mode opératoire"),
        ("Licences AST et extensions T", GP + "2021/08/processus-licences-t_ast.pdf", "Processus"),
    ]), alt=True)
    + section("surclassement", "Surclassement", "Jouer dans une catégorie supérieure", docs([
        ("Certificat d'aptitude au surclassement (à imprimer sur papier blanc)", "https://drive.google.com/file/d/11Yh4gjXVsrtb6g194ZeWczkyYvBBSiGK/view", "Certificat"),
        ("Note FFBB : surclassement automatique des U18 vers les U21 (octobre 2025)", GP + "2025/10/u18-vers-u21.png", "Note"),
    ]))
)

# ---------------------------------------------------------------- Clubs
clubs_body = (
    section("trouver", "Trouver un club", "Six districts", '<div class="districts" id="districts"></div>')
    + section("labels", "Labels", "Les clubs labellisés", rows([
        ("École française de mini-basket", "CMO Bassens, St Médard Basket, AS St Delphin, Pessac BC, JSA Bordeaux, US Talence, B. Izon, US Brédoise Basket, Langon SG."),
        ("École départementale de mini-basket", "Bordeaux Etudiants Club, ES Blanquefort, AS Martignas, Basket Bassin d'Arcachon."),
        ("Club formateur", "St Médard Basket, JSA Bordeaux."),
        ("FFBB Citoyen MAIF", "3 étoiles : US Brédoise Basket, Ent. Pessac BC · 2 étoiles : CMO Bassens, St Médard Basket · 1 étoile : BC St Avit St Nazaire, BC Estuaire Gironde, Basket Izon."),
    ]), alt=True)
    + section("demarches", "Démarches", "Créer, affilier, labelliser", rows([
        ("Créer ou ré-affilier un club", "Formulaire d'affiliation FFBB et <a href='" + GP + "2020/11/mode-operatoire-reaffiliation.pdf' target='_blank' rel='noopener'>mode opératoire de ré-affiliation</a>."),
        ("Créer une entente ou une CTC", "Conventions types et tutoriels FFBB, à demander au secrétariat."),
        ("Labelliser son club", "Le comité accompagne les clubs dans leurs démarches de labels fédéraux et départementaux."),
        ("Homologuer sa salle", "Commission Équipements, via le secrétariat."),
    ]))
)

# ---------------------------------------------------------------- Formations
form_body = (
    section("arbitres", "Arbitres", "Devenir arbitre départemental", rows([
        ("La formation", "Trois week-ends, une journée d'examen (écrit et oral) et une évaluation sur le terrain."),
        ("Inscription", "<a href='https://docs.google.com/forms/d/e/1FAIpQLSdVLD6KxDRbsQwf8QUG1_g9PkeogqNdeLd874iyKcupPPe9cA/viewform' target='_blank' rel='noopener'>Formulaire d'inscription</a>."),
        ("Camps arbitres", "Dès 15 ans, formation diplômante FFBB pour officier dès septembre."),
        ("Contact", "Commission des officiels : <a href='mailto:CDO@basket33.fr'>CDO@basket33.fr</a>."),
    ]) + docs([
        ("Mémo arbitres complet", GP + "2026/11/memo-ref-complet.pdf", "Arbitres"),
        ("Rapport d'incidents disciplinaires", GP + "2026/11/incidents-disciplinaires.pdf", "Formulaire"),
        ("Formulaire de réclamation", GP + "2026/11/formulaire-reclamation.pdf", "Formulaire"),
    ]))
    + section("otm", "Officiels de table", "OTM et e-marque", rows([
        ("Les rôles", "Marqueur (feuille e-marque), chronométreur, opérateur 24 secondes."),
        ("Accompagnement", "Le comité a formé plus de 30 clubs à l'e-marque V2."),
    ]), alt=True)
    + section("entraineurs", "Entraîneurs", "Brevets fédéraux", rows([
        ("BF enfants", "Pour encadrer les U9 à U12."),
        ("BF jeunes", "Pour encadrer les U13 à U15."),
        ("BF adultes", "Pour encadrer les U17 et plus."),
        ("Inscription", "Dès 16 ans, licencié FFBB, directement sur <a href='https://nasket.net' target='_blank' rel='noopener'>nasket.net</a>."),
    ]))
)

# ---------------------------------------------------------------- Comité
COMM = [
    ("Président du comité", "Jean-Luc Dubos"), ("Commission sportive", "Cécile Doumax"), ("Commission technique", "Anaïs Boisnier"),
    ("Commission mini-basket", "Michèle Ladois"), ("Commission féminine", "Anna Gbedemah"), ("Commission des officiels", "Fabien Tapie"),
    ("3x3 et événementiel", "Stéphane Vernagallo"), ("Accompagnement des clubs", "Ludovic Garrigos"), ("Équipements et Coupes 33", "Jacques Doublet"),
    ("Qualification", "Edith Lanau"), ("Communication", "Théo Lanchon-Dumontier"), ("Moyens généraux", "Anthony Matignon"), ("Vivre ensemble", "Gaëtan Sauvignon"),
]
comite_body = (
    section("missions", "Missions", "Le CD33", '<div class="prose"><p>Structure déconcentrée de la FFBB, le comité applique en Gironde la politique fédérale : il organise et développe le basket, soutient les clubs, prépare les compétitions départementales et pré-régionales, et forme joueurs, entraîneurs, arbitres, officiels et dirigeants.</p></div>'
        + docs([("Statuts du comité (24/06/2023)", GP + "2024/01/2023-06-24-statuts-cd33.pdf", "Statuts"),
                ("Règlement intérieur", GP + "2022/06/2021_02_22-recc80glement-intecc81rieur-cd33.pdf", "Règlement")]))
    + section("elus", "Comité directeur 2024-2028", "Les commissions", '<div class="people">' + "".join(f'<div class="person"><span>{r}</span><strong>{n}</strong></div>' for r, n in COMM) + '</div><p class="note">Pour joindre une commission : <a href="mailto:secretariat@basket33.fr">secretariat@basket33.fr</a>, qui transmet.</p>', alt=True)
    + section("finances", "Finances", "Transparence", docs([
        ("Indicateurs financiers 2025 (AG du 20/06/2026)", "https://drive.google.com/file/d/1Yi3O5QZqxPBfm113js6vKMYXlOW2K_9o/view", "Finances"),
        ("Comptes annuels 2025", "https://drive.google.com/file/d/1wKq6LqKBZLNhWKGgGmz-ue6NBK6Idzan/view", "Finances"),
        ("Dispositions financières 2026-2027", "https://drive.google.com/file/d/13SY2D7ZyJ06w_t-XtJUsXBWPZEqjPHBg/view", "Tarifs"),
    ]))
    + section("contact", "Contact", "Nous joindre", '<div class="contact"><div><h3>Adresse</h3><p>4 allée Annie Fratellini<br>33140 Villenave d\'Ornon</p></div><div><h3>Secrétariat</h3><p><a href="mailto:secretariat@basket33.fr">secretariat@basket33.fr</a><br><a href="tel:+33619863771">06 19 86 37 71</a></p></div><div><h3>Accueil sur place</h3><p>Lundi et jeudi, 9h-17h</p></div></div>', alt=True)
)

# ---------------------------------------------------------------- Documents et assistant
docs_body = '<section class="section"><div class="container"><div class="doc-tools"><label for="doc-q" class="sr">Rechercher un document</label><input id="doc-q" type="search" placeholder="Rechercher un document…" autocomplete="off"><div class="doc-filters" id="doc-filters" role="group" aria-label="Filtrer par catégorie"></div></div><div class="doc-list" id="doc-list"></div><p class="note">Vous cherchez une information précise dans un document ? <a href="assistant.html">Posez la question à l\'assistant</a>, il cherche à l\'intérieur des textes.</p></div></section>'
asst_body = '''<section class="section dark asst">
  <div class="container narrow">
    <form class="ask" id="ask-form" role="search">
      <label for="ask-q" class="sr">Votre question</label>
      <input id="ask-q" type="search" placeholder="Ex. : Combien coûte une licence U13 ?" autocomplete="off" required>
      <button type="submit" class="btn btn-primary">Demander</button>
    </form>
    <div class="suggest" id="suggest"></div>
    <div id="answer" class="answer" aria-live="polite"></div>
    <p class="fineprint">Les réponses sont extraites des pages et documents officiels du comité : vérifiez toujours la source. Vos questions ne sont pas enregistrées. En cas de doute : <a href="mailto:secretariat@basket33.fr">secretariat@basket33.fr</a>.</p>
  </div>
</section>'''

PAGES = [
    ("index", "Accueil", "Le Comité départemental de basket-ball de la Gironde : compétitions, détections, mini-basket, licences, clubs, documents officiels et assistant.", "", "", "", home_body),
    ("competitions", "Compétitions", "Championnats jeunes et seniors, Coupes 33, 3x3 départemental et engagements des équipes en Gironde, saison 2026-2027.", "Compétitions", "Compétitions", "Championnats, Coupes 33 et 3x3 : calendrier, règlements et engagements de la saison 2026-2027.", comp_body),
    ("joueurs", "Détections et sélections", "Détections de la génération 2014/2015 en Gironde : dates, lieux et horaires par secteur, sélections et camps.", "Joueurs", "Détections<br>et sélections", "Les dates et lieux des détections de la génération 2014/2015, puis le parcours vers les sélections.", joueurs_body),
    ("mini-basket", "Mini-basket", "Mini-basket en Gironde : projet 2025-2028, règlements U9 et U11, fiche rencontre et outils de rotation.", "Mini-basket", "Mini-basket", "U7, U9 et U11 : le projet éducatif du comité, les règlements et les outils pour les matchs.", mini_body),
    ("licences", "Licences et tarifs", "Licences de basket en Gironde : tarifs 2026-2027, dispositions financières, modes opératoires et surclassement.", "Licences", "Licences<br>et tarifs", "Tarifs de la saison, démarches de licence et surclassement.", lic_body),
    ("clubs", "Clubs", "Les clubs de basket de la Gironde par district, les clubs labellisés et les démarches pour créer ou affilier un club.", "Clubs", "Trouver un club", "Les clubs girondins par district, leurs labels et les démarches pour les dirigeants.", clubs_body),
    ("formations", "Se former", "Devenir arbitre, officiel de table ou entraîneur en Gironde : formations, inscriptions et documents.", "Se former", "Se former", "Arbitrer, tenir la table de marque ou entraîner : les formations proposées par le comité et la FFBB.", form_body),
    ("comite", "Le comité", "Le Comité départemental de basket-ball de la Gironde : missions, commissions, finances et contact.", "Le comité", "Le comité", "Missions, commissions, documents institutionnels et contact.", comite_body),
    ("documents", "Documents officiels", "Tous les documents officiels du comité de basket de la Gironde : règlements, tarifs, calendrier, notes, modes opératoires.", "Documents", "Documents<br>officiels", "Règlements, tarifs, calendrier, notes et modes opératoires. Cherchez par mot-clé ou par catégorie.", docs_body),
    ("assistant", "Une question ?", "Posez votre question sur le basket en Gironde : l'assistant cherche la réponse dans les pages et documents officiels du comité.", "Assistant", "Une question ?", "Licence, tarifs, règlements, calendrier, 3x3, formations : l'assistant cherche dans les pages et documents officiels, et donne toujours la source.", asst_body),
]

for slug, title, desc, kicker, h1, lead, body in PAGES:
    with open(os.path.join(ROOT, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(page(slug, title, desc, kicker, h1, lead, body))

with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    today = datetime.date.today().isoformat()
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for slug, *_ in PAGES:
        f.write(f"  <url><loc>{BASE_URL}{'' if slug == 'index' else slug + '.html'}</loc><lastmod>{today}</lastmod></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n")
print("Pages générées :", ", ".join(p[0] for p in PAGES))
