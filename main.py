import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
""" from transcription import transcript
from errorDetection import errorDetection """
from Utils.sendMessage import send_message


def go_to_second_screen():
    #transcripted = transcript()
    #output = errorDetection(transcripted)
    output = [
        'Wrong (Verb Tense) - "I was went to the park yesterday with my friends."',
        'Wrong (Subject-verb agreement) - "We has a lot of fun, and we play soccer for hours."',
        'Wrong (Subject-verb agreement) - "We don\'t know why, but we was very tired after that."'
    ]


    for widget in checkbutton_frame.winfo_children():
        widget.destroy()

    variaveis = []
    for item in output:
        var = tk.BooleanVar(value=False)
        chk = tk.Checkbutton(checkbutton_frame, text=item, variable=var, anchor="center", background="#56C0D1", selectcolor="#56C0D1", activebackground="#56C0D1")
        chk.pack(fill="x", padx=20, pady=5, anchor="center")
        variaveis.append((item, var)) 

    confirm_button.config(
        command=lambda: put_message([item for item, var in variaveis if var.get()])
    )

    show_frame(frame2)


def back_to_first_screen():
    show_frame(frame1)

def put_message(errors):
    text = 'Errors detected during the lesson:\n'
    for index, message in enumerate(errors):
        text += f'{index + 1}) {message}\n'
    print(text)
    #send_message(text, "69d2d1a285494d1ba7e76396fe451f25")

def show_frame(frame):

    for widget in root.winfo_children():
        widget.pack_forget()

    frame.pack(fill="both", expand=True)


root = tk.Tk()
root.title("Error Correction")
root.geometry("900x600")

# Frame 1 (primeira tela)
frame1 = tk.Frame(root, bg='#56C0D1')
frame1.pack(fill="both", expand=True, anchor="center")

image = Image.open("Assets/logo1.png")  
image = image.resize((140, 100), Image.Resampling.BOX) 
logo = ImageTk.PhotoImage(image)

logo_label = tk.Label(frame1, image=logo, background="#56C0D1")

logo_label.image = logo

logo_label.place(relx=0.5, rely=0.3, anchor="center")


button = tk.Button(frame1, text="Start the correction", command=go_to_second_screen)
button.pack(expand=True)



# Frame 2 (segunda tela)
frame2 = tk.Frame(root, bg='#56C0D1')

logo_label2 = tk.Label(frame2, image=logo, background="#56C0D1")
logo_label2.image = logo
logo_label2.place(relx=0.8, rely=0.8)

spacer = tk.Frame(frame2, height=160, bg="#56C0D1")  
spacer.pack()

title = tk.Label(frame2, text='Errors detected', font=("Arial", 16), background="#56C0D1")
title.pack(fill='both')


checkbutton_frame = tk.Frame(frame2, background="#56C0D1")
checkbutton_frame.pack(fill="both", pady=40)


button_frame = tk.Frame(frame2, background="#56C0D1")
button_frame.pack(anchor="center")


back_button = tk.Button(button_frame, text="Voltar", command=back_to_first_screen)
back_button.pack(side="left", padx=5)


confirm_button = tk.Button(button_frame, text="Confirmar")
confirm_button.pack(side='left', padx=5)

root.mainloop()
