from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import ListFlowable, ListItem
from reportlab.platypus import HRFlowable
from reportlab.lib.styles import ListStyle
from reportlab.platypus import Preformatted
from reportlab.platypus import PageBreak
import os
import re

def generate_pdf(content):
    file_path = "ATS_Report.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    # Split lines
    lines = content.split("\n")

    for line in lines:
        if line.strip() == "":
            elements.append(Spacer(1, 0.2 * inch))
        elif "ATS SCORE" in line:
            elements.append(Paragraph(f"<b>{line}</b>", styles["Heading1"]))
        elif line.endswith(":"):
            elements.append(Paragraph(f"<b>{line}</b>", styles["Heading2"]))
        elif line.startswith("-"):
            elements.append(Paragraph(line, styles["Normal"]))
        else:
            elements.append(Paragraph(line, styles["Normal"]))

    doc.build(elements)
    return file_path
