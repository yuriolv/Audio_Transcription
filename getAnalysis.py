from collections import Counter
from Database import Aluno, Transcrição, Correção
import nltk

def getParticipation(student):
        nltk.download('punkt_tab') 
        participations = []
        texts = Transcrição.read_transcricoes()[-4:]
        for text in texts:
            messages = {}

            new_text = text[0].replace('\r', '')
            lines = new_text.strip().split("\n\n")

            for line in lines:
                parts = line.split("\n")

                header = parts[0]
                content = nltk.sent_tokenize(parts[1])
                
                sender, time = header.strip("[]").rsplit("] ", 1)

                messages.setdefault(sender, []).extend([content])
            
            for key, value in messages.items():
                if key == student:
                    participations.append(round(len(value)/len(lines)*100, 2))
        return participations

def getOcurrence(student):
    student_id = Aluno.get_student(student)[0][0]
    errors = []
    repeated = []

    corrections = Correção.get_correcoes(student_id)

    print(corrections)

    for erro in corrections:
        if erro[0] not in errors:
            errors.append(erro[0])
        else:
            repeated.append(erro[0])
    return repeated