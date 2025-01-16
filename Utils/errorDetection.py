from langchain_ollama import OllamaLLM


def errorDetection(users):
    

    prompt1 = """Im sending you one phrase, classify it with only one word, being the word one of the two options: Correct, Wrong(The Corresponding Grammatical or Syntatical Error Type). Here is the phrase: """

    model = OllamaLLM(model="llama3.2") #ollama run llama3.2-vision 11B

    for user in users:
        for i, phrase in enumerate(user.phrases):
            prompt2 = "Send me only the corrected sentence: " + phrase.content
            output = ''
            new_prompt = prompt1 + phrase.content

            if new_prompt.lower() == "exit":
                break
            
            for chunk in model.stream(new_prompt):
                if(chunk == 'Correct'):
                    user.phrases.pop(i)
                    break
                elif (chunk == 'Wrong'):
                    continue
                output += chunk
                

            if output != '':
                output += f' : "{phrase.content}" - {user.name}\n Correction: '

                for chunk in model.stream(prompt2):
                    output += chunk
                user.phrases[i].content = output
                
                
    return users

""" phrase = "I was went to the park yesterday with my friends. We has a lot of fun, and we play soccer for hours. The weather was very good, and the sun was shining bright. We don't know why, but we was very tired after that. I didn't eat much breakfast, so I was hungry during the game."
errorDetection(phrase) """

