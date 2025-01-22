import requests, os
from dotenv import find_dotenv, set_key
from requests.auth import HTTPBasicAuth
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def refresh():
    
    ZOOM_CLIENT_ID = os.getenv('ZOOM_CLIENT_ID')
    ZOOM_CLIENT_SECRET = os.getenv('ZOOM_CLIENT_SECRET')
    REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')  

    
    token_url = "https://zoom.us/oauth/token"

   
    params = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    response = requests.post(token_url, data=params, auth=HTTPBasicAuth(ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET))

    if response.status_code == 200:
        # Extraindo o novo token da resposta
        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")
        
        print(access_token)
        set_key(find_dotenv(), 'ZOOM_TOKEN', access_token)
        set_key(find_dotenv(), 'REFRESH_TOKEN', refresh_token)
        print(os.environ.get('ZOOM_TOKEN'))
    else:
        print(f"Erro ao obter o novo token: {response.status_code} - {response.text}")
