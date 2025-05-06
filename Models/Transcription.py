from Models.User import User
from Database.Transcription import create_transcription
from Models.Phrases import Phrases
from pathlib import Path
import nltk
import re

class Transcription:
    def __init__(self, file, name):
        self.date = None
        self.name = name
        self.file = file
        self.transcripted = None
        self.participation = {}
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
        create_transcription(self.name, text)
        
    def getTranscriptionFromMeet(self):
        
        nltk.download('punkt_tab')
        
        with open(self.file, encoding='utf-8') as f :
            text = f.read()
            
        messages = {}
        current_time = None
        
        timestamp_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}$")
        speaker_pattern = re.compile(r"^(.+?):\s*(.+)")
        
        lines = text.strip().split("\n")
        
        i = 1
        for line in lines:
            if not line:
                continue # Pula linhas vazias 
            
            if timestamp_pattern.match(line):
                current_time = line.strip()
            
            elif speaker_pattern.match(line):
                speaker, message = speaker_pattern.match(line).groups()
                
                content = nltk.sent_tokenize(message)
                
                messages[f"messages{i}"] = {
                    "sender": speaker,
                    "time": current_time,
                    "content": content
                }
                
                i += 1
                    
        self.transcripted = messages
        create_transcription(self.name, text)


    def getVocab(self, text, user):
        stopwords = set(stopwords.words("english"))

        words = set(text.lower().split())
        meaningful_words = words - self.stopwords

        new_words = meaningful_words - user.vocab

        return [new_words]

    '''def getStudents(self):
        messages = {}
        
        for message in self.transcripted:
            speaker = message["speaker"]
            content = message = ["message"]
            phrase = Phrases(content)
            message.setdefault(speaker, []).append(phrase)
            
        for name, phrase in messages.items():
            user = User(name, phrase)
            user.getEmail()
            self.students.append(user)'''
    
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