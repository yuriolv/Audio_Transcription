import customtkinter as ctk
from Utils.getTranscription import get_Transcription
from Utils.errorDetection import errorDetection
from Utils.sendMessage import send_message
from PIL import Image

def go_to_second_screen():
    transcripted = get_Transcription()
    students = errorDetection(transcripted)


    for widget in checkbutton_frame.winfo_children():
        widget.destroy()

    variaveis = {}
    for student in students:
        for phrase in student.phrases:
            var = ctk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(
                checkbutton_frame, 
                text=phrase.content, 
                variable=var,
                text_color="white",
                fg_color="#1D4E89",
                command=lambda p=phrase: checkbox_changed(p)
            )
            chk.pack(fill="x", padx=20, pady=5, anchor="center")
             
        

    confirm_button.configure(
        command=lambda: put_message(students)
    )

    show_frame(frame2)

def back_to_first_screen():
    show_frame(frame1)

def checkbox_changed(phrase):
    phrase.check = not phrase.check
        

def put_message(students):
    texts = []
    for student in students:
        text = 'Errors detected during the lesson:\n'
        for index, phrase in enumerate(student.phrases):
            if phrase.check == True:
                phrase.content = phrase.content.replace(student.name, '')
                phrase.content = phrase.content.replace(' - ', '')
                text += f'{index + 1}) {phrase.content}\n'
                texts.append(text)
                send_message(text, student.email) 



def show_frame(frame):
    for widget in root.winfo_children():
        widget.pack_forget()
    frame.pack(fill="both", expand=True)

# Configuração principal
ctk.set_appearance_mode("System")  # "System", "Light" ou "Dark"
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Error Correction")
root.geometry("900x600")

# Frame 1 (primeira tela)
frame1 = ctk.CTkFrame(root, corner_radius=0)
frame1.pack(fill="both", expand=True, anchor="center")

image = Image.open("Assets/logo1.png")  
logo = ctk.CTkImage(image, size=(140,100))

logo_label = ctk.CTkLabel(frame1, image=logo, text="")
logo_label.place(relx=0.5, rely=0.3, anchor="center")

button = ctk.CTkButton(frame1, text="Start the correction", command=go_to_second_screen)
button.pack(expand=True)

# Frame 2 (segunda tela)
frame2 = ctk.CTkFrame(root, corner_radius=0)

logo_label2 = ctk.CTkLabel(frame2, image=logo, text="")
logo_label2.place(relx=0.8, rely=0.8)


title = ctk.CTkLabel(frame2, text='Errors detected', font=ctk.CTkFont(size=16, weight="bold"))
title.pack(fill='both')

checkbutton_frame = ctk.CTkFrame(frame2)
checkbutton_frame.pack(fill="both", pady=40)

button_frame = ctk.CTkFrame(frame2)
button_frame.pack(anchor="center")

back_button = ctk.CTkButton(button_frame, text="Back", command=back_to_first_screen)
back_button.pack(side="left", padx=5)

confirm_button = ctk.CTkButton(button_frame, text="Confirm")
confirm_button.pack(side='left', padx=5)

root.mainloop()


""" Verificação de erros, frontend """