from langchain_ollama import OllamaLLM


prompt = """Im sending you one phrase, classify it with only one word, being the word one of the two options: Correct, Wrong(The Corresponding Grammatical or Syntatical Error Type). Here is the phrase: """

caminho_arquivo = 'phrases.txt'

linhas = []

with open(caminho_arquivo, 'r') as arquivo:
    linhas = arquivo.readlines()

linhas = [linha.strip() for linha in linhas]


model = OllamaLLM(model="gemma2:27b") #ollama run llama3.2-vision 11B

i = 0
while linhas:
    phrase = prompt + linhas.pop(0)

    if phrase.lower() == "exit":
        break
    
    print(i, end=" - ", flush=True)
    i += 1
    for chunk in model.stream(phrase):
        print(chunk, end="", flush=True)
    print()