import requests
from dotenv import load_dotenv, find_dotenv
import os
from refreshToken import refresh

ZOOM_TOKEN = os.environ.get('ZOOM_TOKEN')
ZOOM_API_URL = os.environ.get('END_MESSAGES')

load_dotenv(find_dotenv())

def send_message(message, channel_id):
    refresh()
    headers = {
        "Authorization": f"Bearer {ZOOM_TOKEN}",
        "Content-Type": "application/json"
    }

    json = {
        "message": message,
        "to_contact": channel_id
    }
    #"69d2d1a285494d1ba7e76396fe451f25"
    response = requests.post(ZOOM_API_URL, json=json, headers=headers)

    if response.status_code == 201:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar a mensagem: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    send_message("ol[a]", "yuri25olv@gmail.com")
