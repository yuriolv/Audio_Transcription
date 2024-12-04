from langchain_ollama import OllamaLLM
import nltk

nltk.download('punkt') 

caminho_arquivo = 'phrases.txt'
with open(caminho_arquivo, 'r') as arquivo:
    summary = arquivo.read()

phrases = nltk.sent_tokenize(summary)


prompt = """Im sending you one phrase, classify it with only one word, being the word one of the two options: Correct, Wrong(The Corresponding Grammatical or Syntatical Error Type). Here is the phrase: """



model = OllamaLLM(model="gemma2:27b") #ollama run llama3.2-vision 11B

i = 0
while phrases:
    phrase = prompt + phrases.pop(0)

    if phrase.lower() == "exit":
        break
    
    print(i, end=" - ", flush=True)
    i += 1
    for chunk in model.stream(phrase):
        print(chunk, end="", flush=True)
    print()