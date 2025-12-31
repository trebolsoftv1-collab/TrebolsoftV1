# sync-forced-2025
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

infile = 'docs/render_setup_instructions.md'
outfile = 'docs/render_setup_instructions.pdf'

styles = getSampleStyleSheet()
story = []

with open(infile, 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

for line in lines:
    if line.strip() == '':
        story.append(Spacer(1, 6))
        continue
    # Simple markdown-ish handling
    if line.startswith('# '):
        story.append(Paragraph(line[2:].strip(), styles['Title']))
    elif line.startswith('## '):
        story.append(Paragraph(line[3:].strip(), styles['Heading2']))
    elif line.startswith('### '):
        story.append(Paragraph(line[4:].strip(), styles['Heading3']))
    else:
        story.append(Paragraph(line.replace('`', ''), styles['Normal']))

    story.append(Spacer(1, 6))

pdf = SimpleDocTemplate(outfile, pagesize=A4)
pdf.build(story)
print('Wrote', outfile)
