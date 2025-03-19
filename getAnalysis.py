from collections import Counter
from Database import Aluno, Transcrição, Correção
import nltk
from langdetect import detect_langs

def getParticipation(id_aluno):
        nltk.download('punkt_tab') 
        participations = []
        student = Aluno.get_id(id_aluno)
        texts = Transcrição.getById(id_aluno)
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
    student_id = Aluno.get_id(student)[0][0]
    errors = []
    repeated = []

    corrections = Correção.get_correcoes(student_id) 
    
    print(corrections)

    for erro in corrections:
        print(f"Error type: {erro[1]}")
        if erro[1] not in errors:
            print(f"adding {erro} to errors")
            errors.append(erro)
        else:
            print(f"adding {erro} to repeated")
            repeated.append(erro)
    print(f"errors: {errors}")
    print(f"repeated errors: {repeated}")
    return repeated + errors

def getPercentage(phrase):
    detected = detect_langs(phrase)
    result = {}

    for lang in detected:
        if lang.lang == 'pt':
            result['pt'] = round(lang.prob * 100, 2)
        elif lang.lang == 'en':
            result['en'] = round(lang.prob * 100, 2)
        else:
            print('Text not identified')

    return result

def getLanguage(id_aluno):
    student = Aluno.get_name(id_aluno)[0][0]
    texts = Transcrição.getById(id_aluno)

    for text in texts:
        messages = {}

        new_text = text[0].replace('\r', '')
        lines = new_text.strip().split("\n\n")

        for line in lines:
            parts = line.split("\n")

            header = parts[0]
            content = parts[1]
            
            sender, time = header.strip("[]").rsplit("] ", 1)

            messages.setdefault(sender, []).extend([content])
            
        for key, value in messages.items():
            if key == student:
                phrase = ''.join(value)
                return getPercentage(phrase)
    

list = getLanguage(1)
print(list)