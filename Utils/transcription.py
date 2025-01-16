#transcripted = transcript()
#output = errorDetection(transcripted)
#send_message(text, "69d2d1a285494d1ba7e76396fe451f25")
""" from transcription import transcript
from errorDetection import errorDetection """
from pathlib import Path

def get_Transcription():
  main_directory = Path("audios")


  subdirectories = [item for item in main_directory.iterdir() if item.is_dir()]
  if not subdirectories: return None

  subdirectory_path = subdirectories[-1]

  files = [file for file in subdirectory_path.iterdir() if file.is_file()]
  if not files: return None

  with open(files[0]) as f :
      text = f.read()

  messages = {}

  # Processando o texto
  lines = text.strip().split("\n\n")  # Dividindo por mensagens
  for i, line in enumerate(lines, start=1):
      parts = line.split("\n")  # Separando cabeçalho e mensagem
      header = parts[0]
      content = parts[1]
      
      # Extraindo dados do cabeçalho
      sender, time = header.strip("[]").rsplit("] ", 1)
      
      # Adicionando ao dicionário
      messages[f"message_{i}"] = {
          "sender": sender,
          "time": time,
          "content": content
      }

  # Exibindo o resultado
  return messages
