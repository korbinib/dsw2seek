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

    def create_project(self, project, contributors):
        '''
        Create a new project

        Parameters
        ----------
        project : dict describing the project drawn from a DMP file
            Metadata for the project
        contributors : array of tuples on the form ( 1, 1, ['data steward', 'supervisor'])
            The people connected to the project and their roles. 
            - First index is the person_id.
            - Second index is the institution_id.
            - Third index is an array containing the roles of the person. 
        '''
        data = {
            'data': {
                'type': 'projects',
                'attributes': {
                    'title': project['title'],
                    'description': project['description'],
                    'start_date': project['start'],
                    'end_date': project['end'],
                    'contributors': contributors,
                    'default_policy': {
                        'permissions': []
                    }
                }
            }
        }

        # Adds permissions based on roles

        # Permissions are on the form:
        # {'person_id':'1',
        # 'access': 'manage' }
        managers = ['data manager', 'data steward',
                    'project manager', 'project leader']

        for person in contributors:
            # TODO: This crashes when the project already exists
            data['data']['attributes']['contributors'].append(
                {'person_id': person[0],
                 'institution_id': person[1]}
            )

            is_manager = False

            for role in person['role']:
                if role in managers:
                    is_manager = True
                    break

            if is_manager:
                data['data']['attributes']['default_policy']['permissions'].append({
                    'person_id': person['person_id'],
                    'access': 'manage'
                })
            else:
                data['data']['attributes']['default_policy']['permissions'].append({
                    'person_id': person['person_id'],
                    'access': 'download'
                })

        return requests.post(f'{self.base_url}/projects', headers=self.headers, json=data)

    def get_people(self):
        '''
        Return all registered people in the SEEK system.
        '''
        return requests.get(f'{self.base_url}/people', headers=self.headers)

    def get_person(self, id):
        '''
        Return the person registered in the SEEK system to tbe specific id.
        '''
        return requests.get(f'{self.base_url}/people/{id}', headers=self.headers)

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
        Search for institutions in the Seek system.
        '''
        return requests.get(f'{self.base_url}/institutions/typeahead?query={query}', headers=self.headers)
