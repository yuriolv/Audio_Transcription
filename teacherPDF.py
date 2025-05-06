from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.units import cm
from Database.Reports import ReportsCRUD
from reportlab.lib.styles import getSampleStyleSheet

def create_teacher_pdf(file_name, data):
    doc = SimpleDocTemplate(file_name, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    title_style = styles['Heading2']
    field_style = styles['Normal']

    # Header
    def draw_header(canvas_obj, doc):
        width, height = A4
        canvas_obj.setFillColor(colors.HexColor('#e8e2ee'))
        canvas_obj.rect(0, 0, width, height, fill=True)

        canvas_obj.setFillColor(colors.HexColor('#40848c'))
        canvas_obj.rect(0, height - 80, width, 80, fill=True)

        logo_path = "Assets/Images/image5.png"
        canvas_obj.drawImage(logo_path, 20, height - 90 + 10, width=100, height=90, preserveAspectRatio=True, mask='auto')

        canvas_obj.setFont("Helvetica-Bold", 24)
        canvas_obj.setFillColor(colors.HexColor('#fefefe'))
        canvas_obj.drawString(200, height - 50, "CLASS REPORT")

    # Informações
    for i, row in enumerate(data):
        elements.append(Paragraph(f"Report #{i+1}", title_style))
        elements.append(Paragraph(f"<b>Name:</b> {row[0]}", field_style))
        elements.append(Paragraph(f"<b>Class participation:</b> {row[1]}", field_style))
        elements.append(Paragraph(f"<b>Report date:</b> {row[2]}", field_style))
        elements.append(Paragraph(f"<b>Repeated mistakes:</b> {row[3]}", field_style))
        elements.append(Paragraph(f"<b>English percentage:</b> {row[4]}", field_style))
        elements.append(Paragraph(f"<b>Behavioral state:</b> {row[5]}", field_style))
        elements.append(Spacer(1, 20))

    doc.build(elements, onFirstPage=draw_header, onLaterPages=draw_header)


if __name__ == "__main__":
    reports = ReportsCRUD("language_school.db")
    result = reports.read_reports()
    create_teacher_pdf("class_report.pdf", result)