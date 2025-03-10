import customtkinter as ctk
import textwrap
from Utils.getTranscription import get_Transcription
from pathlib import Path
from Utils.errorDetection import errorDetection
from Utils.sendMessage import send_message
from datetime import datetime
from tkinter import PhotoImage
import threading, time
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LauraFix")
        # Dimensões da janela
        window_width = 900
        window_height = 600

        #Calcula posição para centralizar
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_offset = int((screen_width - window_width) / 2)
        y_offset = int((screen_height - window_height) / 2)

        #Define a geometria centralizada
        self.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}") 
        ctk.set_appearance_mode('light')

        self.grid_rowconfigure(0, weight=1)  # Permitir que a linha 0 se expanda
        self.grid_columnconfigure(0, weight=1)

        self.iconbitmap("Assets/Images/image15.ico")

        self.frames = {}
        self.shared_data = None

        for F in (FirstScreen, SecondScreen, LoadingScreen, ReportScreen):
            frame = F(parent=self, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstScreen)

    def show_frame(self, tela):
        print(f"Switching to: {tela}")
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
        logo = ctk.CTkImage(image, size=(160,95))

        logo_label = ctk.CTkLabel(self, image=logo, text="", fg_color="#3C808C")
        logo_label.grid(column=0, row=0,rowspan=3,sticky='nsew')

        middle_frame = ctk.CTkFrame(self, fg_color='transparent')
        middle_frame.grid(column=1, row=1)

        middle_frame.grid_rowconfigure(0, weight=1)
        middle_frame.grid_columnconfigure(0, weight=1)
        middle_frame.grid_columnconfigure(1, weight=1)

        values = self.get_files()

        self.combobox = ctk.CTkComboBox(
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
        
        self.combobox.grid(column=0, row=0, padx=10)
        self.combobox.set('Lessons')

        start_button = ctk.CTkButton(
            middle_frame, text="Start the correction", 
            command=lambda: self.go_to_second_screen(), 
            fg_color="#3C808C", text_color='#FFFFFF', 
            hover_color="#4092a0", 
            font=ctk.CTkFont(family='Inter')
            )
            
        start_button.grid(column=1, row=0, padx=10)
        
        report_button = ctk.CTkButton(
            middle_frame, text="Go to report", 
            command=lambda: self.go_to_report_screen(), 
            fg_color="#3C808C", text_color='#FFFFFF', 
            hover_color="#4092a0", 
            font=ctk.CTkFont(family='Inter')
            )
        
        report_button.grid(column=2, row=0, padx=10)

        self.error_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="red")
        self.error_label.grid(column=1, row=2, sticky='n')

    def initialize(self):
        """Reinicializa os valores ao retornar para a tela inicial."""
        self.selected[0] = None
        self.combobox.set('Lessons')
        self.error_label.configure(text="")

    def select_option(self, option):
        self.error_label.configure(text="")  
        self.selected[0] = option   

    def go_to_report_screen(self):
        if self.selected[0] is not None:
            file_name = self.selected[0]
            self.controller.shared_data = file_name
            
            
            procces_thread = threading.Thread(target=self.load_report_screen)
            procces_thread.start()
            self.controller.show_frame(LoadingScreen)

        else:
            self.error_label.configure(text="No file selected! Please select one and try again.")
            return
        
    def load_report_screen(self):
        print("Loading report screen...")
        self.controller.show_frame(ReportScreen)

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

                date_str = f'{name[0]} {name[1]}'
                date_obj = datetime.strptime(date_str, f"%Y-%m-%d %H.%M.%S") 
                formated_date = date_obj.strftime(f'%d/%m/%y %H:%M')

                subdirectories.append(f'{name[2]} {name[3]} - {formated_date}')
        
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

        loading_label = ctk.CTkLabel(self, text='')

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

class ReportScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.active_button = None
        self.is_initialized = False
        self.configure(fg_color="#FFFFFF")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)

        # Sidebar for students
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#3C808C", corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky='nswe')
        self.sidebar_frame.grid_propagate(False)

        image = Image.open("Assets/Images/image5.png")  
        logo = ctk.CTkImage(image, size=(120, 70))
        logo_label = ctk.CTkLabel(self.sidebar_frame, text='', image=logo)
        logo_label.pack(anchor='center', pady=(50,0))

        self.students_frame = ctk.CTkFrame(self.sidebar_frame, fg_color='transparent')
        self.students_frame.pack(anchor='center', pady=50)

        self.student_buttons = []
        
        self.content_frame = ctk.CTkFrame(self,corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nswe")

        self.title_label = ctk.CTkLabel(self.content_frame, text='', font=ctk.CTkFont('Inter', 18, 'bold'))
        self.title_label.pack(anchor='center', pady=(50,0))

        button_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        button_frame.pack(anchor="center")
        
        back_button = ctk.CTkButton(button_frame, text="Back",fg_color='#3C808C', hover_color='#4092a0',command = lambda: self.go_to_first_screen())
        back_button.pack(side="left", padx=7)

        self.confirm_button = ctk.CTkButton(button_frame,fg_color='#3C808C',hover_color='#4092a0', text="Confirm")
        self.confirm_button.pack(side='left', padx=7)
    
    def initialize(self):
        try:

            transcripted = get_Transcription(self.controller.shared_data)
            self.students = errorDetection(transcripted)

            self.title_label.configure(text=self.controller.shared_data)

            image = Image.open("Assets/Images/profile.png")  
            logo = ctk.CTkImage(image, size=(20, 20))

            for student in self.students:
                button = ctk.CTkButton(
                    self.students_frame, 
                    font=ctk.CTkFont(family='Inter',size=12, weight='bold'),
                    width=40,
                    image=logo,
                    compound='left',
                    anchor='w',
                    text=student.name, 
                    fg_color="#1a5c68", 
                    height=20, 
                    hover_color='#4092a0',
                    corner_radius=10,
                    border_spacing=11
                )
                button.configure(
                    command=lambda s=student, b=button: self.select_student(s, b) 
                )

                button.pack(fill="x", padx=5, pady=4)
                self.student_buttons.append(button)

            if self.student_buttons:
                self.student_buttons[0].invoke()

            '''self.confirm_button.configure(
                command=lambda: 
            )'''

            self.is_initialized = True
        except Exception as e:
            print("Error initializing ReportScreen", e)
    
    def highlight_selected_button(self, selected_button):
        for button in self.student_buttons:
            button.configure(fg_color="#3C808C") 

        selected_button.configure(fg_color="#1a5c68")  
        self.active_button = selected_button
    
    def select_student(self, student, button):
        print(f"the student {student.name} was selected!!")
        self.highlight_selected_button(button)
    
    def clear_sidebar(self):
        for button in self.student_buttons:
            button.destroy()
        self.student_buttons = []
    
    def go_to_first_screen(self):
        print("Back button pressed!!")
        self.clear_sidebar()
        self.is_initialized = False
        self.controller.show_frame(FirstScreen)

class SecondScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.active_button = None
        self.is_initialized = False
        self.configure(fg_color="#FFFFFF")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)

        # Sidebar for students
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#3C808C", corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky='nswe')
        self.sidebar_frame.grid_propagate(False)

        image = Image.open("Assets/Images/image5.png")  
        logo = ctk.CTkImage(image, size=(120, 70))
        logo_label = ctk.CTkLabel(self.sidebar_frame, text='', image=logo)
        logo_label.pack(anchor='center', pady=(50,0))

        self.students_frame = ctk.CTkFrame(self.sidebar_frame, fg_color='transparent')
        self.students_frame.pack(anchor='center', pady=50)

        self.student_buttons = []

        self.content_frame = ctk.CTkFrame(self,corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nswe")

        self.title_label = ctk.CTkLabel(self.content_frame, text='', font=ctk.CTkFont('Inter', 18, 'bold'))
        self.title_label.pack(anchor='center', pady=(50,0))

        self.checkbutton_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color='transparent', height=340)
        self.checkbutton_frame.pack(fill="both", pady=(30,15))

        button_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        button_frame.pack(anchor="center")
        

        self.selected_phrase = None
        
        self.edit_button = ctk.CTkButton(button_frame, fg_color='#3C808C', hover_color='#4092a0', text="Edit", command=lambda:self.edit_phrase(self.selected_phrase))
        self.edit_button.pack(side="left", padx=7)
        
        back_button = ctk.CTkButton(button_frame, text="Back",fg_color='#3C808C', hover_color='#4092a0',command=self.back_to_first_screen)
        back_button.pack(side="left", padx=7)

        self.confirm_button = ctk.CTkButton(button_frame,fg_color='#3C808C',hover_color='#4092a0', text="Confirm")
        self.confirm_button.pack(side='left', padx=7)

    def initialize(self):
        try:

            transcripted = get_Transcription(self.controller.shared_data)
            self.students = errorDetection(transcripted)

            self.title_label.configure(text=self.controller.shared_data)

            image = Image.open("Assets/Images/profile.png")  
            logo = ctk.CTkImage(image, size=(20, 20))

            for student in self.students:
                if len(student.phrases) == 0: continue
                button = ctk.CTkButton(
                    self.students_frame, 
                    font=ctk.CTkFont(family='Inter',size=12, weight='bold'),
                    width=40,
                    image=logo,
                    compound='left',
                    anchor='w',
                    text=student.name, 
                    fg_color="#1a5c68", 
                    height=20, 
                    hover_color='#4092a0',
                    corner_radius=10,
                    border_spacing=11
                )
                button.configure(
                    command=lambda s=student, b=button: self.select_student(s, b) 
                )

                button.pack(fill="x", padx=5, pady=4)
                self.student_buttons.append(button)

            if self.student_buttons:
                self.student_buttons[0].invoke()

            self.confirm_button.configure(
                command=lambda: self.put_message(self.students)
            )

            self.is_initialized = True
        except Exception as e:
            print(e)
    
    def select_phrase(self, phrase):
        self.selected_phrase = phrase
    
    def edit_phrase(self, phrase):
        if phrase is None:
            print("Error: The phrase passed to edit_window is None.")  
            return
    
        self.edit_window = ctk.CTkToplevel(self)
        self.edit_window.iconbitmap("Assets/Images/image15.ico")
        self.edit_window.title("Edit Message")
        
        window_width = 500
        window_height = 250

        screen_width = self.edit_window.winfo_screenwidth()
        screen_height = self.edit_window.winfo_screenheight()
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        self.edit_window.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")
        
        self.edit_window.transient(self)
        self.edit_window.grab_set()
        self.edit_window.lift()
        self.edit_window.focus_force()
        
        # Display da frase para edição
        self.textbox = ctk.CTkTextbox(self.edit_window, width=400, height=150)  
        self.textbox.pack(side="top", padx=15, pady=10, expand=True)
        self.textbox.insert("0.0", phrase.content)
        self.edit_window.after(200, lambda: self.edit_window.update_idletasks())  
        
        self.save_button = ctk.CTkButton(self.edit_window, text="Save", fg_color="#3C808C", hover_color="#4092a0", 
                                        command=lambda: self.save_changes(phrase))
        self.save_button.pack(side="left", padx=15, pady=10, expand=True)

        self.cancel_button = ctk.CTkButton(self.edit_window, text="Cancel", fg_color="#808080", hover_color="#909090", 
                                        command=self.edit_window.destroy)
        self.cancel_button.pack(side="left", padx=15, pady=10, expand=True)
        
        self.edit_window.update()
        self.edit_window.after(201, lambda: self.edit_window.iconbitmap("Assets/Images/image15.ico"))
        
    def save_changes(self, phrase):
        new_text = self.textbox.get("1.0", "end-1c")  # Edita o texto
        print(f"Novo texto : {new_text}")
        if phrase:
            phrase.content = new_text  # Atualiza a frase
            print(f"Novo texto : {new_text}")
            self.show_student_phrases(self.current_student)  # Atualiza a tela com a frase editada
        self.edit_window.destroy()      
        

    def highlight_selected_button(self, selected_button):
        for button in self.student_buttons:
            button.configure(fg_color="#3C808C") 

        selected_button.configure(fg_color="#1a5c68")  
        self.active_button = selected_button


    def select_student(self, student, button):
        self.highlight_selected_button(button)
        self.show_student_phrases(student)

    def clear_sidebar(self):
        for button in self.student_buttons:
            button.destroy()
        self.student_buttons = []
    
    def clear_confirmation(self):
        self.confirmation_window.destroy()
        self.confirmation_window.update_idletasks()
        self.back_to_first_screen()

    def clear_checkbutton_frame(self):
        for widget in self.checkbutton_frame.winfo_children():
            widget.destroy()
        self.checkbutton_frame.update_idletasks()

    def show_student_phrases(self, student):
        self.clear_checkbutton_frame()
        self.current_student = student
        
        for phrase in student.phrases:
            var = ctk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(
                self.checkbutton_frame, 
                text=phrase.content, 
                font=ctk.CTkFont(family='Inter',size=14),
                checkmark_color='white',
                fg_color='#3C808C',
                hover_color="#3C808C",
                width=450,
                variable=var,
                text_color="black",
                
            )
            chk.configure(command=lambda p=phrase: self.checkbox_changed(p))

            chk.pack(anchor="w", padx=15, pady=7)

    def back_to_first_screen(self):
        self.clear_sidebar()
        self.clear_checkbutton_frame()
        self.is_initialized = False
        self.controller.show_frame(FirstScreen)
        self.select_phrase(None)

    def checkbox_changed(self, phrase):
        if hasattr(phrase, 'check'):
            phrase.check = not phrase.check
        if phrase.check:
            self.select_phrase(phrase)
        else:
            self.select_phrase(None)
        
    def show_confirmation(self, success):
        self.confirmation_window = ctk.CTkToplevel(self)
        self.confirmation_window.iconbitmap("Assets/Images/image15.ico")  # Definido logo após criar a janela
        self.confirmation_window.title("Message Status")

        window_width = 300
        window_height = 150

        screen_width = self.confirmation_window.winfo_screenwidth()
        screen_height = self.confirmation_window.winfo_screenheight()
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        self.confirmation_window.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

        # Configurações adicionais para exibir no topo
        self.confirmation_window.transient(self)
        self.confirmation_window.grab_set()
        self.confirmation_window.lift()
        self.confirmation_window.focus_force()

        # Mensagem de confirmação
        message = "Message sent successfully!" if success else "Failed to send the message!"
        label = ctk.CTkLabel(self.confirmation_window, text=message, font=ctk.CTkFont(family='Inter', size=14))
        label.pack(pady=20)
        ok_button = ctk.CTkButton(
            self.confirmation_window,
            text="OK",
            fg_color="#3C808C",
            text_color='#FFFFFF',
            hover_color="#4092a0",
            command=self.clear_confirmation
        )
        ok_button.pack()

        # Garante que o ícone é reconfigurado após qualquer sobrescrição
        self.confirmation_window.after(201, lambda: self.confirmation_window.iconbitmap("Assets/Images/image15.ico"))

    
    def put_message(self, students):
        for student in students:
            found = False
            text = 'Errors detected during the lesson:\n'
            for index, phrase in enumerate(student.phrases):
                if phrase.check:
                    found = True
                    phrase.content = phrase.content.replace(student.name, '')
                    phrase.content = phrase.content.replace(' - ', '')
                    text += f'{index + 1}) {phrase.content}\n'

            if found:
                try:
                    response = send_message(text, student.email)
                    self.show_confirmation(response)
                except Exception as e:
                    print(e)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
