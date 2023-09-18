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

    def create_project(self):
        '''
        Create a new project
        '''
        data = {
            "data": {
                "type": "projects",
                "attributes": {
                    "avatar": null,
                    "title": "Post Project Max",
                    "description": "A Taverna project",
                    "web_page": "http://www.taverna.org.uk",
                    "wiki_page": "http://www.mygrid.org.uk",
                    "default_license": "Other (Open)",
                    "default_policy": {
                        "access": "no_access",
                        "permissions": [
                            {
                                "resource": {
                                    "id": "1273",
                                    "type": "people"
                                },
                                "access": "manage"
                            },
                            {
                                "resource": {
                                    "id": "1924",
                                    "type": "projects"
                                },
                                "access": "download"
                            },
                            {
                                "resource": {
                                    "id": "1297",
                                    "type": "institutions"
                                },
                                "access": "view"
                            }
                        ]
                    }
                },
                "relationships": {
                    "programmes": {
                        "data": [
                            {
                                "id": "27",
                                "type": "programmes"
                            }
                        ]
                    },
                    "organisms": {
                        "data": [
                            {
                                "id": "5",
                                "type": "organisms"
                            }
                        ]
                    }
                }
            }
        }
        return requests.post(f'{self.base_url}/projects', headers=self.headers, json=data)


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
        data = {
            "data": {
                "type": "people",
                "attributes": {
                    "first_name": "Post",
                    "last_name": "Last",
                    "email": "maxPosttest1154@test.com"
                }
            }
        }

        return requests.post(f'{self.base_url}/people', headers=self.headers, json=data)


if __name__ == '__main__':
    client = SeekClient()
    # assert (client.get_people().status_code == 200)
    res = client.create_person()
    print(res.content)
    print(res.status_code)
    # assert (client.create_person().status_code == 201)
