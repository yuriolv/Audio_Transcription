from collections import Counter
from Database import Corrections, Student, Transcription
import nltk
from textblob import TextBlob
from langdetect import detect_langs

def getParticipation(id_aluno):
        nltk.download('punkt_tab') 
        participations = []
        student = Student.get_id(id_aluno)
        texts = Transcription.get_by_id(id_aluno)
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
        print(f"Final participation percentages: {participations}")
        return participations

def getOcurrence(id_aluno):
    errors = []
    repeated = []

    corrections = Corrections.get_corrections(id_aluno) 
    
    if len(corrections) == 0:
        return

    for erro in corrections:
        if erro[1] not in errors:
            errors.append(erro)
        else:
            repeated.append(erro)
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
    student = Student.get_name(id_aluno)[0][0]
    texts = Transcription.get_by_id(id_aluno)
    mean = []

    if len(texts) == 0 or student == None:
        return

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
                result = getPercentage(phrase)
                mean.append(result['en'])
    return round((sum(mean)/len(mean)), 2)

def sentimentalScore(phrase):
    blob = TextBlob(phrase)
    sentiment_score = blob.sentiment.polarity 
    return sentiment_score


def getSentimental(id_aluno):
    student = Student.get_name(id_aluno)[0][0]
    texts = Transcription.get_by_id(id_aluno)
    mean = []

    if len(texts) == 0 or student == None:
        return

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
                result = sentimentalScore(phrase)
                mean.append(result)
    return round((sum(mean)/len(mean)), 2)

def getPhraseLength(id_aluno):
    student = Student.get_name(id_aluno)[0][0]
    texts = Transcription.get_by_id(id_aluno)

    phrase_length = []
    average_length = 0
    
    for text in texts:
        messages = {}
        new_text = text[0].replace('\r', '')
        lines = new_text.strip().split("\n\n")
        for line in lines:
            parts = line.split("\n")
            header = parts[0]
            content = parts[1]
            
            sender, _ = header.strip("[]").rsplit("] ", 1)

            messages.setdefault(sender, []).extend([content])
        
        for key, value in messages.items():
            if key == student:
                phrase = ' '.join(value)
                words = phrase.split()
                phrase_length.append(len(words))
                
    if phrase_length:
        average_length = round(sum(phrase_length) / len(phrase_length), 2)
    else:
        print("No phrases found for the student.")
        
    return average_length

def getName(id_aluno):
    student = Student.get_name(id_aluno)[0][0]
    return student