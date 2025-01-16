from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Acessar as variáveis de ambiente
ZOOM_ACCOUNT_ID = os.getenv('ZOOM_ACCOUNT_ID')
ZOOM_CLIENT_ID = os.getenv('ZOOM_CLIENT_ID')
ZOOM_CLIENT_SECRET = os.getenv('ZOOM_CLIENT_SECRET')
ASSEMBLYAI_API_KEY = os.environ.update({'ASSEMBLYAI_API_KEY': 'abc'})
ZOOM_TOKEN = os.getenv('ZOOM_TOKEN')
END_MESSAGES = os.getenv('END_MESSAGES')
END_CONTACTS = os.getenv('END_CONTACTS')

# Verificar se as variáveis estão sendo carregadas corretamente
print("ZOOM_ACCOUNT_ID:", ZOOM_ACCOUNT_ID)
print("ZOOM_CLIENT_ID:", ZOOM_CLIENT_ID)
print("ZOOM_CLIENT_SECRET:", ZOOM_CLIENT_SECRET)
print("ASSEMBLYAI_API_KEY:", ASSEMBLYAI_API_KEY)
print("ZOOM_TOKEN:", ZOOM_TOKEN)
print("END_MESSAGES:", END_MESSAGES)
print("END_CONTACTS:", END_CONTACTS)
