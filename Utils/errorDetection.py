from langchain_ollama import OllamaLLM
import nltk


def errorDetection(summary):
    errors = {}
    output = ''

    prompt = """Im sending you one phrase, classify it with only one word, being the word one of the two options: Correct, Wrong(The Corresponding Grammatical or Syntatical Error Type). Here is the phrase: """

    model = OllamaLLM(model="gemma2:27b") #ollama run llama3.2-vision 11B

    for message, sender in summary.values():
        phrase = message['content']
        new_prompt = prompt + phrase

        if new_prompt.lower() == "exit":
            break
        
        for chunk in model.stream(new_prompt):
            if(chunk == 'Correct'):
                break
            output += chunk
            if(chunk == '\n'):
                output += f' - {sender}: "{phrase}"'
                errors.setdefault(sender, []).append(f'{output.replace(' \n', '')}') 
                output = ''
    return errors

""" phrase = "I was went to the park yesterday with my friends. We has a lot of fun, and we play soccer for hours. The weather was very good, and the sun was shining bright. We don't know why, but we was very tired after that. I didn't eat much breakfast, so I was hungry during the game."
errorDetection(phrase) """