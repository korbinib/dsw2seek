import requests
import os
import base64
from dotenv import load_dotenv


load_dotenv()


class SeekClient:
    def __init__(self, username, passsword):
        self.base_url = 'http://localhost:3000'
        auth = base64.b64encode(
            f"{username}:{password}".encode()).decode()
        self.headers = {
            'Accept': 'application/vnd.api+json',
            'Accept-Charset': 'ISO-8859-1',
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/vnd.api+json'
        }

    def create_project(self, project, people):
        '''
        Create a new project

        Parameters
        ----------
        project : dict describing the project drawn from a DMP file
            Metadata for the project
        people : array of tuples on the form (person_id, institution_id)
            The people connected to the project
        '''
        data = {
            'data': {
                'type': 'projects',
                'attributes': {
                    'title': project['title'],
                    'description': project['description'],
                    'start_date': project['start'],
                    'end_date': project['end'],
                    'members': []
                }
            }
        }

        # TODO: This crashes when the project already exists
        # for person in people:
        #     data['data']['attributes']['members'].append(
        #         {'person_id': person[0], 'institution_id': person[1]}
        #     )

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
            'data': {
                'type': 'people',
                'attributes': {
                    'first_name': name,
                    'email': email
                }
            }
        }

        return requests.post(f'{self.base_url}/people', headers=self.headers, json=data)
