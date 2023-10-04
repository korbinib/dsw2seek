import requests
import os
import base64
from dotenv import load_dotenv


load_dotenv()
SEEK_USERNAME = os.environ.get('SEEK_USERNAME')
SEEK_PASSWORD = os.environ.get('SEEK_PASSWORD')


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


    def create_project(self, project, contributors):
        '''
        Create a new project

        Parameters
        ----------
        project : dict describing the project drawn from a DMP file
            Metadata for the project
        contributors : array of dictionaries on the form {'person_id': '1', 'institution_id': '1', 'role':[ ] }
            The people connected to the project and their roles
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
                        'permissions':[]
                    }
                }
            }
        }

        #Adds permissions based on roles 

        #Permissions are in the form: 
        # {'person_id':'1', 
        # 'access': 'manage' }
        managers = ['data manager', 'data steward','project manager', 'project leader']

        for cont in contributors:
            is_manager = False

            for role in cont['role']:
                if role in managers:
                    is_manager = True
                    break
            
            if is_manager:
                data['data']['attributes']['default_policy']['permissions'].append({
                        'person_id': cont['person_id'],
                        'access': 'manage'
                    })
            else:
                data['data']['attributes']['default_policy']['permissions'].append({
                        'person_id': cont['person_id'],
                        'access': 'download'
                    })
            
        return requests.post(f'{self.base_url}/projects', headers=self.headers, json=data)


    def get_people(self):
        '''
        Return all registered people in the SEEK system.
        '''
        return requests.get(f'{self.base_url}/people', headers=self.headers)


    def create_person(self, id, name, email):
        '''
        Create a new person in the SEEK system.
        '''
        data = {
            'data': {
                'id':id,
                'type': 'people',
                'attributes': {
                    'first_name': name,
                    'email': email
                }
            }
        }

        return requests.post(f'{self.base_url}/people', headers=self.headers, json=data)
