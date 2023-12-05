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

    def create_project(self, project, members):
        '''
        Create a new project

        Parameters
        ----------
        project : dict describing the project drawn from a DMP file
            Metadata for the project
        members : array of tuples on the form ( 1, 1, ['data steward', 'supervisor'])
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
                    'description': project.get('description', None),
                    'start_date': project['start'],
                    'end_date': project['end'],
                    'members': {
                        'data': members
                    },
                    'default_policy': {
                        'access': 'no_access',
                        'permissions': []
                    }
                }
            }
        }

        # Adds permissions based on roles

        # Permissions are on the form:
        # {
        #   'resource': {
        #       'id': '1',
        #       'type': 'people'
        #       },
        #   'access': 'manage' }
        managers = ['data manager', 'data steward',
                    'project manager', 'project leader']

        for person in members:
            
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
                data['data']['attributes']['default_policy']['permissions'].append(
                    {
                    'resource' : {
                        'id': person['person_id'],
                        'type': 'people'
                        },
                    'access': 'manage'
                })
            else:
                data['data']['attributes']['default_policy']['permissions'].append(
                    {
                    'resource' : {
                        'id': person['person_id'],
                        'type': 'people'
                        },
                    'access': 'download'
                })
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
        Search for institutions in the Seek system.
        '''
        return requests.get(f'{self.base_url}/institutions/typeahead?query={query}', headers=self.headers)
