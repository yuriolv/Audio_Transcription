from langchain_ollama import OllamaLLM


def errorDetection(users):
    

    prompt1 = """Im sending you one phrase, classify it with only one word, being the word one of the two options: Correct, Wrong(The Corresponding Grammatical or Syntatical Error Type). Here is the phrase: """

    model = OllamaLLM(model="llama3.2") #ollama run llama3.2-vision 11B

    for user in users:
        phrases = []
        for phrase in enumerate(user.phrases[:]):
            print(phrase.content)
            prompt2 = "Send me only the corrected sentence: " + phrase.content
            output = ''
            new_prompt = prompt1 + phrase.content

            if new_prompt.lower() == "exit":
                print(new_prompt)
                break
            
            for chunk in model.stream(new_prompt):
                if(chunk == 'Correct'):
                    user.phrases.pop(user.phrases.index(phrase))
                    break
                output += chunk
                
            if output != '':
                report = f'"{phrase.content}" {output.replace('Wrong', '')} - {user.name}\n Correction: '

                for chunk in model.stream(prompt2):
                    report += chunk
                phrase.content = report
                
                
    return users

""" phrase = "I was went to the park yesterday with my friends. We has a lot of fun, and we play soccer for hours. The weather was very good, and the sun was shining bright. We don't know why, but we was very tired after that. I didn't eat much breakfast, so I was hungry during the game."
errorDetection(phrase) """

