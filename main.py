import speech_recognition as sr
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
            # Escuta o áudio
            audio = recognizer.listen(source)
            
            #Faz a transcrição usando a API do Google
            text = recognizer.recognize_google(audio, language="en")
            
            correction = corrigir_texto(text)

            print('\nincorrect sentence: ' + text)
            print('corrected sentence: ' + correction)

        except sr.UnknownValueError:
            print("Não entendi o que foi dito.")
        except sr.RequestError as e:
            print(f"Erro ao se comunicar com o serviço de reconhecimento: {e}")
        except KeyboardInterrupt:
            print("saindo...")
            break
