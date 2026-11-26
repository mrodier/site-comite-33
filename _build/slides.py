"""Génère les visuels du slider d'accueil (1920x720) : fond noir, texte blanc, accent orange."""
import pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "carrousel"
O = "#E8590C"
SLIDES = {
  "00-bienvenue.svg": ("COMITÉ DÉPARTEMENTAL DE BASKET-BALL", "LE BASKET", "EN GIRONDE", "66 clubs · 6 districts · au service des clubs"),
  "01-detections.svg": ("JOUEURS · GÉNÉRATION 2014/2015", "DÉTECTIONS", "NOV. – DÉC. 2026", "29/11 à Talence · 06/12 au Taillan et en Sud Gironde"),
  "02-3x3-stop2.svg": ("3X3 DÉPARTEMENTAL · STOP 2", "3X3", "19 ET 20 DÉC.", "Halle des sports de Talence · U13 à seniors"),
  "04-finales-coupes.svg": ("COUPES 33 · TOUTES CATÉGORIES", "FINALES", "12 JUIN 2027", "Le rendez-vous de fin de saison du basket girondin"),
}
COURT = f'''<g fill="none" stroke="#ffffff" stroke-opacity=".10" stroke-width="5">
<line x1="1420" y1="0" x2="1420" y2="720"/><circle cx="1420" cy="360" r="150"/><circle cx="1420" cy="360" r="50"/>
<path d="M1924 60 L1760 60 A320 320 0 0 0 1760 660 L1924 660"/><rect x="1700" y="250" width="224" height="220"/></g>
<circle cx="1420" cy="360" r="150" fill="none" stroke="{O}" stroke-width="5" stroke-dasharray="120 820"/>'''
for name, (k, t1, t2, s) in SLIDES.items():
    size = 190 if len(t1) <= 10 else 150
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 720" width="1920" height="720">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#0b0b0b"/><stop offset="1" stop-color="#1c1c1c"/></linearGradient></defs>
<rect width="1920" height="720" fill="url(#g)"/>
{COURT}
<rect x="140" y="170" width="80" height="8" fill="{O}"/>
<text x="140" y="235" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="700" letter-spacing="5" fill="#ffffff" fill-opacity=".8">{k}</text>
<text x="132" y="{235+size}" font-family="'Arial Narrow', Arial, Helvetica, sans-serif" font-size="{size}" font-weight="800" fill="#ffffff">{t1}</text>
<text x="138" y="{235+size+105}" font-family="'Arial Narrow', Arial, Helvetica, sans-serif" font-size="88" font-weight="800" fill="{O}">{t2}</text>
<text x="140" y="{235+size+175}" font-family="Arial, Helvetica, sans-serif" font-size="34" fill="#ffffff" fill-opacity=".8">{s}</text>
</svg>'''
    (OUT / name).write_text(svg, encoding="utf-8")
print("ok")
