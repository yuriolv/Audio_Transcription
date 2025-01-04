import tkinter as tk
""" from transcription import transcript
from errorDetection import errorDetection """

with open('phrases.txt', 'r') as f:
    summary = f.read()


def go_to_second_screen():
    #transcripted = transcript()
    #output = errorDetection(transcripted)
    output = [
        'Wrong (Verb Tense) - "I was went to the park yesterday with my friends."',
        'Wrong (Subject-verb agreement) - "We has a lot of fun, and we play soccer for hours."',
        'Wrong (Subject-verb agreement) - "We don\'t know why, but we was very tired after that."'
    ]

    # Limpa o frame2 para evitar duplicações
    for widget in frame2.winfo_children():
        widget.destroy()

    # Adiciona o título ao frame2
    title = tk.Label(frame2, text='Erros detectados', font=("Arial", 14))
    title.pack(pady=40)

    # Adiciona os Checkbuttons ao frame2
    variaveis.clear()  # Certifique-se de limpar a lista
    for item in output:
        var = tk.BooleanVar(value=False)
        chk = tk.Checkbutton(frame2, text=item, variable=var, anchor="center")
        chk.pack(fill="x", padx=20, pady=5, anchor="center")
        variaveis.append(var)

    button_frame = tk.Frame(frame2)
    button_frame.pack(pady=40)

    # Botão Voltar
    back_button = tk.Button(button_frame, text="Voltar", command=back_to_first_screen)
    back_button.pack(side="left", padx=5)

    # Botão Confirmar
    confirm_button = tk.Button(button_frame, text="Confirmar")
    confirm_button.pack(side="left", padx=5)

    # Alterna as telas
    frame1.pack_forget()
    frame2.pack(expand=True, anchor="center")


def back_to_first_screen():
    frame2.pack_forget()
    frame1.pack( expand=True)

def send_message():
    pass


# Configuração principal
root = tk.Tk()
root.title("Interface com Múltiplas Telas")
root.geometry("900x600")

# Frame 1 (primeira tela)
frame1 = tk.Frame(root)
frame1.pack(fill="both", expand=True, anchor="center")

# Botão para ir para a segunda tela
button = tk.Button(frame1, text="Ir para segunda tela", command=go_to_second_screen)
button.pack(expand=True)

# Frame 2 (segunda tela)
frame2 = tk.Frame(root)
variaveis = []  # Lista para armazenar as variáveis dos Checkbuttons

# Inicia o loop da interface
root.mainloop()
