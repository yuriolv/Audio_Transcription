import customtkinter as ctk
from Utils.getTranscription import get_Transcription
from pathlib import Path
from Utils.errorDetection import errorDetection
from Utils.sendMessage import send_message
from tkinter import PhotoImage
import threading, time
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LauraFix")
        self.geometry("900x600")
        ctk.set_appearance_mode('light')

        self.grid_rowconfigure(0, weight=1)  # Permitir que a linha 0 se expanda
        self.grid_columnconfigure(0, weight=1)

        self.iconbitmap("Assets/Images/image15.ico")

        self.frames = {}
        self.shared_data = None

        for F in (FirstScreen, SecondScreen, LoadingScreen):
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
        self.configure(fg_color="#FFFFFF")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        title = ctk.CTkLabel(self, text_color='#000000', text='Welcome to LauraFix! Choose the lesson below',font=ctk.CTkFont(family='Inter',size=18))
        title.grid(column=1, row=0, sticky='s')

        image = Image.open("Assets/Images/image5.png")  
        logo = ctk.CTkImage(image, size=(140,100))

        logo_label = ctk.CTkLabel(self, image=logo, text="", fg_color="#3C808C")
        logo_label.grid(column=0, row=0,rowspan=3,sticky='nsew')

        middle_frame = ctk.CTkFrame(self, fg_color='transparent')
        middle_frame.grid(column=1, row=1)

        middle_frame.grid_rowconfigure(0, weight=1)
        middle_frame.grid_columnconfigure(0, weight=1)
        middle_frame.grid_columnconfigure(1, weight=1)

        values = self.get_files()

        combobox = ctk.CTkComboBox(
            middle_frame,
            values=values,
            state='readonly',  
            command=self.select_option, 
            button_color="#3C808C",
            dropdown_font=ctk.CTkFont(family='Inter'),
            font=ctk.CTkFont(family='Inter'),
            border_color="#3C808C",
            dropdown_fg_color="#FFFFFF",
            button_hover_color="#4092a0"
        )
        
        combobox.grid(column=0, row=0, padx=10)
        combobox.set('Lessons')

        start_button = ctk.CTkButton(
            middle_frame, text="Start the correction", 
            command=lambda: self.go_to_second_screen(), 
            fg_color="#3C808C", text_color='#FFFFFF', 
            hover_color="#4092a0", 
            font=ctk.CTkFont(family='Inter')
            )
            
        start_button.grid(column=1, row=0, padx=5)

        self.error_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="red")
        self.error_label.grid(column=1, row=2, sticky='n')

    def select_option(self, option):
        self.error_label.configure(text="")  
        self.selected[0] = option

    def go_to_second_screen(self):

        if self.selected[0] is not None:
            file_name = self.selected[0]
            self.controller.shared_data = file_name
            
            procces_thread = threading.Thread(target=self.load_second_screen)
            procces_thread.start()
            self.controller.show_frame(LoadingScreen)

        else:
            self.error_label.configure(text="No file selected! Please select one and try again.")
            return
        
    def load_second_screen(self):
        self.controller.show_frame(SecondScreen)
        
        
    def get_files(self):
        main_directory = Path("Assets/Transcriptions")
        subdirectories = []

        for item in main_directory.iterdir():
            if item.is_dir():
                name = item.name.split()
                subdirectories.append(f'{name[0]} {name[1]}')
        
        if not subdirectories: return None

        return subdirectories
    
class LoadingScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#FFFFFF")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        label_title = ctk.CTkLabel(
            self,
            text="Loading, please wait...",
            font=ctk.CTkFont(family='Inter', size=18),
            text_color='#000000'
        )
        label_title.grid(column=0, row=0, sticky='s', pady=10)

        loading_label = ctk.CTkLabel(self)

        loading_label.grid(column=0, row=1, sticky='n', pady=10)

        frames = self._get_frames('Assets/Images/loading.gif')
        self._play_gif(loading_label, frames)


    def _play_gif(self, label, frames):
        def update(frame_idx=0):
            frame = frames[frame_idx]
            label.configure(image=frame)
            frame_idx = (frame_idx + 1) % len(frames)  # Loop circular das frames
            self.controller.after(50, update, frame_idx)  # Atualiza a cada 100ms

        update()

    def _next_frame(self, frame, label):
        label.configure(
            image=frame
        )

    def _get_frames(self, img_path):
        with Image.open(img_path) as gif:
            frames = []
            while True:
                try:
                    gif.seek(len(frames))  # Vai para o próximo frame
                    frame = gif.copy()  # Faz uma cópia do frame atual como PIL.Image.Image
                    frames.append(ctk.CTkImage(light_image=frame, size=(40, 40)))  # Define o tamanho da imagem
                except EOFError:
                    break  # Sai do loop ao atingir o final do GIF
            return frames



class SecondScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.is_initialized = False

        image = Image.open("Assets/Images/image5.png")  
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
        if self.is_initialized:
            return

        self.clear_checkbutton_frame()

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

        self.is_initialized = True

    def clear_checkbutton_frame(self):
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