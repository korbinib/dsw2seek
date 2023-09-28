import requests
import os
import base64
from dotenv import load_dotenv


load_dotenv()
SEEK_USERNAME = os.environ.get("SEEK_USERNAME")
SEEK_PASSWORD = os.environ.get("SEEK_PASSWORD")


class SeekClient:
    def __init__(self):
        self.base_url = 'http://localhost:3000'
        auth = base64.b64encode(
            f"{SEEK_USERNAME}:{SEEK_PASSWORD}".encode()).decode()
        self.headers = {
            'Accept': 'application/vnd.api+json',
            'Accept-Charset': 'ISO-8859-1',
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/vnd.api+json'
        }

    def create_project(self, title, ids):
        '''
        Create a new project
        '''
        data = {
            "data": {
                "type": "projects",
                "attributes": {
                    "title": title,
                    "members": []
                }
            }
        }

        for id in ids: data['data']['attributes']['members'].append(id)

        return requests.post(f'{self.base_url}/projects', headers=self.headers, json=data)

    def get_people(self):
        '''
        Return all registered people in the SEEK system.
        '''
        return requests.get(f'{self.base_url}/people', headers=self.headers)

    def create_person(self, name, email):
        '''
        Create a new person in the SEEK system.
        '''
        data = {
            "data": {
                "type": "people",
                "attributes": {
                    "first_name": name,
                    "email": email
                }
            }
        }

        return requests.post(f'{self.base_url}/people', headers=self.headers, json=data)
