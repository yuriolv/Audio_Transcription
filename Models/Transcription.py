from Models.User import User
from Models.Phrases import Phrases
from pathlib import Path
import nltk

class Transcription:
    def __init__(self, file):
        self.date = None
        self.file = file
        self.transcripted = None
        self.students = []

    def getTranscription(self):

        nltk.download('punkt_tab') 

        with open(self.file, encoding='utf-8') as f :
            text = f.read()

        messages = {}
        
        lines = text.strip().split("\n\n")  
        for i, line in enumerate(lines, start=1):
            parts = line.split("\n")  
            header = parts[0]
            content = nltk.sent_tokenize(parts[1])
            
            
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
            for i in message['content']:
                phrase = Phrases(i)
                messages.setdefault(message['sender'], []).extend([phrase])

        for key, value in messages.items():
            name = key
            phrases = value

            user = User(name, phrases)
            user.getEmail()
            self.students.append(user)