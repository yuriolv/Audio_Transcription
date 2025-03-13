from langchain_ollama import OllamaLLM
from Database.Correção import create_correcao
from Database.Transcrição import get_transcricao
from Database.Aluno import get_student
import textwrap


def errorDetection(transcripted):
    

    prompt1 = """Im sending you one phrase, classify it with only one word, being the word one of the two options: Correct, Wrong(The Corresponding Grammatical or Syntatical Error Type). Here is the phrase: """

    model = OllamaLLM(model="llama3.2") #ollama run llama3.2-vision 11B

    for user in transcripted.students:
        for phrase in user.phrases[:]:
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
                report = f'"{phrase.content}" {output.replace("Wrong", "")}\nCorrection: '

                for chunk in model.stream(prompt2):
                    report += chunk
                wrapped_lines = [textwrap.fill(line, 80) for line in report.split('\n')]
                report = '\n'.join(wrapped_lines)
                
                phrase.content = report
                id_aluno = get_student(user.name)[0][0]
                id_transcricao = get_transcricao(transcripted.name)[0][0]
                create_correcao(report, id_aluno, id_transcricao)
                
                
    return transcripted.students

""" phrase = "I was went to the park yesterday with my friends. We has a lot of fun, and we play soccer for hours. The weather was very good, and the sun was shining bright. We don't know why, but we was very tired after that. I didn't eat much breakfast, so I was hungry during the game."
errorDetection(phrase) """

