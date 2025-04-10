import customtkinter as ctk
import re
import textwrap
from tkinter import ttk
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory
import textwrap
from Utils.getTranscription import get_Transcription
from pathlib import Path
from Database.Reports import ReportsCRUD
from Utils.errorDetection import errorDetection
from Utils.sendMessage import send_message
from datetime import datetime
from tkinter import PhotoImage
import threading, time
from PIL import Image, ImageTk
from generatePDF import create_pdf
import webbrowser

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

        for F in (LoginScreen, StudentHome, TeacherHome, ClassReport, LoadingScreen, ReportScreen):
            frame = F(parent=self, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginScreen)

    def show_frame(self, tela):
        frame = self.frames[tela]
        if hasattr(frame, "initialize"):
            if tela == ClassReport or not getattr(frame, "is_initialized", False):
                frame.initialize()
        frame.tkraise()

class LoginScreen(ctk.CTkFrame):
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

        title = ctk.CTkLabel(self, text_color='#000000', text='Welcome to LauraFix! Please login into your account.',font=ctk.CTkFont(family='Inter',size=18))
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

        teacher_button = ctk.CTkButton(
            middle_frame, text="Teacher", 
            command=lambda: self.go_to_teacher_screen(), 
            fg_color="#3C808C", text_color='#FFFFFF', 
            hover_color="#4092a0", 
            font=ctk.CTkFont(family='Inter')
            )

        teacher_button.grid(column=1, row=0, padx=10)

        student_button = ctk.CTkButton(
            middle_frame, text="Student", 
            command=lambda: self.go_to_student_screen(), 
            fg_color="#3C808C", text_color='#FFFFFF', 
            hover_color="#4092a0", 
            font=ctk.CTkFont(family='Inter')
            )

        student_button.grid(column=2, row=0, padx=10)

    def load_student_screen(self):
        self.controller.show_frame(StudentHome)
        student_frame = self.controller.frames[StudentHome]

        student_frame.show_chatbot()

    def load_teacher_screen(self):
        self.controller.show_frame(TeacherHome)

    def select_option(self, option):
        self.error_label.configure(text="")  
        self.selected[0] = option

    def go_to_teacher_screen(self):
        file_name = self.selected[0]
        self.controller.shared_data = file_name

        procces_thread = threading.Thread(target=self.load_teacher_screen)
        procces_thread.start()
        self.controller.show_frame(LoadingScreen)

    def go_to_student_screen(self):
        file_name = self.selected[0]
        self.controller.shared_data = file_name

        procces_thread = threading.Thread(target=self.load_student_screen)
        procces_thread.start()
        self.controller.show_frame(LoadingScreen)

class StudentHome(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#FFFFFF")

        self.llm = OllamaLLM(model="llama3.2")

        self.memory = ConversationBufferMemory()
        self.memory.chat_memory.add_user_message('')
        self.get_user_info()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#3C808C", corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky='nswe')
        self.sidebar_frame.configure(width=250)
        self.sidebar_frame.pack_propagate(False)
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.update_idletasks()

        image = Image.open("Assets/Images/image5.png")  
        logo = ctk.CTkImage(image, size=(120, 70))
        logo_label = ctk.CTkLabel(self.sidebar_frame, text='', image=logo)
        logo_label.pack(anchor='center', pady=(50,0))

        robot_image = Image.open("Assets/Images/robot.png")
        robot_logo = ctk.CTkImage(robot_image, size=(25, 25))
        self.chatbot_button = ctk.CTkButton(
            self.sidebar_frame, 
            font=ctk.CTkFont(family='Inter',size=12, weight='bold'),
            text="Chatbot", 
            command=self.show_chatbot, 
            fg_color="#1a5c68", 
            hover_color='#4092a0',
            image=robot_logo,
            width=40,
            compound='left',
            anchor='w',
            height=20,
            corner_radius=10,
            border_spacing=11
        )
        self.chatbot_button.pack(fill="x", padx=10, pady=(20, 5), expand=False)

        report_image = Image.open("Assets/Images/report.png")
        report_logo = ctk.CTkImage(report_image, size=(25, 25))

        self.report_button = ctk.CTkButton(
            self.sidebar_frame, 
            font=ctk.CTkFont(family='Inter',size=12, weight='bold'),
            text="Report", 
            command=self.show_report, 
            fg_color="#1a5c68", 
            hover_color='#4092a0',
            image=report_logo,
            width=40,
            compound='left',
            anchor='w',
            height=20,
            corner_radius=10,
            border_spacing=11
        )
        self.report_button.pack(fill="x", padx=10, pady=5, expand=False)

        self.tempBack_button = ctk.CTkButton (
            self.sidebar_frame,
            text="Temporary go back",
            command=self.go_to_login_screen,
            fg_color="#1a5c68", 
            hover_color='#4092a0',
            width=40,
            compound='left',
            anchor='w',
            height=20,
            corner_radius=10,
            border_spacing=11
        )
        self.tempBack_button.pack(fill="x", padx=10, pady=(10, 5), expand=False)

        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nswe")

        self.chatbot_page = self.create_chatbot_page()
        self.report_page = self.create_report_page()

        self.initial_message_shown = False
        

    def go_to_login_screen(self):
        self.pack_forget()
        self.controller.show_frame(LoginScreen)
    

    def show_initial_message(self):
        bot_label = ctk.CTkLabel(self.chat_frame, text="", 
                                font=ctk.CTkFont('Inter', 14),
                                fg_color="#f6f6f6", text_color="black",
                                corner_radius=10, padx=10, pady=5, justify='left', width=400)
        bot_label.pack(anchor="w", padx=10, pady=4) 
        first_message = 'Olá, em que posso ajudá-lo hoje? Avise-me se preferir continuar a nossa conversa em inglês.'
        self.display_text_slowly(bot_label, textwrap.fill(first_message, 60))
        self.memory.chat_memory.add_ai_message(first_message)

    def get_chatbot_response(self, message):
        self.memory.chat_memory.add_user_message(message)

        history = self.memory.load_memory_variables({})['history']

        response = self.llm.invoke(history + "\nUser: " + message + "\nAI:")

        self.memory.chat_memory.add_ai_message(response.strip())

        return response.strip()

    def get_user_info(self):
        reports = ReportsCRUD('language_school.db')
        response = reports.get_report(1)[0]

        prompt = f"""You are a personal assistant to students on an English course.  
                        Before we start, ask them what language they would like to communicate in (e.g. English, Spanish, Portuguese) 
                        Regardless of the choice, all examples will be provided in English.  

                        Based on the class data, here is your analysis of the student's last week:  
                            - Percentage of class participation: {float(response[1]) * 100:.0f}% 
                            - Percentage of English word usage: {float(response[4]) * 100:.0f}% 
                            - Behavioral status: {response[5]}  
                            - Repeated errors: {response[3]}  

                        I am the course administrator, and this information is being passed on to you as if you had observed it during the lessons!  He will talk to you soon.  

                        Use this information to provide constructive and direct feedback to help the student improve, only when they talk about it.    
                        Keep your answers clear, objective and short. Remember that all examples and questions will be given in English, even if the student prefers to continue the conversation in Portuguese."""

        self.memory.chat_memory.add_user_message(prompt)


    def send_message_on_enter(self, event=None):
        self.send_message()

    def send_message(self):
        message = self.chat_entry.get().strip()
        message = textwrap.fill(message, 60)

        if message:
            # Exibe a mensagem do usuário
            user_label = ctk.CTkLabel(self.chat_frame, text=message,
                                    font=ctk.CTkFont('Inter', 14),
                                    fg_color="#DCF8C6", text_color="black",
                                    corner_radius=10, padx=10, pady=5, justify='left')
            user_label.pack(anchor="e", padx=10, pady=4)

            self.chat_entry.delete(0, 'end')
            self.chat_frame.update_idletasks()
            self.chat_frame._parent_canvas.yview_moveto(1.0)

            # Label do bot com tamanho reduzido e animação de "Digitando..."
            bot_label = ctk.CTkLabel(self.chat_frame, text="Digitando", 
                                    font=ctk.CTkFont('Inter', 14),
                                    fg_color="#f6f6f6", text_color="black",
                                    corner_radius=10, padx=10, pady=5, justify='left', 
                                    width=200, wraplength=180)
            bot_label.pack(anchor="w", padx=10, pady=4)

            self.chat_frame.update_idletasks()
            self.chat_frame._parent_canvas.yview_moveto(1.0)

            # Inicia a animação
            self.typing_animation_running = True
            self.animate_typing(bot_label)

            # Roda a resposta do bot em background
            threading.Thread(target=self.handle_bot_response, args=(message, bot_label)).start()

    def animate_typing(self, label, count=0):
        if not hasattr(self, 'typing_animation_running') or not self.typing_animation_running:
            return

        dots = "." * (count % 4)
        label.configure(text="Digitando" + dots)
        self.after(500, self.animate_typing, label, count + 1)

    def handle_bot_response(self, message, bot_label):
        # Gera a resposta
        response = self.get_chatbot_response(message)
        formatted_response = self.format_response(response)

        # Para a animação
        self.typing_animation_running = False

        # Atualiza visualmente no thread principal
        self.after(0, lambda: self.show_final_response(bot_label, formatted_response))

    def show_final_response(self, label, text):
        label.configure(width=400, wraplength=390, text="")  
        self.display_text_slowly(label, text)


    
    def format_response(self, text):
        # Captura blocos com 2 a 3 frases seguidas
        sentence_pattern = r'([^.!?]*[.!?])'
        sentences = re.findall(sentence_pattern, text.strip())

        paragraphs = []
        buffer = ""

        for i, sentence in enumerate(sentences, 1):
            buffer += sentence.strip() + " "
            if i % 2 == 0:
                paragraphs.append(buffer.strip())
                buffer = ""

        if buffer:
            paragraphs.append(buffer.strip())

        formatted = []
        for paragraph in paragraphs:

            paragraph = re.sub(r'(\d+%+)', lambda m: m.group(1).upper(), paragraph)

            keywords = ["behavior", "mistake", "participation", "English", "improve",
                        'participação', 'comportamento', 'erros', 'Ingles', 'melhorar']
            for kw in keywords:
                paragraph = re.sub(fr'\b({kw})\b', lambda m: m.group(1).upper(), paragraph, flags=re.IGNORECASE)

            formatted.append(paragraph.strip())

        return '\n\n'.join(formatted)




    def display_text_slowly(self, label, text, index=0):
        if index < len(text):
            label.configure(text=text[:index + 1])
            self.after(30, self.display_text_slowly, label, text, index + 1)
            self.chat_frame._parent_canvas.yview_moveto(1.0)  

    def create_chatbot_page(self):
        frame = ctk.CTkFrame(self.content_frame, fg_color="white")

        title = ctk.CTkLabel(frame, text='Chat with AI', font=ctk.CTkFont('Inter', 18, 'bold'))
        title.pack(anchor='center', pady=(20,0))

        self.chat_frame = ctk.CTkScrollableFrame(frame, height=300, fg_color="grey90")
        self.chat_frame.pack(fill="both", pady=(10,5), padx=20)

        self.chat_history = ctk.CTkLabel(self.chat_frame, text='', font=ctk.CTkFont('Inter', 14), justify="left", wraplength=500)
        self.chat_history.pack(anchor="w", padx=10, pady=10)

        entry_frame = ctk.CTkFrame(frame, fg_color='transparent')
        entry_frame.pack(fill="x", padx=20, pady=(5,10))

        self.chat_entry = ctk.CTkEntry(entry_frame, placeholder_text="Type a message...", width=300)
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.chat_entry.bind("<Return>", self.send_message_on_enter)

        self.send_button = ctk.CTkButton(entry_frame, text="Send", command=self.send_message, fg_color='#3C808C', hover_color='#4092a0')
        self.send_button.pack(side="right")

        return frame

    def create_report_page(self):
        frame = ctk.CTkFrame(self.content_frame, fg_color="white")

        title = ctk.CTkLabel(frame, text='Your monthly report!', font=ctk.CTkFont('Inter', 18, 'bold'))
        title.pack(anchor='center', pady=(20,0))

        self.pdf_button = ctk.CTkButton(frame, text="Open PDF", command=lambda: (create_pdf("monthly_report.pdf", 1), webbrowser.open("monthly_report.pdf")), fg_color="#3C808C", hover_color="#4092a0")
        self.pdf_button.pack(pady=10)

        return frame

    def show_chatbot(self):
        self.report_page.pack_forget()
        self.chatbot_page.pack(fill="both", expand=True)
        self.sidebar_frame.update_idletasks()

        if not self.initial_message_shown:
            self.after(1000, self.show_initial_message)
            self.initial_message_shown = True

    def show_report(self):
        self.chatbot_page.pack_forget()
        self.report_page.pack(fill="both", expand=True)
        self.sidebar_frame.update_idletasks()

class TeacherHome(ctk.CTkFrame): 
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
            command=lambda: self.go_to_classReport(), 
            fg_color="#3C808C", text_color='#FFFFFF', 
            hover_color="#4092a0", 
            font=ctk.CTkFont(family='Inter')
            )

        start_button.grid(column=1, row=0, padx=10)

        """ report_button = ctk.CTkButton(
            middle_frame, text="Go to report", 
            command=lambda: (create_pdf("monthly_report.pdf", 1), webbrowser.open("monthly_report.pdf")), 
            fg_color="#3C808C", text_color='#FFFFFF', 
            hover_color="#4092a0", 
            font=ctk.CTkFont(family='Inter')
            ) """

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
        
        temp_back_button = ctk.CTkButton(
            middle_frame, text="Go back", 
            command=lambda: self.go_to_login_screen(), 
            fg_color="#3C808C", text_color='#FFFFFF', 
            hover_color="#4092a0", 
            font=ctk.CTkFont(family='Inter')
            )

        temp_back_button.grid(column=3, row=0, padx=10)

    def initialize(self):
        """Reinicializa os valores ao retornar para a tela inicial."""
        self.selected[0] = None
        self.combobox.set('Lessons')
        self.error_label.configure(text="")
        
    def go_to_login_screen(self):
        self.pack_forget()
        self.controller.show_frame(LoginScreen)

    def select_option(self, option):
        self.error_label.configure(text="")  
        self.selected[0] = option   

    def go_to_report_screen(self): 
        procces_thread = threading.Thread(target=self.load_report_screen)
        procces_thread.start()
        self.controller.show_frame(LoadingScreen)

    def load_report_screen(self):
        self.controller.show_frame(ReportScreen)

    def go_to_classReport(self):

        if self.selected[0] is not None:
            file_name = self.selected[0]
            self.controller.shared_data = file_name


            procces_thread = threading.Thread(target=self.load_classReport)
            procces_thread.start()
            self.controller.show_frame(LoadingScreen)

        else:
            self.error_label.configure(text="No file selected! Please select one and try again.")
            return

    def load_classReport(self):
        self.controller.show_frame(ClassReport)


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
            frame_idx = (frame_idx + 1) % len(frames) 
            self.controller.after(50, update, frame_idx)  

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
                    gif.seek(len(frames))
                    frame = gif.copy() 
                    frames.append(ctk.CTkImage(light_image=frame, size=(40, 40))) 
                except EOFError:
                    break  
            return frames

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class ReportScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.is_initialized = False
        self.configure(fg_color="#FFFFFF")
        db_path = 'language_school.db'
        reports = ReportsCRUD(db_path)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)

        self.title_label = ctk.CTkLabel(self, text='Weekly Reports', font=ctk.CTkFont('Inter', 18, 'bold'))
        self.title_label.pack(anchor='center', pady=(20, 0))

        table_frame = ctk.CTkFrame(self, fg_color="#FFFFFF")
        table_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_rowconfigure(1, weight=0)
        
        tree_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        tree_frame.grid(row=0, column=0, sticky='nsew')

        columns = ("Name", "Class participation", "Report date", "Repeated mistakes", "English percentage", "Behavioral state")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=30)
        style.configure("Treeview.Heading", background="#3C808C", foreground="white", font=("Arial", 13, "bold"), padding=(0,20))
        style.layout("Treeview.Heading",
             [('Treeheading.cell', {'sticky': 'nswe', 'border': 1}),
              ('Treeheading.padding', {'sticky': 'nswe'}),
              ('Treeheading.label', {'sticky': 'nswe'})])

        for col in columns:
            tree.heading(col, text=col)
            if col == 'Report date' or col == "Behavioral state":
                tree.column(col, width=80, stretch=True, anchor="center")
            else:
                tree.column(col, width=140, stretch=True, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.tooltip_repeated = {}
        self.tooltip_name = {}
        CHAR_LIMIT = 22
        
        button_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, pady=(10, 0))
        
        back_button = ctk.CTkButton(
            button_frame, text="Go back", 
            command=lambda: self.go_to_teacherHome(), 
            fg_color="#3C808C", text_color='#FFFFFF', 
            hover_color="#4092a0", 
            font=ctk.CTkFont(family='Inter'),
            width=150
            )

        back_button.pack()

        def carregar_dados():
            result = reports.read_reports()

            for row in result:
                if len(row[0]) > CHAR_LIMIT:
                    display_name = row[0][:CHAR_LIMIT] + ' ...'
                else:
                    display_name = row[0]

                if len(row[3]) > CHAR_LIMIT:
                    display_repeated = row[3][:CHAR_LIMIT] + ' ...'
                else:
                    display_repeated = row[3]

                item_id = tree.insert("", "end", values=(display_name, row[1], row[2], display_repeated, row[4], row[5]))

                self.tooltip_repeated[item_id] = row[3] 
                self.tooltip_name[item_id] = row[0] 

        carregar_dados()

        back_button = ctk.CTkButton(self, text="Back", fg_color='#3C808C', hover_color='#4092a0', command=lambda: self.go_to_teacherHome())
        back_button.pack(anchor='center', pady=15)

        tooltip_label = tk.Label(self, text="", background="white", foreground='black', relief="solid", borderwidth=1, wraplength=250)
        tooltip_label.place_forget()

        def show_tooltip(event):
            item_id = tree.identify_row(event.y)
            column_id = tree.identify_column(event.x)

            tooltip_label.place_forget()  

            if item_id:  
                if column_id == "#4":  
                    text = self.tooltip_repeated.get(item_id, "")
                elif column_id == "#1":
                    text = self.tooltip_name.get(item_id, "")
                else:
                    text = ""

                if text: 
                    tooltip_label.config(text=text)
                    tooltip_label.place(x=event.x_root - self.winfo_rootx() + 20, 
                                        y=event.y_root - self.winfo_rooty() + 20)

        tree.bind("<Motion>", show_tooltip)


    def initialize(self):
        try:
            self.is_initialized = True
        except Exception as e:
            print("Error initializing ReportScreen", e)

    def go_to_teacherHome(self):

        self.is_initialized = False
        self.controller.show_frame(TeacherHome)

class ClassReport(ctk.CTkFrame):
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
            # Limpa antes de carregar
            self.clear_sidebar()
            self.clear_checkbutton_frame()

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
            else:
                ctk.CTkLabel(self.content_frame, text="No students with detected phrases.", 
                            text_color="black", font=ctk.CTkFont("Inter", 14)).pack(pady=20)


            self.confirm_button.configure(
                command=lambda: self.put_message(self.students)
            )

            self.is_initialized = True
        except Exception as e:
            import traceback
            print("Erro ao inicializar ClassReport:", e)
            traceback.print_exc()


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
        new_text = self.textbox.get("1.0", "end-1c")  
        print(f"Novo texto : {new_text}")

        if phrase:
            original_text = phrase.content  # salva antes de mudar
            phrase.content = new_text       # modifica o conteúdo

            # Atualiza dinamicamente a checkbox correspondente
            for widget in self.checkbutton_frame.winfo_children():
                if isinstance(widget, ctk.CTkCheckBox) and widget.cget("text") == original_text:
                    widget.configure(text=new_text)
                    break

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
        print(f"student: {student}")

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
            print(f"phrase: {phrase}")

            chk.pack(anchor="w", padx=15, pady=7)

    def back_to_first_screen(self):
        self.clear_sidebar()
        self.clear_checkbutton_frame()
        self.is_initialized = False
        self.controller.show_frame(TeacherHome)
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
        self.confirmation_window.iconbitmap("Assets/Images/image15.ico")  
        self.confirmation_window.title("Message Status")

        window_width = 300
        window_height = 150

        screen_width = self.confirmation_window.winfo_screenwidth()
        screen_height = self.confirmation_window.winfo_screenheight()
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        self.confirmation_window.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

        self.confirmation_window.transient(self)
        self.confirmation_window.grab_set()
        self.confirmation_window.lift()
        self.confirmation_window.focus_force()

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
        print(f"show_confirmation ran")

        self.confirmation_window.after(201, lambda: self.confirmation_window.iconbitmap("Assets/Images/image15.ico"))


    def put_message(self, students):
        print("put_message began")
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
                    print("not found")
                    print(e)
        
        print("put_message ran")


if __name__ == "__main__":
    app = App()
    app.mainloop()