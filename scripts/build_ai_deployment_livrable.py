from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle


ROOT = Path('/Users/ed/Desktop/Docker')
OUT = ROOT / 'output' / 'pdf' / 'Livrable_AI_Deployment_OSINT_Edouard_Cappaert.pdf'
IMG1 = Path('/Users/ed/Downloads/WhatsApp Image 2026-07-21 at 19.45.22.jpeg')
IMG2 = Path('/Users/ed/Downloads/WhatsApp Image 2026-07-21 at 19.45.44.jpeg')
IMG3 = Path('/Users/ed/Downloads/WhatsApp Image 2026-07-21 at 19.45.57.jpeg')

W, H = A4
NAVY = colors.HexColor('#0B1728')
NAVY_2 = colors.HexColor('#12233A')
TEAL = colors.HexColor('#0F5C8E')
TEAL_DARK = colors.HexColor('#0B4770')
INK = colors.HexColor('#172033')
SLATE = colors.HexColor('#536278')
MUTED = colors.HexColor('#E8EEF5')
PALE = colors.HexColor('#F5F8FB')
AMBER = colors.HexColor('#D98A00')
WHITE = colors.white

pdfmetrics.registerFont(TTFont('Arial', '/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))

styles = {
    'body': ParagraphStyle('body', fontName='Arial', fontSize=9.3, leading=13.2, textColor=INK),
    'small': ParagraphStyle('small', fontName='Arial', fontSize=7.8, leading=10.5, textColor=SLATE),
    'card': ParagraphStyle('card', fontName='Arial', fontSize=8.5, leading=11.5, textColor=INK),
    'white': ParagraphStyle('white', fontName='Arial', fontSize=9.2, leading=13, textColor=WHITE),
    'note': ParagraphStyle('note', fontName='Arial', fontSize=9.5, leading=13.5, textColor=INK),
}


def safe(text):
    return (text.replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', '-')
                .replace('\u00a0', ' '))


def para(c, text, x, y_top, width, style='body', height=300):
    p = Paragraph(safe(text), styles[style])
    _, h = p.wrap(width, height)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def header(c, number, title, kicker='AI DEPLOYMENT | OSINT ET NER'):
    c.setFont('Arial-Bold', 7.2)
    c.setFillColor(colors.HexColor('#60758E'))
    c.drawRightString(W - 34, H - 31, 'E.Cappaert, JC.Dorn, N.Segonds')
    c.setFont('Arial', 7.5)
    c.setFillColor(INK)
    c.drawString(19, 18, str(number))


def title(c, text, y=H-70, size=15.5):
    c.setFont('Arial-Bold', size)
    c.setFillColor(NAVY)
    c.drawString(34, y, safe(text))
    return y-25


def card(c, x, y, w, h, heading, body, accent=TEAL, value=None):
    c.setFillColor(PALE)
    c.setStrokeColor(colors.HexColor('#C8D7E6'))
    c.setLineWidth(.7)
    c.roundRect(x, y, w, h, 5, fill=1, stroke=1)
    c.setFont('Arial-Bold', 9)
    c.setFillColor(NAVY)
    c.drawString(x+14, y+h-20, safe(heading))
    if value:
        c.setFont('Arial-Bold', 19)
        c.setFillColor(accent)
        c.drawString(x+14, y+h-47, safe(value))
        para(c, body, x+14, y+h-57, w-27, 'small', h-55)
    else:
        para(c, body, x+14, y+h-31, w-27, 'card', h-35)


def image_fit(c, path, x, y, w, h, border=True):
    img = ImageReader(str(path))
    iw, ih = img.getSize()
    scale = min(w/iw, h/ih)
    dw, dh = iw*scale, ih*scale
    dx, dy = x + (w-dw)/2, y + (h-dh)/2
    c.drawImage(img, dx, dy, dw, dh, preserveAspectRatio=True, mask='auto')
    if border:
        c.setStrokeColor(colors.HexColor('#CBD5E1'))
        c.setLineWidth(.6)
        c.rect(dx, dy, dw, dh, fill=0, stroke=1)
    return dx, dy, dw, dh


def bullet_list(c, items, x, y, width, font=9.2, leading=13.6, bullet_color=TEAL):
    yy = y
    st = ParagraphStyle('bul', fontName='Arial', fontSize=font, leading=leading, textColor=INK,
                        leftIndent=12, firstLineIndent=-10, bulletIndent=0)
    for item in items:
        p = Paragraph(safe(item), st, bulletText='•')
        _, ph = p.wrap(width, 200)
        p.drawOn(c, x, yy-ph)
        yy -= ph + 4
    return yy


def draw_cover(c):
    c.setFont('Arial-Bold', 7.2)
    c.setFillColor(colors.HexColor('#60758E'))
    c.drawRightString(W-34, H-31, 'E.Cappaert, JC.Dorn, N.Segonds')
    c.setFillColor(NAVY)
    c.setFont('Arial-Bold', 24)
    c.drawCentredString(W/2, H-245, 'Livrable final')
    c.setFont('Arial', 13)
    c.setFillColor(colors.HexColor('#30415B'))
    c.drawCentredString(W/2, H-282, 'AI Deployment - veille OSINT militaire')
    c.drawCentredString(W/2, H-302, 'NER, Elasticsearch et dashboards analytiques')
    boxes = [
        ('Périmètre', 'Corpus TASS, extraction d’entités militaires, indexation et visualisation.'),
        ('Dataset', '20 895 articles publiés entre 2015 et 2025.'),
        ('Stack', 'Python, spaCy NER, Elasticsearch et Kibana.'),
        ('Dépôt GitHub', 'github.com/edcdataworker/ai-deployment-osint'),
    ]
    y = H-380
    for label, body in boxes:
        c.setFillColor(PALE)
        c.setStrokeColor(colors.HexColor('#C8D7E6'))
        c.roundRect(38, y, W-76, 31, 5, fill=1, stroke=1)
        c.setFont('Arial-Bold', 8.5)
        c.setFillColor(INK)
        c.drawString(47, y+11, safe(label + ' :'))
        c.setFont('Arial', 8.5)
        c.drawString(111, y+11, safe(body))
        y -= 48
    c.setFont('Arial', 7.5)
    c.setFillColor(INK)
    c.drawString(19, 18, '1')


def draw_summary(c):
    header(c, 2, 'Synthèse exécutive')
    y = title(c, 'Ce que montre le corpus')
    para(c,
         '<b>Le dispositif transforme un corpus d’articles en indicateurs interrogeables.</b> Le modèle NER classe les mentions en trois catégories opérationnelles - WEAPON, MIL_UNIT et MIL_ORG - puis Elasticsearch agrège les résultats dans Kibana. Les tableaux de bord rendent visibles le volume, la temporalité, la concentration des entités et la distribution par article.',
         34, y, W-68, 'body')
    cy = H-276
    gap = 10
    cw = (W-68-2*gap)/3
    card(c, 34, cy, cw, 102, 'Armes', 'Soit 31,2 % des mentions d’entités et 1,99 mention par article en moyenne.', TEAL, '41 665')
    card(c, 34+cw+gap, cy, cw, 102, 'Unités', 'Soit 14,3 % des mentions et 0,91 mention par article en moyenne.', colors.HexColor('#6F87D8'), '19 116')
    card(c, 34+2*(cw+gap), cy, cw, 102, 'Organisations', 'Soit 54,5 % des mentions et 3,49 mentions par article en moyenne.', colors.HexColor('#55BD7B'), '72 816')
    c.setFont('Arial-Bold', 12)
    c.setFillColor(NAVY)
    c.drawString(34, cy-37, 'Constats clés')
    bullet_list(c, [
        '<b>Forte domination des organisations.</b> Plus d’une mention d’entité sur deux relève de MIL_ORG, ce qui reflète un cadrage institutionnel très présent dans les dépêches.',
        '<b>Concentration des systèmes d’armes.</b> S-400 domine nettement le classement ; le premier élément est plus de deux fois au-dessus du suivant dans la capture.',
        '<b>Pic de production en 2023.</b> Le volume annuel d’articles atteint son maximum visible autour de 4 400, avant de refluer en 2024-2025.',
        '<b>Distribution très asymétrique.</b> Beaucoup d’articles ne citent aucune arme ; une minorité en cite un grand nombre, jusqu’à près de 40.'
    ], 34, cy-56, W-68)
    c.setFillColor(PALE)
    c.setStrokeColor(colors.HexColor('#C8D7E6'))
    c.roundRect(34, 64, W-68, 52, 5, fill=1, stroke=1)
    para(c, '<b>Précaution :</b> ces métriques décrivent les mentions produites par TASS. Elles ne mesurent ni l’emploi réel d’un équipement, ni l’ordre de bataille, ni la véracité des affirmations.', 48, 102, W-96, 'small')


def draw_sources(c):
    header(c, 3, 'Périmètre et chaîne de traitement')
    y = title(c, 'Sources, code et méthode')
    c.setFont('Arial-Bold', 11)
    c.setFillColor(NAVY)
    c.drawString(34, y, 'Accès au code')
    c.setFillColor(PALE)
    c.roundRect(34, y-96, W-68, 78, 8, fill=1, stroke=0)
    para(c, '<b>Dépôt GitHub du projet</b><br/><link href="https://github.com/edcdataworker/ai-deployment-osint" color="#0F5C8E">https://github.com/edcdataworker/ai-deployment-osint</link>', 48, y-34, W-96, 'card')
    c.setFillColor(PALE)
    c.setStrokeColor(colors.HexColor('#C8D7E6'))
    c.roundRect(34, y-147, W-68, 37, 5, fill=1, stroke=1)
    para(c, '<b>Notebook Colab</b> - <link href="https://colab.research.google.com/drive/1wE2RMIx62Ic95o7bkGo29yfDAV7svlRQ?authuser=1" color="#0F5C8E">ouvrir le notebook de travail</link>. Le dépôt contient le livrable, son générateur et les captures.', 48, y-121, W-96, 'small')
    c.setFont('Arial-Bold', 11)
    c.setFillColor(NAVY)
    c.drawString(34, y-184, 'Pipeline fonctionnel')
    steps = [
        ('1', 'Extraction', 'Parser articles.json, isoler le texte et conserver le découpage par article.'),
        ('2', 'Annotation', 'Pré-annoter, valider manuellement les offsets et appliquer le schéma à 3 labels.'),
        ('3', 'Entraînement', 'Convertir en DocBin, séparer train/dev et adapter en_core_web_sm.'),
        ('4', 'Inférence', 'Appliquer le modèle retenu et regrouper les entités par type pour chaque article.'),
        ('5', 'Indexation', 'Indexer texte, date et entités structurées dans Elasticsearch puis visualiser dans Kibana.'),
    ]
    yy = y-213
    for num, head, body in steps:
        c.setFillColor(TEAL)
        c.circle(52, yy-8, 13, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Arial-Bold', 9)
        c.drawCentredString(52, yy-11, num)
        c.setFillColor(NAVY)
        c.setFont('Arial-Bold', 9.5)
        c.drawString(78, yy, head)
        para(c, body, 78, yy-8, W-112, 'small', 40)
        if num != '5':
            c.setStrokeColor(colors.HexColor('#B8C6D6'))
            c.line(52, yy-22, 52, yy-47)
        yy -= 62
    c.setFillColor(PALE)
    c.roundRect(34, 55, W-68, 77, 8, fill=1, stroke=0)
    para(c, '<b>Choix d’architecture.</b> Un NER spécialisé offre une inférence locale, rapide, déterministe et structurée. Elasticsearch déporte les agrégations côté serveur ; Kibana permet de composer les vues sans recoder l’analyse. Cette séparation facilite la traçabilité : article source, entités détectées, index et visualisation restent auditables.', 48, 116, W-96, 'card')


def draw_global_dashboard(c):
    header(c, 4, 'Dashboard 1 - Vue globale')
    y = title(c, 'Volumes, temporalité et structure des entités')
    image_fit(c, IMG1, 34, 420, W-68, 230)
    c.setFont('Arial-Bold', 11)
    c.setFillColor(NAVY)
    c.drawString(34, 396, 'Lecture des métriques')
    bullet_list(c, [
        '<b>133 597 mentions d’entités</b> sont extraites des 20 895 articles, soit 6,39 mentions par article en moyenne.',
        '<b>MIL_ORG est majoritaire (54,5 %)</b>, devant WEAPON (31,2 %) et MIL_UNIT (14,3 %). La tarte donne immédiatement la structure du corpus.',
        '<b>La série annuelle contextualise les volumes.</b> Elle augmente de 520 articles en 2015 à un sommet proche de 4 400 en 2023, puis décroît.',
        '<b>Le filtre temporel global</b> rend tous les indicateurs cohérents et permet une comparaison de périodes sans multiplier les tableaux.'
    ], 34, 375, W-68)
    card(c, 34, 65, (W-78)/2, 85, 'Pourquoi cette vue ?', 'Elle répond en quelques secondes à trois questions : combien d’articles, combien d’entités et comment la couverture évolue-t-elle ?', TEAL)
    card(c, 44+(W-78)/2, 65, (W-78)/2, 85, 'Point de vigilance', 'Une hausse de volume éditorial augmente mécaniquement les mentions. Pour mesurer l’intensité, il faut aussi normaliser par article.', AMBER)


def draw_rankings(c):
    header(c, 5, 'Dashboard 2 - Classements et distribution')
    y = title(c, 'Entités dominantes et asymétrie du corpus')
    image_fit(c, IMG2, 34, 330, W-68, 350)
    c.setFont('Arial-Bold', 11)
    c.setFillColor(NAVY)
    c.drawString(34, 307, 'Interprétation')
    bullet_list(c, [
        '<b>S-400 domine les systèmes d’armes</b> avec environ 1 800 mentions visibles, très loin devant le deuxième terme. Cette concentration justifie un suivi spécifique dans le temps.',
        '<b>Northern Fleet arrive en tête des unités</b> avec environ 1 550 mentions. Le classement décroît ensuite régulièrement, ce qui signale un noyau restreint d’unités très médiatisées.',
        '<b>Russian Defense Ministry domine les organisations</b> avec plus de 5 000 mentions. Ce résultat est cohérent avec la nature institutionnelle et étatique de la source.',
        '<b>La distribution du nombre d’armes par article est fortement inclinée.</b> Le mode est à zéro ; la moyenne de 1,99 est tirée vers le haut par une longue traîne d’articles très chargés.'
    ], 34, 289, W-68, font=8.8, leading=12.7)
    c.setFillColor(PALE)
    c.setStrokeColor(colors.HexColor('#C8D7E6'))
    c.roundRect(34, 55, W-68, 54, 5, fill=1, stroke=1)
    para(c, '<b>Choix de dashboard :</b> les barres horizontales conviennent aux libellés longs et rendent le rang évident. L’histogramme complète les tops : il montre la forme de la population et évite de confondre quelques articles extrêmes avec le comportement typique.', 48, 96, W-96, 'small')


def draw_year_table(c):
    header(c, 6, 'Dashboard 3 - Contrôle temporel')
    y = title(c, 'Table de synthèse par année')
    image_fit(c, IMG3, 34, 560, W-68, 140)
    c.setFont('Arial-Bold', 11)
    c.setFillColor(NAVY)
    c.drawString(34, 535, 'Ratios calculés sur les lignes visibles')
    data = [
        ['Année', 'Armes/article', 'Unités/article', 'Orgs/article'],
        ['2015', '2,94', '0,98', '4,30'],
        ['2016', '2,24', '0,96', '3,84'],
        ['2017', '2,32', '0,77', '3,73'],
        ['2018', '2,44', '0,81', '3,70'],
        ['2019', '3,10', '1,10', '3,59'],
        ['Corpus complet', '1,99', '0,91', '3,49'],
    ]
    t = Table(data, colWidths=[110, 120, 120, 120], rowHeights=27)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),NAVY), ('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Arial-Bold'), ('FONTNAME',(0,1),(0,-1),'Arial-Bold'),
        ('FONTNAME',(1,1),(-1,-1),'Arial'), ('FONTSIZE',(0,0),(-1,-1),8.5),
        ('ALIGN',(1,1),(-1,-1),'CENTER'), ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('GRID',(0,0),(-1,-1),.5,colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,PALE]),
        ('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#E7F7F5')),
        ('TEXTCOLOR',(0,-1),(-1,-1),TEAL_DARK),
    ]))
    t.wrapOn(c, W-68, 220)
    t.drawOn(c, 34, 318)
    c.setFont('Arial-Bold', 11)
    c.setFillColor(NAVY)
    c.drawString(34, 292, 'Ce que les ratios ajoutent')
    bullet_list(c, [
        'Les volumes bruts répondent à « combien ? » ; les ratios répondent à « avec quelle densité éditoriale ? ».',
        '2019 combine, sur les lignes visibles, la plus forte densité d’armes (3,10) et d’unités (1,10) par article.',
        'La baisse des organisations par article de 2015 à 2019 peut refléter un changement de cadrage, mais elle doit être testée sur toute la période.',
        'Le tableau est aussi un contrôle qualité : une année absente, un ratio aberrant ou une rupture brutale devient immédiatement détectable.'
    ], 34, 273, W-68, font=8.7, leading=12.6)
    para(c, '<b>Note :</b> la capture pagine les années ; seules les lignes 2015-2019 et le total sont visibles. Les ratios ci-dessus sont calculés à partir de ces valeurs affichées, sans extrapolation des années masquées.', 34, 82, W-68, 'small')


def draw_design(c):
    header(c, 7, 'Choix analytiques et qualité')
    y = title(c, 'Pourquoi ces dashboards sont utiles')
    rows = [
        ['Vue', 'Question traitée', 'Décision facilitée', 'Limite principale'],
        ['KPI globaux', 'Quel est le volume traité ?', 'Vérifier couverture et ingestion', 'Les comptes ne mesurent pas la qualité'],
        ['Série annuelle', 'Quand la couverture change-t-elle ?', 'Isoler les périodes à examiner', 'Effet volume de publication'],
        ['Donut par label', 'Quel type d’entité domine ?', 'Comprendre le cadrage du corpus', 'Dépend du schéma d’annotation'],
        ['Top entités', 'Qui ou quoi est le plus cité ?', 'Prioriser les investigations', 'Biais vers les variantes fréquentes'],
        ['Distribution/article', 'Quelle est la forme des détections ?', 'Repérer zéros et valeurs extrêmes', 'Ne dit rien sur la pertinence'],
        ['Table annuelle', 'Les totaux sont-ils cohérents ?', 'Auditer et exporter', 'Pagination dans la capture'],
    ]
    t = Table(rows, colWidths=[87, 135, 145, 155], rowHeights=[30]+[48]*6)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),NAVY), ('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Arial-Bold'), ('FONTNAME',(0,1),(0,-1),'Arial-Bold'),
        ('FONTNAME',(1,1),(-1,-1),'Arial'), ('FONTSIZE',(0,0),(-1,-1),7.4),
        ('LEADING',(0,0),(-1,-1),9.5), ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(0,0),(-1,-1),6), ('RIGHTPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),.45,colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,PALE]),
    ]))
    t.wrapOn(c, W-68, 400)
    t.drawOn(c, 34, 414)
    c.setFont('Arial-Bold', 11)
    c.setFillColor(NAVY)
    c.drawString(34, 385, 'Améliorations recommandées')
    bullet_list(c, [
        '<b>Normaliser</b> chaque série en mentions pour 100 articles afin de séparer activité éditoriale et intensité lexicale.',
        '<b>Ajouter un indicateur de qualité NER</b> sur le jeu dev : précision, rappel, F1 par label et matrice de confusion.',
        '<b>Normaliser les alias</b> (sigles, translittérations, variantes) avant les agrégations pour éviter la fragmentation des tops.',
        '<b>Créer une vue de co-occurrence</b> WEAPON x MIL_UNIT et un drill-down vers les articles sources pour validation analyste.',
        '<b>Afficher la couverture et la date de collecte</b> afin d’éviter de lire une année partielle comme une baisse opérationnelle.'
    ], 34, 364, W-68, font=8.7, leading=12.8)
    card(c, 34, 59, W-68, 72, 'Critère de réussite', 'Un bon dashboard n’est pas seulement lisible : chaque agrégation doit permettre de revenir au texte source, de vérifier une détection et de distinguer fréquence médiatique, qualité du modèle et réalité opérationnelle.', TEAL)


def draw_intel_note(c):
    header(c, 8, 'Note de renseignement')
    y = title(c, 'TASS : cadrage militaire dominant et pic éditorial en 2023', size=17.5)
    c.setFillColor(PALE)
    c.setStrokeColor(colors.HexColor('#C8D7E6'))
    c.roundRect(34, y-105, W-68, 86, 5, fill=1, stroke=1)
    para(c, '<b>Appréciation</b><br/>Le corpus fait apparaître une communication fortement institutionnelle, structurée autour d’un petit nombre d’organisations et de systèmes d’armes très cités. Le volume d’articles culmine en 2023, tandis que les organisations représentent 54,5 % de toutes les mentions d’entités.', 50, y-38, W-100, 'body')
    yy = y-143
    sections = [
        ('Éléments observés', [
            '20 895 articles couvrent la période 2015-2025 ; 133 597 mentions d’entités sont détectées.',
            'Russian Defense Ministry domine le classement des organisations ; S-400 domine celui des armes ; Northern Fleet celui des unités.',
            'La distribution des armes par article est très asymétrique : de nombreux zéros coexistent avec une longue traîne.'
        ]),
        ('Analyse', [
            'La prépondérance des organisations est compatible avec une production de dépêches centrée sur les annonces officielles, les porte-parole et les institutions militaires.',
            'La surreprésentation d’un système comme S-400 peut signaler une priorité narrative ou diplomatique autant qu’un intérêt opérationnel.',
            'Le pic de 2023 indique une intensification de la couverture ; il ne suffit pas, seul, à conclure à une intensification militaire.'
        ]),
        ('Niveau de confiance', [
            '<b>Modéré.</b> Les constats quantitatifs sont directement visibles dans les dashboards. L’interprétation reste limitée par le biais éditorial de TASS, la qualité non documentée du NER et l’absence de triangulation avec d’autres sources.'
        ]),
        ('Indicateurs à surveiller', [
            'Rupture de tendance des mentions normalisées par article ; apparition d’une nouvelle arme ou unité dans le top 20 ; hausse de co-occurrences arme-unité ; divergence entre TASS et sources indépendantes.'
        ])
    ]
    for heading, items in sections:
        c.setFont('Arial-Bold', 10.5)
        c.setFillColor(TEAL_DARK)
        c.drawString(34, yy, heading)
        yy = bullet_list(c, items, 34, yy-15, W-68, font=8.8, leading=12.7)
        yy -= 7
    c.setFillColor(PALE)
    c.setStrokeColor(colors.HexColor('#C8D7E6'))
    c.roundRect(34, 56, W-68, 52, 5, fill=1, stroke=1)
    para(c, '<b>Jugement analytique :</b> les dashboards constituent un outil de veille et de détection de signaux. Toute conclusion opérationnelle doit être confirmée par lecture des articles, contrôle du modèle et confrontation à des sources distinctes.', 48, 96, W-96, 'small')


def draw_limits(c):
    header(c, 9, 'Limites et conclusion')
    y = title(c, 'Un dispositif utile, à condition de rester auditable')
    cols = [
        ('Source', 'TASS est un média d’État russe. Les thèmes, omissions, cadrages et volumes relèvent d’une ligne éditoriale.'),
        ('Modèle', 'Sans précision, rappel et F1 sur un jeu dev validé, un volume de détections ne prouve pas la qualité du NER.'),
        ('Comptage', 'Une mention n’est ni une entité unique, ni un événement. Les répétitions dans un même article peuvent gonfler les totaux.'),
        ('Temporalité', 'Une année partielle ou un changement de collecte peut produire une rupture artificielle dans la série.'),
        ('Normalisation', 'Les alias et variantes linguistiques peuvent fragmenter une même entité en plusieurs barres.'),
        ('Interprétation', 'Les tops mesurent la visibilité dans la source, pas l’importance opérationnelle réelle.'),
    ]
    gap=12
    cw=(W-68-gap)/2
    yy=y-8
    for i,(h,b) in enumerate(cols):
        x=34+(i%2)*(cw+gap)
        row=i//2
        cy=yy-row*117-94
        card(c,x,cy,cw,94,h,b,TEAL if i%2==0 else colors.HexColor('#6F87D8'))
    c.setFont('Arial-Bold', 12)
    c.setFillColor(NAVY)
    c.drawString(34, 350, 'Conclusion')
    para(c,
         'La chaîne proposée répond au besoin du TP : elle convertit un corpus brut en objets structurés, indexables et exploitables. Les trois dashboards couvrent les niveaux complémentaires de l’analyse : vue d’ensemble, classement des entités et contrôle temporel. Les résultats mettent en évidence un corpus dominé par les organisations, un pic d’activité éditoriale en 2023 et une forte concentration de certaines entités. La valeur du dispositif tient surtout à sa capacité de filtrage et de retour au document source ; son usage renseignement doit rester prudent, traçable et triangulé.',
         34, 330, W-68, 'body')
    c.setFillColor(PALE)
    c.setStrokeColor(colors.HexColor('#C8D7E6'))
    c.roundRect(34, 164, W-68, 94, 5, fill=1, stroke=1)
    para(c, '<b>Livrable conforme aux éléments de la page 21</b><br/>1. lien vers le code fourni ; 2. trois captures de dashboards ; 3. analyse des métriques et justification des vues ; 4. note de renseignement courte.', 50, 236, W-100, 'body')
    c.setFillColor(PALE)
    c.setStrokeColor(colors.HexColor('#C8D7E6'))
    c.roundRect(34, 75, W-68, 67, 5, fill=1, stroke=1)
    para(c, '<b>Dépôt du projet :</b> <link href="https://github.com/edcdataworker/ai-deployment-osint" color="#0F5C8E">https://github.com/edcdataworker/ai-deployment-osint</link>. Le notebook Colab reste référencé dans le README.', 48, 126, W-96, 'note')


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
    c.setTitle('Livrable AI Deployment - OSINT, NER et dashboards')
    c.setAuthor('Edouard Cappaert')
    pages = [draw_cover, draw_summary, draw_sources, draw_global_dashboard,
             draw_rankings, draw_year_table, draw_design, draw_intel_note, draw_limits]
    for fn in pages:
        fn(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == '__main__':
    build()
