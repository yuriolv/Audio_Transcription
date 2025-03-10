import requests
from dotenv import load_dotenv, find_dotenv
import os
from Utils.refreshToken import refresh
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



def send_message(message, contact_id):
    refresh()

    ZOOM_TOKEN = os.environ.get('ZOOM_TOKEN')
    ZOOM_API_URL = os.environ.get('END_MESSAGES')
    
    headers = {
        "Authorization": f"Bearer {ZOOM_TOKEN}",
        "Content-Type": "application/json"
    }

    json = {
        "message": message,
        "to_contact": contact_id
    }

    response = requests.post(ZOOM_API_URL, json=json, headers=headers)

    if response.status_code == 201:
        print("Mensagem enviada com sucesso!")
        return True
    else:
        print(f"Erro ao enviar a mensagem: {response.status_code}")
        print(response.json())
        return False

if __name__ == "__main__":
    send_message("ol[a]", "yuri25olv@gmail.com")
