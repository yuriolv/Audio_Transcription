import os
import subprocess

# Base do caminho no AppData
user = os.getlogin()
base_path = os.path.join(os.environ["LOCALAPPDATA"],"Programs" ,"Ollama", "ollama app.exe")
print(user)

# Executa o Ollama
if os.path.exists(base_path):
    subprocess.run(["runas", f"/user:{user}", base_path])
else:
    print("O caminho do Ollama não foi encontrado.")
