from Model.User import User
from Model.Phrases import Phrases
from pathlib import Path

class Transcription:
    def __init__(self):
        self.date = None
        self.transcripted = None
        self.students = []

    def getTranscription(self):
        main_directory = Path("audios")
        subdirectories = []

        for item in main_directory.iterdir():
            if item.is_dir():
                subdirectories.append(item)
        
        if not subdirectories: return None

        subdirectory_path = subdirectories[-1]

        files = [file for file in subdirectory_path.iterdir() if file.is_file()]
        if not files: return None

        with open(files[0], encoding='utf-8') as f :
            text = f.read()

        messages = {}

        
        lines = text.strip().split("\n\n")  
        for i, line in enumerate(lines, start=1):
            parts = line.split("\n")  
            header = parts[0]
            content = parts[1]
            
            
            sender, time = header.strip("[]").rsplit("] ", 1)
            
            
            messages[f"message_{i}"] = {
                "sender": sender,
                "time": time,
                "content": content
            }

        self.transcripted = messages

    def getStudents(self):
        messages = {}
        for message in self.transcripted.values():
            phrase = Phrases(message['content'])
            messages.setdefault(message['sender'], []).append(phrase)

        for key, value in messages.items():
            name = key
            phrases = value

            user = User(name, phrases)
            user.getEmail()
            self.students.append(user)