import speech_recognition as sr
import re
from tkinter import messagebox
from model import corrigir_texto

# Inicializa o recognizer
recognizer = sr.Recognizer()

# Usa o microfone como fonte de áudio
with sr.Microphone() as source:
    print("Ajustando o ruído ambiente...")
    recognizer.adjust_for_ambient_noise(source)
    print("Comece a falar...")

    while True:
        try:
            
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language="en")
            correction = corrigir_texto(text)

            if( re.sub(r'[.,]', '', text) == re.sub(r'[.,]', '', correction)):
                continue
            
            messagebox.showinfo("Erro", correction)
            print('\nincorrect sentence: ' + text)
            print('corrected sentence: ' + correction)

        except sr.UnknownValueError:
            print("Não entendi o que foi dito.")
        except sr.RequestError as e:
            print(f"Erro ao se comunicar com o serviço de reconhecimento: {e}")
        except KeyboardInterrupt:
            print("saindo...")
            break
        except Exception as e:
            print(e)
            break


""" "She go to the store yesterday."
Correção: "She went to the store yesterday."

"I has two dogs and one cat."
Correção: "I have two dogs and one cat."

"They was happy to see him."
Correção: "They were happy to see him."

"He don't like ice cream."
Correção: "He doesn't like ice cream."

"We is going to the party tonight."
Correção: "We are going to the party tonight."

"She no speak English very good."
Correção: "She doesn't speak English very well."

"Him and me went to the park."
Correção: "He and I went to the park."

"This book have too many pages."
Correção: "This book has too many pages."

"I'm going to meet with my friend tonight at 6 PM o'clock."
Correção: "I'm going to meet my friend tonight at 6 PM."

"There's five people in the room."
Correção: "There are five people in the room." """