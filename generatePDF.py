import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from getAnalysis import getOcurrence, getParticipation, getLanguage, getPhraseLength, getName

# Criação do gráfico 
def create_speedometer(percentage, output_path = "Assets/Images/speedometer.png"):
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw={'projection': 'polar'})
    ax.set_aspect(1)
    
    colors = ['#55aaaa', '#40848c', '#23535a'] # Baixo, médio de alto (em relação ao uso do inglês)
    ranges = [33, 66, 100]
    
    fig.patch.set_facecolor('#e8e2ee')
    ax.set_facecolor('#e8e2ee')
    
    # Converte a porcentagem para radiano
    rad = np.deg2rad(180 * (percentage / 100))
    
    ax.set_theta_zero_location("W")  # Faz o velocímetro ficar na horizontal
    ax.set_theta_direction(-1)
    
    # Background
    start_angle = 0
    for i in range(len(ranges)):
        end_angle = np.deg2rad(180 * (ranges[i] / 100))
        ax.barh(y=1, width=end_angle - start_angle, left=start_angle, 
                color=colors[i], height=0.5, edgecolor='black')
        start_angle = end_angle  # Atualiza para a próxima seção
    
    # Agulha
    ax.plot([0, rad], [0, 1], color = 'black', linewidth=2, marker='o')
    
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['polar'].set_visible(False)
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

# Tabela de participação 
def draw_section(c, rect_x, rect_y, rect_width, rect_height, title):
    width, height = A4
    
    # Background
    c.setFillColor(colors.HexColor('#e8e2ee'))
    c.rect(rect_x, rect_y - rect_height, rect_width, rect_height, fill=True, stroke=True)
    
    # Título
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(rect_x + 10, rect_y - 15, title)

def table(c, rect_x, rect_y, student_participation, rect_width, rect_height):
    bar_width = 30
    bar_gap = 10
    max_height = 100
    table_width = len(student_participation) * (bar_width + bar_gap)

    table_x = rect_x + (rect_width - table_width) / 2
    table_y = rect_y + rect_height - 100

    # Barras de participação
    for i, participation in enumerate(student_participation):
        bar_height = max_height * (participation / 100)
        bar_x = table_x + (i * (bar_width + bar_gap))
        c.setFillColor(colors.HexColor('#40848c'))
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
    c.setFillColor(colors.HexColor('#e8e2ee'))
    c.rect(0, 0, width, height, fill=True)

    # Header
    header_height = 80
    c.setFillColor(colors.HexColor('#40848c'))
    c.rect(0, height - header_height, width, header_height, fill=True)
    logo_path = "Assets/Images/image5.png"
    logo_width = 100
    logo_height = 90
    c.drawImage(logo_path, 20, height - logo_height + 10, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')

    title = 'MONTHLY REPORT' 
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor('#fefefe'))
    title_width = c.stringWidth(title, "Helvetica-Bold", 24)
    c.drawString((width - title_width) / 2, height - header_height + 40, title)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor('#fefefe'))
    student_width = c.stringWidth(getName(student_id), "Helvetica-Bold", 14)
    c.drawString((width - student_width) / 2, height - header_height + 20, getName(student_id))

    # Seções
    sections = [("Repeated mistakes", getOcurrence(student_id)),
                ("Participation", getParticipation(student_id)),
                ("Your main language", getLanguage(student_id)),
                ("How much are you speaking?", getPhraseLength(student_id))
    ]

    rect_y = 700
    rect_height = (height - 250) / 4  
    rect_width = width - 100  

    for title, data in sections:
        draw_section(c, 50, rect_y, rect_width, rect_height, title)  
        rect_y -= rect_height  

        if title == "Repeated mistakes":
            errors = data
            y_offset = rect_y + rect_height - 40
            for phrase, error in errors:
                c.setFont("Helvetica", 12)
                c.drawString(60, y_offset, f"{phrase} → {error}")
                y_offset -= 20
            if len(errors) > 5:
                c.drawString(60, y_offset, "More errors in the full report.")
        
        elif title == "Participation":
            participation = data
            print(f"Participation data: {participation}")  
            if participation:
                print("Drawing table...")
                table(c, 50, rect_y, participation, rect_width, rect_height)
            else:
                print("No participation data available.")
        
        elif title == "Your main language":
            eng_percentage = data
            create_speedometer(percentage=eng_percentage)
            c.setFont("Helvetica", 12)
            c.drawImage("Assets/Images/speedometer.png", 200, rect_y - 40, width=170, height=130)
            if eng_percentage > 50:
                message = "You speak primarily in English! Keep it up!" 
            else:
                message = "You speak primarily in Portuguese. Try to incorporate more English!"
            c.drawString(60, rect_y + rect_height - 40, message)

        elif title == "How much are you speaking?":
            average_length = data
            c.setFont("Helvetica", 12)
            message = f"This is your average words per sentence: {average_length}"
            c.drawString(60, rect_y + rect_height - 40, message)
            if average_length < 30:
                advice = "You didn't speak much. Try to speak more next time!"
            elif average_length in range(31, 51):
                advice = "Good job. Stay strong and keep learning!"
            else:
                advice = "You spoke a lot this time!! Keep it up, long sentences will help you reach fluency faster."
            y_position = 200
            lines = advice.split("! ")
            for line in lines:
                c.drawString(60, y_position-20, line)
                y_position -= 20
            
    c.save()

if __name__ == "__main__":
    print("pdf created!")
    create_pdf("monthly_report.pdf", 1)