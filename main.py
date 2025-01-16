#transcripted = transcript()
#output = errorDetection(transcripted)
#send_message(text, "69d2d1a285494d1ba7e76396fe451f25")
import customtkinter as ctk
from PIL import Image, ImageTk

def go_to_second_screen():
    output = [
        'Wrong (Verb Tense) - "I was went to the park yesterday with my friends."',
        'Wrong (Subject-verb agreement) - "We has a lot of fun, and we play soccer for hours."',
        'Wrong (Subject-verb agreement) - "We don\'t know why, but we was very tired after that."'
    ]

    for widget in checkbutton_frame.winfo_children():
        widget.destroy()

    variaveis = {}
    for i in output.items():
        for error in i[1]:
            var = ctk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(
                checkbutton_frame, 
                text=error, 
                variable=var,
                text_color="white",
                fg_color="#1D4E89"
            )
            chk.pack(fill="x", padx=20, pady=5, anchor="center")
            variaveis.append(({i[0]: error}, var))
            #resolver como a lista será passada para a função put message 
        

    confirm_button.configure(
        command=lambda: put_message([item for item, var in variaveis if var.get()])
    )

    show_frame(frame2)

def back_to_first_screen():
    show_frame(frame1)

def put_message(senders, errors):
    #pegar id do sender
    text = 'Errors detected during the lesson:\n'
    for index, message in enumerate(errors):
        text += f'{index + 1}) {message}\n'
    print(text)

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
