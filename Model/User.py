from Utils.getContacts import get_email
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class User:
    def __init__(self, name, phrases):
        self.name = name
        self.phrases = phrases
        self.email = None

    def getEmail(self):
        self.email = get_email(self.name)
