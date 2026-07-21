from pathlib import Path
import fitz


SOURCE = Path('/Users/ed/Desktop/Docker/Rendu_AI_Deployment_FINAL.pdf')
OUTPUT = Path('/Users/ed/Desktop/Docker/output/pdf/Rendu_AI_Deployment_FINAL.pdf')

GITHUB = 'https://github.com/edcdataworker/ai-deployment-osint'
COLAB = 'https://colab.research.google.com/drive/1wE2RMIx62Ic95o7bkGo29yfDAV7svlRQ?usp=sharing'
KIBANA = 'https://my-elasticsearch-project-aed731.kb.eu-west-1.aws.elastic.cloud/app/dashboards#/view/dash-tass-v3'


def add_cell_text(page, rect, text, bold=False, color=(0.08, 0.10, 0.16), size=8.2):
    page.insert_textbox(
        rect,
        text,
        fontname='hebo' if bold else 'helv',
        fontsize=size,
        lineheight=1.25,
        color=color,
        align=fitz.TEXT_ALIGN_LEFT,
    )


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(SOURCE)
    page = doc[3]

    # Replace the original two-row source table and its explanatory paragraph.
    clean = fitz.Rect(64, 505, 536, 668)
    page.add_redact_annot(clean, fill=(1, 1, 1))
    page.apply_redactions()

    left, split, right = 68, 208, 527
    top = 511
    heights = [34, 43, 43]
    labels = ['Dépôt GitHub', 'Notebook Google Colab', 'Dashboard Kibana']
    urls = [GITHUB, COLAB, KIBANA]
    fills = [(0.96, 0.79, 0.80), (0.95, 0.95, 0.95), (0.96, 0.79, 0.80)]
    border = (0.80, 0.80, 0.80)
    burgundy = (0.50, 0.06, 0.16)
    blue = (0.02, 0.27, 0.54)

    y = top
    link_rects = []
    for height, label, url, fill in zip(heights, labels, urls, fills):
        row = fitz.Rect(left, y, right, y + height)
        label_rect = fitz.Rect(left, y, split, y + height)
        value_rect = fitz.Rect(split, y, right, y + height)
        page.draw_rect(row, color=border, width=0.55)
        page.draw_rect(label_rect, color=border, fill=fill, width=0.55)
        page.draw_line((split, y), (split, y + height), color=border, width=0.55)
        add_cell_text(page, fitz.Rect(left + 7, y + 8, split - 5, y + height - 4), label, bold=True, color=burgundy, size=8.2)
        add_cell_text(page, fitz.Rect(split + 6, y + 7, right - 6, y + height - 3), url, color=blue, size=7.6)
        link_rects.append((fitz.Rect(split + 4, y + 3, right - 4, y + height - 3), url))
        y += height

    explanation = (
        "Le dépôt GitHub centralise le livrable, les captures et le script de génération. "
        "Le notebook Colab contient l'intégralité du pipeline : extraction, annotation LLM, "
        "fine-tuning spaCy, inférence et ingestion Elasticsearch."
    )
    page.insert_textbox(
        fitz.Rect(68, y + 15, 527, y + 60),
        explanation,
        fontname='helv',
        fontsize=8.4,
        lineheight=1.35,
        color=(0.08, 0.08, 0.08),
        align=fitz.TEXT_ALIGN_JUSTIFY,
    )

    for rect, uri in link_rects:
        page.insert_link({'kind': fitz.LINK_URI, 'from': rect, 'uri': uri})

    metadata = doc.metadata
    metadata.update({
        'title': 'Rendu AI Deployment FINAL',
        'author': 'Jean-Christophe Dorn, Noah Segonds, Edouard Cappaert',
        'subject': 'TASS NER Pipeline - AI Deployment',
    })
    doc.set_metadata(metadata)
    doc.save(OUTPUT, garbage=4, deflate=True, clean=True)
    doc.close()
    print(OUTPUT)


if __name__ == '__main__':
    build()
