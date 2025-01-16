import requests
from dotenv import set_key, find_dotenv
from requests.auth import HTTPBasicAuth
import os


ZOOM_CLIENT_ID = os.getenv('ZOOM_CLIENT_ID')
ZOOM_CLIENT_SECRET = os.getenv('ZOOM_CLIENT_SECRET')
AUTHORIZATION_CODE = os.getenv('AUTHORIZATION_CODE')  # O código que você obteve após o redirecionamento
REDIRECT_URI = os.getenv('REDIRECT_URI')  # A URI configurada no Zoom

token_url = "https://zoom.us/oauth/token"

params = {
    "grant_type": "authorization_code",
    "code": AUTHORIZATION_CODE,
    "redirect_uri": REDIRECT_URI
}

# Fazendo a solicitação para obter o token
response = requests.post(token_url, data=params, auth=HTTPBasicAuth(ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET))

if response.status_code == 200:
    # Extraindo o token da resposta
    token_data = response.json()
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    
    
    set_key(find_dotenv(), 'ZOOM_TOKEN', access_token)
    set_key(find_dotenv(), 'REFRESH_TOKEN', refresh_token)
else:
    print(f"Erro ao obter o token: {response.status_code} - {response.text}")
