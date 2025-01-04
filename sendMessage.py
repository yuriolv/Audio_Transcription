import requests
import os

ZOOM_TOKEN = os.environ.get('ZOOM_TOKEN')
ZOOM_API_URL = os.environ.get('ZOOM_API_URL')

mensagem = {
    "message": "Olá, Ana",
    "to_channel": "69d2d1a285494d1ba7e76396fe451f25"
}

def send_message():
    headers = {
        "Authorization": f"Bearer {ZOOM_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(ZOOM_API_URL, json=mensagem, headers=headers)

    if response.status_code == 201:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar a mensagem: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    send_message()
