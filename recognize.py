import speech_recognition as sr

rec = sr.Recognizer()

try:
    with sr.Microphone() as mic: #captura o microfone padrão do sistema
        rec.adjust_for_ambient_noise(mic, duration=5) #calcula  o nível de ruído do amb.
        print("Estou na escuta!")
        while True:
            audio = rec.listen(mic, phrase_time_limit=1) #põe um listener no mic
            try:
                texto = rec.recognize_google(audio, language="pt-BR")
                print(f"Texto reconhecido: {texto}")
            except sr.UnknownValueError:  
                print("Não foi possível entender")
            except sr.RequestError:
                print("Erro de requisição")
except KeyboardInterrupt:
    print("Saindo...")