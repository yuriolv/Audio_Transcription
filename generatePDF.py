import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from collections import Counter
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from getAnalysis import getOcurrence, getParticipation, getLanguage, getPhraseLength, getSentimental
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

# Criação do gráfico 
def create_speedometer(percentage, output_path = "Assets/Images/speedometer.png"):
    print("Creating speedometer...")
    fig, ax = plt.subplots(figsize=(4, 2), subplot_kw={'projection': 'polar'})
    
    colors = ['#882577', '#631974', '#440c74'] # Baixo, médio de alto (em relação ao uso do inglês)
    ranges = [33, 66, 100]
    
    fig.patch.set_facecolor("#e8e2ee")
    ax.set_facecolor("#e8e2ee")
    
    # Converte a porcentagem para radiano
    rad = np.deg2rad(180 * (percentage / 100))
    
    ax.set_theta_zero_location("W")  # Faz o velocímetro ficar na horizontal
    ax.set_theta_direction(-1)
    
    # Background
    start_angle = 0
    for i in range(len(ranges)):
        end_angle = np.deg2rad(180 * (ranges[i] / 100))
        ax.barh(y=1, width=end_angle - start_angle, left=start_angle, 
                color=colors[i], height=0.5, edgecolor="black")
        start_angle = end_angle  # Atualiza para a próxima seção
    
    # Agulha
    ax.plot([0, rad], [0, 1], color = 'black', linewidth=2, marker='o')
    
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['polar'].set_visible(False)
    
    fig.patch.set_facecolor("#e8e2ee")
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    print(f"Speedometer saved at: {output_path}")
    plt.close()

def add_to_pdf(c, percentage):
    speedometer_path = "Assets/Images/speedometer.png"
    c.drawImage(speedometer_path, 190, 212, width=200, height=100)

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

def create_pdf(file_name, student_id):
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
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#f1457e"))
    student_width = c.stringWidth(student_id, "Helvetica-Bold", 14)
    c.drawString((width - student_width) / 2, height - header_height + 5, student_id)

    # Seções
    rect_x = 50
    rect_y = 100
    rect_width = width - 100
    rect_height = (height - 250) / 4
    section_titles = ["Repeated mistakes", "Participation", "Your main language", "How much are you speaking?"]

    for i, section in enumerate(section_titles):
        y_position = height - 150 - (i * rect_height)
        c.setFillColor(colors.HexColor("#e8e2ee"))
        c.rect(rect_x, y_position, rect_width, -rect_height, fill=True, stroke=True)

        # Título das seções
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(rect_x + 10, y_position - 20, section)

        if section == "Repeated mistakes":
            errors = getOcurrence(student_id)
            c.setFont("Helvetica", 12)
            
            if errors:
                y_offset = y_position - 40
                y_offset -= 20
                c.setFont("Helvetica-Bold", 12)

                for frase, erro in errors:
                    formatted_text = f"{frase} → {erro}"
                    c.setFont("Helvetica", 12)
                    
                    if y_offset < rect_y + 20:
                        c.drawString(rect_x + 10, y_offset, "More errors are available in the full report.")
                        break

                    c.drawString(rect_x + 10, y_offset, formatted_text)
                    y_offset -= 20 
            else:
                c.drawString(rect_x + 10, y_position - 40, "No frequent errors detected.")
            
        
        if section == "Participation":
            participation = getParticipation(student_id)
            if participation:
                table(c, rect_x, rect_y, participation, rect_width, rect_height)
            else:
                c.setFont("Helvetica", 12)
                c.drawString(rect_x + 10, y_position - 40, "No participation data available.")
        
        
        if section == "Your main language":
            eng_percentage = getLanguage(student_id)
            pt_percentage = 100 - eng_percentage
            if eng_percentage > pt_percentage:
                message = "You speak primarily in English! Keep it up, speaking in English is essential for your learning journey!"

            else:
                message = "You speak primarily in Portuguese. Try to incorporate more English into your conversations for better learning!"
            c.setFont("Helvetica", 12)
            y_position = 400
            lines = message.split(", ")
            for line in lines:
                c.drawString(rect_x + 10, y_position-60, line)
                y_position -= 20
            
            create_speedometer(percentage=eng_percentage)
            add_to_pdf(c, percentage=eng_percentage)
        
        if section == "How much are you speaking?":
            average_length = 23 #getPhraseLength(student_id)
            c.setFont("Helvetica", 12)
            message = f"This is your average phrase length: {average_length}"
            c.drawString(rect_x + 10, 200, message)
            if average_length < 30:
                advice = "You didn't speak much. Try to speak more next time!"
            elif average_length in range(31, 51):
                advice = "Good start. Stay strong and keep learning!"
            else:
                advice = "You spoke a lot this time!! Keep it up, long sentences will help you reach fluency faster."
            y_position = 200
            lines = advice.split("! ")
            for line in lines:
                c.drawString(rect_x + 10, y_position-20, line)
                y_position -= 20
            
    drawMyRuler(c)
    c.save()

if __name__ == "__main__":
    print("pdf created!")
    create_pdf("monthly_report.pdf", '1')