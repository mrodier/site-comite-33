"""Génère les pages HTML du site à partir d'un gabarit commun.
Usage : python3 _build/build.py   (depuis la racine du dépôt)
Modifier le contenu dans PAGES ci-dessous, puis relancer le script et pousser les fichiers produits."""
import os, json, datetime, pathlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://mrodier.github.io/site-comite-33/"
MAJ = "26/11/2026"
GP = "https://girondebasket.com/wp-content/uploads/"

# Menu principal : (page, libellé, [(ancre ou page, libellé), ...])
MENU = [
    ("comite", "Le CD33", [("comite.html#missions", "Qui sommes-nous"), ("comite.html#elus", "Commissions"), ("comite.html#finances", "Finances"), ("comite.html#contact", "Contact")]),
    ("clubs", "Nos clubs", [("clubs.html#trouver", "Trouver un club"), ("clubs.html#labels", "Clubs labellisés"), ("clubs.html#demarches", "Créer, affilier, labelliser"), ("licences.html", "Licences et tarifs"), ("licences.html#surclassement", "Surclassement")]),
    ("competitions", "Compétitions et pratiques", [("competitions.html#jeunes", "Championnats jeunes"), ("competitions.html#seniors", "Championnats seniors"), ("competitions.html#coupes", "Coupes 33"), ("competitions.html#trois", "3x3"), ("mini-basket.html", "Mini-basket"), ("competitions.html#engager", "Engager ses équipes")]),
    ("formations", "Formations", [("joueurs.html", "Joueur"), ("formations.html#arbitres", "Arbitres"), ("formations.html#otm", "Officiels de table"), ("formations.html#entraineurs", "Entraîneurs")]),
    ("agenda", "Agenda", []),
    ("galerie", "Galerie photos", []),
    ("documents", "Ressources documentaires", []),
]
SECTION_OF = {"mini-basket": "competitions", "joueurs": "formations", "licences": "clubs"}

def doc(label, url, meta=""):
    m = f'<span class="doc-cat">{meta}</span>' if meta else ""
    return f'<a class="doc" href="{url}" target="_blank" rel="noopener"><span class="doc-title">{label}</span>{m}<span class="doc-open">Ouvrir ↗</span></a>'

CHEV = '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'

def menu(slug):
    cur = SECTION_OF.get(slug, slug)
    out = []
    for s, label, subs in MENU:
        here = ' aria-current="page"' if s == cur else ""
        if not subs:
            out.append(f'<li class="mi"><a class="mlink" href="{s}.html"{here}>{label}</a></li>')
            continue
        items = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in subs)
        out.append(f'<li class="mi has-sub"><a class="mlink" href="{s}.html"{here}>{label}</a>'
                   f'<button type="button" class="sub-toggle" aria-expanded="false" aria-label="Ouvrir le sous-menu {label}">{CHEV}</button>'
                   f'<ul class="sub">{items}</ul></li>')
    return "".join(out)

def page(slug, title, desc, kicker, h1, lead, body, wide_head=False):
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/style.css">
</head>
<body class="p-{slug}">
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="header" id="topbar">
  <div class="wrap header-inner">
    <a class="brand" href="index.html" aria-label="Comité de basket de la Gironde, accueil">
      <img src="assets/ballon-33.svg" alt="" width="44" height="47">
      <span class="brand-t"><span>Comité</span><span>Basketball</span><span>Gironde</span></span>
    </a>
    <nav class="menu" id="nav" aria-label="Menu principal">
      <ul class="menu-list">{menu(slug)}</ul>
    </nav>
    <a class="ask-btn" href="assistant.html"{' aria-current="page"' if slug == 'assistant' else ''}>Une question ?</a>
    <button type="button" class="menu-toggle" id="menu-toggle" aria-expanded="false" aria-controls="nav"><span class="burger" aria-hidden="true"></span>Menu</button>
  </div>
</header>
<main id="contenu">
{hero(slug, kicker, h1, lead)}
{body}
</main>
{FOOTER}
<script src="assets/config.js"></script>
<script src="assets/app.js"></script>
</body>
</html>
"""

def hero(slug, kicker, h1, lead):
    if slug == "index":
        return ""
    return f"""<section class="phead">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Accueil</a> <span aria-hidden="true">/</span> {kicker}</p>
    <h1>{h1}</h1>
    {f'<p class="phead-lead">{lead}</p>' if lead else ''}
    <p class="updated">Mis à jour le {MAJ}</p>
  </div>
</section>"""

AGENDA = [  # (jour, mois, titre, lieu, lien) – à tenir à jour
    ("29", "nov.", "Détections 2014/2015 · District de Bordeaux", "Gymnase Jean Bouin, Talence", "joueurs.html#detections"),
    ("06", "déc.", "Détections 2014/2015 · Médoc et Sud Gironde", "Le Taillan · lieu Sud Gironde à confirmer", "joueurs.html#detections"),
    ("19", "déc.", "3x3 départemental · Stop 2 (19 et 20 déc.)", "Halle des sports, Talence", "competitions.html#trois"),
    ("22", "févr.", "3x3 départemental · Stop 3 (22 au 25 févr.)", "Halle des sports, Talence", "competitions.html#trois"),
    ("19", "avr.", "3x3 départemental · Stop 4 (19 au 22 avr.)", "Halle des sports, Talence", "competitions.html#trois"),
    ("12", "juin", "Finales des Coupes 33", "Toutes catégories", "competitions.html#coupes"),
]

FOOTER = f"""<footer class="footer">
  <div class="wrap footer-grid">
    <div class="fcol">
      <img src="assets/logo.svg" alt="Gironde Basketball" width="72" height="104" class="flogo">
      <p>4 allée Annie Fratellini<br>33140 Villenave d'Ornon</p>
      <p><a href="tel:+33619863771">06 19 86 37 71</a><br><a href="mailto:secretariat@basket33.fr">secretariat@basket33.fr</a></p>
      <p class="fmuted">Accueil sur place : lundi et jeudi, 9h-17h</p>
    </div>
    <div class="fcol">
      <h2>Liens utiles</h2>
      <ul>
        <li><a href="https://www.ffbb.com/" rel="noopener">Fédération française de basket-ball</a></li>
        <li><a href="https://nouvelleaquitainebasketball.org/" rel="noopener">Ligue Nouvelle-Aquitaine</a></li>
        <li><a href="https://www.3x3ffbb.com/" rel="noopener">3x3 FFBB</a></li>
        <li><a href="https://www.gironde.fr/" rel="noopener">Département de la Gironde</a></li>
        <li><a href="https://www.agencedusport.fr/" rel="noopener">Agence nationale du sport</a></li>
      </ul>
    </div>
    <div class="fcol">
      <h2>Suivez-nous</h2>
      <ul>
        <li><a href="https://www.facebook.com/Cd33Basket" rel="noopener">Facebook</a></li>
        <li><a href="https://www.instagram.com/girondebasket" rel="noopener">Instagram</a></li>
        <li><a href="https://www.youtube.com/@comitedegirondedebasketbal7366" rel="noopener">YouTube</a></li>
      </ul>
      <a class="fask" href="assistant.html">Une question ? Demandez à l'assistant →</a>
    </div>
    <div class="fcol">
      <h2><a href="agenda.html">Agenda</a></h2>
      <ul class="fagenda">{''.join(f'<li><a href="{h}"><strong>{d} {m}</strong> {tt}</a></li>' for d, m, tt, l, h in AGENDA[:4])}</ul>
    </div>
  </div>
  <div class="wrap fbottom"><span>© Comité départemental de basket-ball de la Gironde</span><a href="mentions-legales.html">Mentions légales et confidentialité</a></div>
</footer>"""

def section(id_, kicker, title, inner, alt=False, lead=""):
    return f"""<section class="section{' alt' if alt else ''}" id="{id_}">
  <div class="wrap">
    <div class="section-head"><p class="kicker">{kicker}</p><h2>{title}</h2>{f'<p class="section-lead">{lead}</p>' if lead else ''}</div>
    {inner}
  </div>
</section>"""

def rows(items):
    return '<div class="rows">' + "".join(f'<div class="row"><h3>{h}</h3><div>{t}</div></div>' for h, t in items) + "</div>"

def docs(items):
    return '<div class="doc-list">' + "".join(doc(*i) for i in items) + "</div>"

# ---------------------------------------------------------------- Accueil
SLIDES = [  # image dans assets/carrousel/ (format 16:6, remplaçable par une photo), texte alternatif, lien
    ("00-bienvenue.svg", "Le basket en Gironde, comité départemental de basket-ball", "comite.html"),
    ("01-detections.svg", "Détections génération 2014/2015, novembre et décembre 2026", "joueurs.html"),
    ("02-3x3-stop2.svg", "3x3 départemental, stop 2 les 19 et 20 décembre 2026 à Talence", "competitions.html#trois"),
    ("04-finales-coupes.svg", "Finales des Coupes 33 le samedi 12 juin 2027", "competitions.html#coupes"),
]

def slider():
    slides = "".join(
        f'<li class="slide" role="group" aria-roledescription="diapositive" aria-label="{i+1} sur {len(SLIDES)}">'
        f'<a href="{href}"><img src="assets/carrousel/{img}" alt="{alt}" width="1920" height="720" loading="{"eager" if i == 0 else "lazy"}"></a></li>'
        for i, (img, alt, href) in enumerate(SLIDES))
    dots = "".join(f'<button type="button" class="dot" aria-label="Diapositive {i+1}"{" aria-current=\"true\"" if i == 0 else ""}></button>' for i in range(len(SLIDES)))
    return f"""<section class="hero-slider" aria-roledescription="carrousel" aria-label="À la une">
  <div class="carousel" data-carousel>
    <ul class="slides">{slides}</ul>
    <button type="button" class="cbtn prev" data-dir="-1" aria-label="Diapositive précédente">‹</button>
    <button type="button" class="cbtn next" data-dir="1" aria-label="Diapositive suivante">›</button>
    <div class="dots">{dots}</div>
  </div>
</section>"""

FIGURES = [("66", "Clubs"), ("6", "Districts"), ("50+", "Bénévoles"), ("5", "Salariés"), ("4", "Stops 3x3")]
ACTIVITES = [
    ("competitions.html#jeunes", "5x5", "Championnats jeunes et seniors"),
    ("competitions.html#trois", "3x3", "Championnat départemental"),
    ("mini-basket.html", "Mini-basket", "U7, U9, U11"),
    ("competitions.html#coupes", "Coupes 33", "Seniors et jeunes"),
    ("joueurs.html", "Détections", "Génération 2014/2015"),
    ("formations.html#arbitres", "Officiels", "Arbitres et table de marque"),
    ("formations.html#entraineurs", "Entraîneurs", "Brevets fédéraux"),
    ("clubs.html", "Nos clubs", "66 clubs, 6 districts"),
]
BASEDOC = [
    ("documents.html#reglements", "Règlements sportifs"), ("documents.html#finances", "Tarifs et dispositions financières"),
    ("documents.html#clubs-licences", "Licences : modes opératoires"), ("documents.html#competitions", "Compétitions et engagements"),
    ("documents.html#cd33", "Statuts et règlement intérieur"), ("documents.html", "Toutes les ressources documentaires"),
]
ACTUS = [  # articles du site actuel girondebasket.com
    ("19/11/2026", "Violences dans le sport : le comité signe une convention départementale", "https://girondebasket.com/2026/11/19/violences-dans-le-sport-le-comite-de-gironde-de-basket-ball-signe-une-convention-departementale/"),
    ("05/11/2026", "Respect en jeu : la dynamique se poursuit", "https://girondebasket.com/2026/11/05/respect-en-jeu-la-dynamique-se-poursuit/"),
    ("13/05/2026", "1/2 finales Coupe 33 seniors féminines : Pessac veut garder la coupe !", "https://girondebasket.com/2026/05/13/1-2-finales-coupe-33-seniors-feminines-pessac-veut-garder-la-coupe/"),
    ("04/05/2026", "Florian Leroyer, arbitre de Gauriac, sacré champion de France", "https://girondebasket.com/2026/05/04/florian-leroyer-arbitre-de-gauriac-sacre-champion-de-france/"),
]
PARTENAIRES = [("Fédération française de basket-ball", "https://www.ffbb.com/"), ("Ligue Nouvelle-Aquitaine", "https://nouvelleaquitainebasketball.org/"), ("Département de la Gironde", "https://www.gironde.fr/"), ("Agence nationale du sport", "https://www.agencedusport.fr/")]

home_body = f"""{slider()}
<section class="figures" aria-label="Le comité en chiffres">
  <div class="wrap"><ul>{''.join(f'<li><strong>{n}</strong><span>{l}</span></li>' for n, l in FIGURES)}</ul></div>
</section>
<section class="section" id="activites">
  <div class="wrap">
    <div class="section-head center"><h2>Nos activités</h2></div>
    <div class="tiles">{''.join(f'<a class="tile" href="{h}"><span class="tile-t">{t}</span><span class="tile-d">{d}</span></a>' for h, t, d in ACTIVITES)}</div>
  </div>
</section>
<section class="section alt" id="administratif">
  <div class="wrap">
    <div class="section-head center"><h2>Administratif et base documentaire</h2></div>
    <div class="admin">
      <ul class="admin-links">{''.join(f'<li><a href="{h}"><span class="ico" aria-hidden="true">▤</span>{l}</a></li>' for h, l in BASEDOC[:3])}</ul>
      <form class="ask-card" action="assistant.html" method="get" role="search">
        <p class="ask-k">Assistant</p>
        <h3>Une question ?</h3>
        <p>Il cherche la réponse dans les pages et documents officiels du comité et vous donne la source.</p>
        <label for="home-q" class="sr">Votre question</label>
        <div class="ask-row"><input id="home-q" name="q" type="search" placeholder="Ex. : tarif licence U13" autocomplete="off" required><button type="submit">Demander</button></div>
      </form>
      <ul class="admin-links">{''.join(f'<li><a href="{h}"><span class="ico" aria-hidden="true">▤</span>{l}</a></li>' for h, l in BASEDOC[3:])}</ul>
    </div>
  </div>
</section>
<section class="section" id="agenda">
  <div class="wrap two-cols">
    <div>
      <div class="section-head"><h2>Agenda</h2></div>
      <ul class="agenda">{''.join(f'<li><a href="{h}"><span class="date"><strong>{d}</strong>{m}</span><span><span class="ag-t">{tt}</span><span class="ag-l">{l}</span></span></a></li>' for d, m, tt, l, h in AGENDA)}</ul>
      <p class="more"><a href="agenda.html">Tout l’agenda →</a></p>
    </div>
    <div>
      <div class="section-head"><h2>Actualités</h2></div>
      <ul class="news">{''.join(f'<li><a href="{u}" target="_blank" rel="noopener"><span class="news-d">{d}</span><span class="news-t">{tt}</span></a></li>' for d, tt, u in ACTUS)}</ul>
      <p class="more"><a href="https://girondebasket.com/category/blog/" target="_blank" rel="noopener">Toutes les actualités →</a></p>
    </div>
  </div>
</section>
<section class="partners" aria-label="Partenaires institutionnels">
  <div class="wrap"><p class="kicker">Nos partenaires institutionnels</p><ul>{''.join(f'<li><a href="{u}" rel="noopener">{n}</a></li>' for n, u in PARTENAIRES)}</ul></div>
</section>
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
docs_body = """<section class="section">
  <div class="wrap">
    <div class="res-search">
      <label for="doc-q" class="res-label">Quel document cherchez-vous ?</label>
      <div class="res-row">
        <input id="doc-q" type="search" placeholder="Ex. : règlement 3x3, tarifs, mutation, fiche rencontre U9…" autocomplete="off">
      </div>
      <p class="res-help">Tapez un ou plusieurs mots : la recherche porte sur le titre, la rubrique du site où le document apparaît et, pour les documents indexés, sur leur texte. Les accents et majuscules ne comptent pas.</p>
    </div>
    <div class="doc-filters" id="doc-filters" role="group" aria-label="Filtrer par catégorie"></div>
    <div class="res-bar"><p id="doc-count" class="res-count" aria-live="polite"></p>
      <label class="res-sort">Trier <select id="doc-sort"><option value="cat">par catégorie</option><option value="az">de A à Z</option></select></label></div>
    <div class="res-list" id="doc-list"></div>
    <p class="note">Vous ne trouvez pas ? <a href="assistant.html">Posez la question à l'assistant</a> ou écrivez à <a href="mailto:secretariat@basket33.fr">secretariat@basket33.fr</a>.</p>
  </div>
</section>"""
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

# ---------------------------------------------------------------- Agenda
CAL_GENERAL = "https://drive.google.com/file/d/1ml0u5hERsjXXAmbd_6r5MFnAS_rRXM9-/view"
MOIS = {"nov.": "Novembre 2026", "déc.": "Décembre 2026", "janv.": "Janvier 2027", "févr.": "Février 2027", "mars": "Mars 2027", "avr.": "Avril 2027", "mai": "Mai 2027", "juin": "Juin 2027"}

def agenda_body():
    groups = {}
    for d, m, tt, l, h in AGENDA:
        groups.setdefault(MOIS.get(m, m), []).append((d, m, tt, l, h))
    blocks = ""
    for mo, items in groups.items():
        lis = "".join(f'<li><a href="{h}"><span class="date"><strong>{d}</strong>{m}</span><span><span class="ag-t">{tt}</span><span class="ag-l">{l}</span></span></a></li>' for d, m, tt, l, h in items)
        blocks += f'<div class="ag-month"><h2 class="ag-mh">{mo}</h2><ul class="agenda">{lis}</ul></div>'
    return f"""<section class="section">
  <div class="wrap agenda-page">
    <div>{blocks}</div>
    <aside class="ag-side">
      <h2>Calendrier général</h2>
      <p>Toutes les dates de la saison 2026-2027 (championnats, coupes, rassemblements) sont dans le calendrier général du comité.</p>
      <a class="btn-dark" href="{CAL_GENERAL}" target="_blank" rel="noopener">Ouvrir le calendrier 2026-2027 ↗</a>
      <p class="note">Une date manque ou a changé ? Écrivez à <a href="mailto:secretariat@basket33.fr">secretariat@basket33.fr</a>.</p>
    </aside>
  </div>
</section>"""

# ---------------------------------------------------------------- Galerie photos
# Pour ajouter des photos : les déposer dans assets/galerie/ et les lister dans l'album (fichier, légende).
# Ne publier que des photos dont le comité détient les droits, avec l'accord des personnes
# (autorisation parentale pour les mineurs).
GALERIE = [
    ("Détections 2014/2015", "Novembre et décembre 2026", "joueurs.html", []),
    ("3x3 départemental", "Saison 2026-2027", "competitions.html#trois", []),
    ("Mini-basket", "Plateaux et rassemblements", "mini-basket.html", []),
    ("Finales des Coupes 33", "Juin 2027", "competitions.html#coupes", []),
]

def galerie_body():
    albums = ""
    for titre, sous, lien, photos in GALERIE:
        if photos:
            grid = "".join(f'<figure><img src="assets/galerie/{f}" alt="{c}" loading="lazy"><figcaption>{c}</figcaption></figure>' for f, c in photos)
        else:
            grid = '<div class="gal-empty"><span aria-hidden="true"></span><p>Photos à venir</p></div>'
        albums += f'<article class="album"><header><h2>{titre}</h2><p>{sous} · <a href="{lien}">En savoir plus</a></p></header><div class="gal-grid">{grid}</div></article>'
    return f"""<section class="section">
  <div class="wrap">
    {albums}
    <div class="gal-social">
      <p>En attendant, retrouvez les photos des événements sur nos réseaux :
      <a href="https://www.facebook.com/Cd33Basket" rel="noopener">Facebook</a> · <a href="https://www.instagram.com/girondebasket" rel="noopener">Instagram</a> · <a href="https://www.youtube.com/@comitedegirondedebasketbal7366" rel="noopener">YouTube</a></p>
    </div>
  </div>
</section>"""

MENTIONS = (pathlib.Path(__file__).resolve().parent / "mentions-legales.inc.html").read_text(encoding="utf-8")
ml_body = f'<section class="section"><div class="wrap prose">{MENTIONS}</div></section>'

PAGES = [
    ("mentions-legales", "Mentions légales", "Mentions légales et politique de confidentialité du site du Comité de basket de la Gironde.", "Mentions légales", "Mentions légales et confidentialité", "Les passages surlignés sont à compléter et à faire valider par le comité avant la mise en ligne.", ml_body),
    ("index", "Accueil", "Le Comité départemental de basket-ball de la Gironde : compétitions, détections, mini-basket, licences, clubs, documents officiels et assistant.", "", "", "", home_body),
    ("competitions", "Compétitions", "Championnats jeunes et seniors, Coupes 33, 3x3 départemental et engagements des équipes en Gironde, saison 2026-2027.", "Compétitions", "Compétitions", "Championnats, Coupes 33 et 3x3 : calendrier, règlements et engagements de la saison 2026-2027.", comp_body),
    ("joueurs", "Joueur", "Parcours du joueur en Gironde : détections de la génération 2014/2015 (dates, lieux et horaires par secteur), sélections et camps.", "<a href=\"formations.html\">Formations</a> <span aria-hidden=\"true\">/</span> Joueur", "Joueur", "Les dates et lieux des détections de la génération 2014/2015, puis le parcours vers les sélections.", joueurs_body),
    ("mini-basket", "Mini-basket", "Mini-basket en Gironde : projet 2025-2028, règlements U9 et U11, fiche rencontre et outils de rotation.", "Mini-basket", "Mini-basket", "U7, U9 et U11 : le projet éducatif du comité, les règlements et les outils pour les matchs.", mini_body),
    ("licences", "Licences et tarifs", "Licences de basket en Gironde : tarifs 2026-2027, dispositions financières, modes opératoires et surclassement.", "Licences", "Licences<br>et tarifs", "Tarifs de la saison, démarches de licence et surclassement.", lic_body),
    ("clubs", "Clubs", "Les clubs de basket de la Gironde par district, les clubs labellisés et les démarches pour créer ou affilier un club.", "Clubs", "Trouver un club", "Les clubs girondins par district, leurs labels et les démarches pour les dirigeants.", clubs_body),
    ("formations", "Se former", "Devenir arbitre, officiel de table ou entraîneur en Gironde : formations, inscriptions et documents.", "Se former", "Se former", "Arbitrer, tenir la table de marque ou entraîner : les formations proposées par le comité et la FFBB.", form_body),
    ("comite", "Le CD33", "Le Comité départemental de basket-ball de la Gironde : missions, commissions, finances et contact.", "Le CD33", "Le CD33", "Missions, commissions, documents institutionnels et contact.", comite_body),
    ("documents", "Ressources documentaires", "Tous les documents présents sur le site du comité de basket de la Gironde : règlements, tarifs, calendrier, notes, modes opératoires, formulaires.", "Ressources documentaires", "Ressources<br>documentaires", "Tous les documents présents sur le site, réunis au même endroit. Cherchez par mot-clé ou par catégorie.", docs_body),
    ("agenda", "Agenda", "Agenda du basket en Gironde : détections, 3x3 départemental, finales des Coupes 33 et calendrier général 2026-2027.", "Agenda", "Agenda", "Les prochains rendez-vous du comité et le calendrier général de la saison.", agenda_body()),
    ("galerie", "Galerie photos", "Galerie photos du Comité de basket de la Gironde : détections, 3x3, mini-basket, Coupes 33.", "Galerie photos", "Galerie photos", "Les temps forts de la saison en images.", galerie_body()),
    ("assistant", "Une question ?", "Posez votre question sur le basket en Gironde : l'assistant cherche la réponse dans les pages et documents officiels du comité.", "Assistant", "Une question ?", "Licence, tarifs, règlements, calendrier, 3x3, formations : l'assistant cherche dans les pages et documents officiels, et donne toujours la source.", asst_body),
]

# ---------------------------------------------------------------- Écriture des pages et catalogue documentaire
# Le catalogue (data/catalogue.json) réunit tous les documents présents sur le site :
# ceux de data/documents.json et tous les liens « document » rencontrés dans les pages.
import re, html as _html
CAT_MAP = {"Licences et clubs": "Clubs et licences", "Officiels": "Formations et officiels", "Le comité": "Le CD33"}
CAT_OF_PAGE = {"comite": "Le CD33", "competitions": "Compétitions", "joueurs": "Formations et officiels", "formations": "Formations et officiels",
               "licences": "Clubs et licences", "clubs": "Clubs et licences", "mini-basket": "Mini-basket", "agenda": "Compétitions"}
DOC_RE = re.compile(r'<a class="doc" href="([^"]+)"[^>]*><span class="doc-title">(.*?)</span>')

def kind(u):
    low = u.lower().split("?")[0]
    for ext, k in ((".pdf", "PDF"), (".docx", "Word"), (".doc", "Word"), (".xlsx", "Excel"), (".png", "Image"), (".jpg", "Image")):
        if low.endswith(ext):
            return k
    if "docs.google.com/forms" in low: return "Formulaire en ligne"
    if "docs.google.com/document" in low: return "Document Google"
    if "drive.google.com" in low: return "PDF"
    return "Page web"

src = json.load(open(os.path.join(ROOT, "data", "documents.json"), encoding="utf-8"))
catalogue, by_url = [], {}

def add(u, titre, categorie, slug=None, ptitle=None, idx=None):
    key = u.split("#")[0]
    if key not in by_url:
        by_url[key] = {"t": titre, "u": u, "cat": categorie, "k": kind(u), "p": [], "i": idx}
        catalogue.append(by_url[key])
    d = by_url[key]
    if idx is not None and d["i"] is None:
        d["i"] = idx
    if slug and not any(x[0] == slug for x in d["p"]):
        d["p"].append([slug, ptitle])

for i, d in enumerate(src["docs"]):
    add(d["u"], d["t"], CAT_MAP.get(d["cat"], d["cat"]), idx=i)

for slug, title, desc, kicker, h1, lead, body in PAGES:
    out = page(slug, title, desc, kicker, h1, lead, body)
    with open(os.path.join(ROOT, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(out)
    if slug in ("documents", "index", "assistant", "mentions-legales"):
        continue
    for u, lab in DOC_RE.findall(out):
        lab = _html.unescape(re.sub("<[^>]+>", " ", lab)).strip()
        add(_html.unescape(u), lab, CAT_OF_PAGE.get(slug, "Le CD33"), slug, re.sub("<[^>]+>", " ", title))
    if slug == "agenda":
        add(CAL_GENERAL, "Calendrier sportif 2026-2027 (provisoire)", "Compétitions", slug, title)

with open(os.path.join(ROOT, "data", "catalogue.json"), "w", encoding="utf-8") as f:
    json.dump({"maj": MAJ, "docs": catalogue}, f, ensure_ascii=False, separators=(",", ":"))
print("Catalogue :", len(catalogue), "documents")

with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    today = datetime.date.today().isoformat()
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for slug, *_ in PAGES:
        f.write(f"  <url><loc>{BASE_URL}{'' if slug == 'index' else slug + '.html'}</loc><lastmod>{today}</lastmod></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n")
print("Pages générées :", ", ".join(p[0] for p in PAGES))
