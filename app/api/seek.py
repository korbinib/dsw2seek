import requests
import json
import os
import base64
from dotenv import load_dotenv

load_dotenv()
SEEK_USERNAME = os.environ.get("SEEK_USERNAME")
SEEK_PASSWORD = os.environ.get("SEEK_PASSWORD")


class SeekClient:
    def __init__(self):
        self.base_url = 'http://localhost:3000'
        self.headers = {
            'Accept': 'application/vnd.api+json',
            'Accept-Charset': 'ISO-8859-1',
            'Authorization': f'Basic {base64.b64encode(bytes(f"{SEEK_USERNAME}:{SEEK_PASSWORD}", "utf-8"))}',
            'Content-Type': 'application/vnd.api+json'
        }

    def get_people(self):
        '''
        Return all registered people in the SEEK system.
        '''
        return requests.get(
            f'{self.base_url}/people', headers=self.headers)

    def create_person(self):
        '''
        Create a new person in the SEEK system.
        '''
        data = json.dumps({
            "data": {
                "type": "people",
                "attributes": {
                    "first_name": "Post",
                    "last_name": "Last",
                    "email": "maxPosttest264@test.com",
                    "description": "A person with all possible details",
                    "web_page": "http://www.website.com",
                    "orcid": "http://orcid.org/0000-0001-9842-9718",
                    "phone": "34-167-552266",
                    "skype_name": "postedSkype",
                    "expertise": [
                        "modeling",
                        "programming"
                    ],
                    "tools": [
                        "CeriusII",
                        "Gromacs",
                        "Python"
                    ]
                }
            }
        })

        return requests.post(
            f'{self.base_url}/people', headers=self.headers, data=data)
