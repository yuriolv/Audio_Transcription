import os
from Utils.refreshToken import refresh
from dotenv import load_dotenv
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



def get_email(user_name):
    refresh()
    
    contacts = {}

    ZOOM_TOKEN = os.environ.get('ZOOM_TOKEN')
    END_CONTACTS = os.environ.get('END_CONTACTS')
    headers = {
    "Authorization": f"Bearer {ZOOM_TOKEN}",
    "Content-Type": "application/json"
    }
    
    response = requests.get(END_CONTACTS, headers=headers)
    
    if response.status_code == 200:
        json = response.json()
        for i in json['contacts']:
            name = f'{i["first_name"]} {i["last_name"]}'
            contacts[name] = i['email']
    else:
        raise Exception(response.text)
    
    for key, value in contacts.items():
        if user_name.lower() == key.lower():
            return value

if __name__ == "__main__":
    email = get_email('Erandi matos Magalhaes')
