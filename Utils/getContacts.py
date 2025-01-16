import os
from refreshToken import refresh
import requests


def get_zoom_contacts():
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
            contacts[f'{i['first_name']} {i['last_name']}'] = i['email']
        return contacts
    else:
        raise Exception(response.text)
