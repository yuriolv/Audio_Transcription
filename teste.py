from reportlab.pdfgen import canvas

def criar_pdf(nome_arquivo):
    c = canvas.Canvas(nome_arquivo)
    c.drawString(100, 750, "Erros recentes:")
    c.drawString(150, 850, "Olá, este é um exemplo!")
    c.drawString(100, 950, "Olá, este é um PDF gerado com Python!")
    c.save()

criar_pdf("meu_arquivo.pdf")
