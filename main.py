import customtkinter as ctk
from Utils.getTranscription import get_Transcription
from pathlib import Path
from Utils.errorDetection import errorDetection
from Utils.sendMessage import send_message
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Error Correction")
        self.geometry("900x600")

        self.grid_rowconfigure(0, weight=1)  # Permitir que a linha 0 se expanda
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.shared_data = None

        for F in (FirstScreen, SecondScreen):
            frame = F(parent=self, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstScreen)

    def show_frame(self, tela):
        frame = self.frames[tela]
        if hasattr(frame, "initialize"):
            frame.initialize()
        frame.tkraise()

class FirstScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected = [None]

        # Elementos da Tela Inicial
        image = Image.open("Assets/Images/logo1.png")  
        logo = ctk.CTkImage(image, size=(140,100))

        logo_label = ctk.CTkLabel(self, image=logo, text="")
        logo_label.place(relx=0.5, rely=0.1, anchor="center")

        values = self.get_files()

        combobox = ctk.CTkComboBox(
            self,
            values=values,  # Define as opções disponíveis
            command=self.select_option  # Chama a função quando uma opção é selecionada
        )
        combobox.pack(pady=100)
        combobox.set('Select the lesson')

        self.error_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="red")
        self.error_label.pack(pady=10)

        button = ctk.CTkButton(self, text="Start the correction", command=lambda: self.go_to_second_screen())
        button.pack()

    def select_option(self, option):
        self.error_label.configure(text="")  
        self.selected[0] = option

    def go_to_second_screen(self):

        if self.selected[0] != None:
            file_name = self.selected[0]
            self.controller.shared_data = file_name
            self.controller.show_frame(SecondScreen)
        else:
            self.error_label.configure(text="No file selected! Please select one and try again.")
            return
        
    def get_files(self):
        main_directory = Path("Assets/Transcriptions")
        subdirectories = []

        for item in main_directory.iterdir():
            if item.is_dir():
                name = item.name.split()
                subdirectories.append(f'{name[0]} {name[1]}')
        
        if not subdirectories: return None

        return subdirectories

        


class SecondScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        image = Image.open("Assets/Images/logo1.png")  
        logo = ctk.CTkImage(image, size=(140,100))

        logo_label2 = ctk.CTkLabel(self, image=logo, text="")
        logo_label2.place(relx=0.8, rely=0.8)


        title = ctk.CTkLabel(self, text='Errors detected', font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(fill='both')

        self.checkbutton_frame = ctk.CTkFrame(self)
        self.checkbutton_frame.pack(fill="both", pady=40)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(anchor="center")

        back_button = ctk.CTkButton(button_frame, text="Back", command=self.back_to_first_screen)
        back_button.pack(side="left", padx=5)

        self.confirm_button = ctk.CTkButton(button_frame, text="Confirm")
        self.confirm_button.pack(side='left', padx=5)


    def initialize(self):
        self.clear_checkbutton_frame()

        # Carregar transcrição e dados de erros
        transcripted = get_Transcription(self.controller.shared_data)
        students = errorDetection(transcripted)

        for student in students:
            for phrase in student.phrases:
                var = ctk.BooleanVar(value=False)
                chk = ctk.CTkCheckBox(
                    self.checkbutton_frame, 
                    text=phrase.content, 
                    variable=var,
                    text_color="white",
                    fg_color="#1D4E89",
                    command=lambda p=phrase: self.checkbox_changed(p)
                )
                chk.pack(fill="x", padx=20, pady=5, anchor="center")

        self.confirm_button.configure(
            command=lambda: self.put_message(students)
        )

    def clear_checkbutton_frame(self):
        """Remove widgets existentes no frame de checkboxes."""
        for widget in self.checkbutton_frame.winfo_children():
            widget.destroy()

    def back_to_first_screen(self):
        self.controller.show_frame(FirstScreen)

    def checkbox_changed(self, phrase):
        phrase.check = not phrase.check
        

    def put_message(self, students):
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


if __name__ == "__main__":
    app = App()
    app.mainloop()