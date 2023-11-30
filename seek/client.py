import os
import requests
from dotenv import load_dotenv

load_dotenv()
SEEK_URL = os.environ.get('SEEK_URL')


class SeekClient:
    def __init__(self, credentials):
        '''
        Initialize a new Seek client with the given base-64 encoded credentials.
        '''
        self.base_url = SEEK_URL
        self.headers = {
            'Accept': 'application/vnd.api+json',
            'Accept-Charset': 'ISO-8859-1',
            'Authorization': f'Basic {credentials}',
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
                    'description': project.get('description', None),
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

    def institutions_typeahead(self, query):
        '''
        Return all registered institutions in the SEEK system.
        '''
        return requests.get(f'{self.base_url}/institutions/typeahead?query={query}', headers=self.headers)
