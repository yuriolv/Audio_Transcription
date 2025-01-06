import tkinter as tk
""" from transcription import transcript
from errorDetection import errorDetection """
from sendMessage import send_message

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

    # Frame para armazenar checkbuttons
    for widget in checkbutton_frame.winfo_children():
        widget.destroy()  # Limpa o frame antes de adicionar novos widgets

    # Cria uma lista local para armazenar os estados das checkboxes
    variaveis = []
    for item in output:
        var = tk.BooleanVar(value=False)
        chk = tk.Checkbutton(checkbutton_frame, text=item, variable=var, anchor="center")
        chk.pack(fill="x", padx=20, pady=5, anchor="center")
        variaveis.append((item, var))  # Salva o texto e a variável juntos

    # Atualiza o botão Confirmar para enviar os itens selecionados
    confirm_button.config(
        command=lambda: put_message([item for item, var in variaveis if var.get()])
    )

    # Alterna para a segunda tela
    frame1.pack_forget()
    frame2.pack(expand=True, anchor="center")


def back_to_first_screen():
    frame2.pack_forget()
    frame1.pack( expand=True)

def put_message(errors):
    text = 'Errors detected during the lesson:\n'
    for index, message in enumerate(errors):
        text += f'{index + 1}) {message}\n'
    send_message(text, "69d2d1a285494d1ba7e76396fe451f25")


# Configuração principal
root = tk.Tk()
root.title("Interface com Múltiplas Telas")
root.geometry("900x600")

# Frame 1 (primeira tela)
frame1 = tk.Frame(root)
frame1.pack(fill="both", expand=True, anchor="center")

# Botão para ir para a segunda tela
button = tk.Button(frame1, text="Start the correction", command=go_to_second_screen)
button.pack(expand=True)

# Frame 2 (segunda tela)
frame2 = tk.Frame(root)

title = tk.Label(frame2, text='Errors detected', font=("Arial", 14))
title.pack(pady=40)

# Frame para armazenar os checkbuttons
checkbutton_frame = tk.Frame(frame2)
checkbutton_frame.pack(expand=True)

# Frame para os botões
button_frame = tk.Frame(frame2)
button_frame.pack(pady=40)

# Botão Voltar
back_button = tk.Button(button_frame, text="Voltar", command=back_to_first_screen)
back_button.pack(side="left", padx=5)

# Botão Confirmar (configurado dinamicamente na segunda tela)
confirm_button = tk.Button(button_frame, text="Confirmar")
confirm_button.pack(side="left", padx=5)

# Inicia o loop da interface
root.mainloop()
