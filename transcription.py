import speech_recognition as sr
import re
from tkinter import messagebox

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

            with open('phrases.txt', 'a') as arquivo:
                summary = arquivo.write(text)


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


"""I was went to the park yesterday with my friends. We has a lot of fun, and we play soccer for hours. 
The weather was very good, and the sun was shining bright. We don't know why, but we was very tired after that. I didn't eat much breakfast, so I was
hungry during the game. My friend Mark, he bring some snacks, but I forget to take water. We took many pictures because 
we wants to remember that day. At the end, we all sat down and talk about our plans for the next weekend. 
I hope we can do it again soon, maybe next Saturday. I didn't like that we left so early, but we had to go back home. 
I want go to the park more often, because it's fun and healthy."""