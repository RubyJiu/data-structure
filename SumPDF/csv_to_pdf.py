import pandas as pd
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import cm

csv_file = "customer_support_intro_dataset.csv"
pdf_file = "customer_support_intro_dataset.pdf"

df = pd.read_csv(csv_file)

doc = SimpleDocTemplate(
    pdf_file,
    pagesize=landscape(A4),
    leftMargin=0.5 * cm,
    rightMargin=0.5 * cm,
    topMargin=0.5 * cm,
    bottomMargin=0.5 * cm
)

styles = getSampleStyleSheet()
elements = []

# Data with paragraph formatting for wrapping
data = [df.columns.tolist()] + df.values.tolist()
formatted_data = [[Paragraph(str(cell), styles["Normal"]) for cell in row] for row in data]

column_widths = [4 * cm, 8.5 * cm] + [1.875 * cm] * (len(df.columns) - 2)

table = Table(formatted_data, repeatRows=1, colWidths=column_widths)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 6),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
]))

elements.append(table)
doc.build(elements)

print(f"Final PDF generated without column cutoff: {pdf_file}")
