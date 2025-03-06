
from collections import Counter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from Database import Aluno, Transcrição, Correção
from getAnalysis import getOcurrence, getParticipation
import nltk

# Régua para auxiliar na criação do PDF
def drawMyRuler(canvas_obj):
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setStrokeColor(colors.black)
    canvas_obj.drawString(100, 810, 'x100')
    canvas_obj.drawString(200, 810, 'x200')
    canvas_obj.drawString(300, 810, 'x300')
    canvas_obj.drawString(400, 810, 'x400')
    canvas_obj.drawString(500, 810, 'x500')
    canvas_obj.drawString(100, 800, 'y800')
    canvas_obj.drawString(100, 700, 'y700')
    canvas_obj.drawString(100, 600, 'y600')
    canvas_obj.drawString(100, 500, 'y500')
    canvas_obj.drawString(100, 400, 'y400')
    canvas_obj.drawString(100, 300, 'y300')
    canvas_obj.drawString(100, 200, 'y200')
    canvas_obj.drawString(100, 100, 'y100')

# Tabela de participação 
def table(c, rect_x, rect_y, student_participation, rect_width, rect_height):
    bar_width = 30
    bar_gap = 10
    max_height = 200  
    table_width = len(student_participation) * (bar_width + bar_gap)

    table_x = rect_x + (rect_width - table_width) / 2
    table_y = 260

    # Barras de participação
    for i, participation in enumerate(student_participation):
        bar_height = max_height * (participation / 100)
        bar_x = table_x + (i * (bar_width + bar_gap))
        c.setFillColor(colors.HexColor("#f1457e"))
        c.rect(bar_x, table_y, bar_width, bar_height, fill=True, stroke=False)
        
        number_y = table_y - 10 
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        c.drawString(bar_x + (bar_width / 2) - 13, number_y, f"{participation:.1f}%")  
    
    # Média de participação
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    avg_participation = sum(student_participation) / len(student_participation)
    c.drawString(table_x + table_width + 20, table_y - 15, f"Avg: {avg_participation:.1f}%")
    
    # Comparação de participação
    if len(student_participation) > 1:
        last_participation = student_participation[-1]
        prev_participation = student_participation[-2]
        if last_participation > prev_participation:
            participation_message = "Your participation has increased compared to previous weeks. Keep it up!"
        elif last_participation < prev_participation:
            participation_message = "You participated a bit less this time. Try to engage more during classes!"
        else:
            participation_message = "Your participation has remained steady. Keep it up, consistency is key!"
        c.drawString(rect_x + 10, table_y - 40, participation_message)

def create_pdf(file_name, student_name):
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    # Background
    c.setFillColor(colors.HexColor("#e8e2ee"))
    c.rect(0, 0, width, height, fill=True)

    # Header
    header_height = 80
    c.setFillColor(colors.HexColor("#400e72"))
    c.rect(0, height - header_height, width, header_height, fill=True)

    logo_path = "Assets/Images/geoenglish.PNG"
    logo_width = 60
    logo_height = 60
    c.drawImage(logo_path, 20, height - logo_height - 10, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')

    title = 'MONTHLY REPORT' 
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor("#f1457e"))
    title_width = c.stringWidth(title, "Helvetica-Bold", 24)
    c.drawString((width - title_width) / 2, height - header_height + 25, title)

    # Seções
    rect_x = 50
    rect_y = 100
    rect_width = width - 100
    rect_height = (height - 350) / 2
    section_titles = ["Repeated mistakes", "Participation"]

    for i, section in enumerate(section_titles):
        y_position = height - 150 - (i * rect_height)
        c.setFillColor(colors.HexColor("#e8e2ee"))
        c.rect(rect_x, y_position, rect_width, -rect_height, fill=True, stroke=True)

        # Título das seções
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(rect_x + 10, y_position - 20, section)

        if section == "Repeated mistakes":
            errors = getOcurrence(student_name)
            c.setFont("Helvetica-BoldOblique", 12)
            error_text = ", ".join(errors) if errors else "No frequent errors detected."
            c.drawString(rect_x + 10, y_position - 40, error_text)
            c.setFont("Helvetica", 12)
            c.drawString(rect_x + 10, y_position - 70, "In the last few weeks, you've been making some repeated mistakes!")
            c.drawString(rect_x + 10, y_position - 90, "Don't worry, this is part of the learning process.")
            c.drawString(rect_x + 10, y_position - 110, "In the student portal, you will soon find activities to help you overcome these challenges!")
            
        
        if section == "Participation":
            participation = getParticipation(student_name)
            if participation:
                table(c, rect_x, rect_y, participation, rect_width, rect_height)
            else:
                c.setFont("Helvetica", 12)
                c.drawString(rect_x + 10, y_position - 40, "No participation data available.")

    #drawMyRuler(c)
    c.save()

if __name__ == "__main__":
    create_pdf("monthly_report.pdf", 'Yuri De Oliveira Magalhães')
