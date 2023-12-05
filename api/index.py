import json
import base64
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from waitress import serve

import sys
sys.path.append(".")
from seek.client import SeekClient

app = Flask(__name__)
cors = CORS(app, resources={r'\/(login|typeahead)': {'origins': '*'}})

# This will be set by the login endpoint below.
seek_client = None


@app.route('/login', methods=['POST'])
def __seek_login():
    '''
    Receive a username and password and use these to log into Seek.
    '''
    global seek_client
    data = request.json
    credentials = base64.b64encode(
        f'{data["username"]}:{data["password"]}'.encode()).decode()
    seek_client = SeekClient(credentials)
    return jsonify({'success': True})


@app.route('/typeahead')
def __institutions_typeahead():
    '''
    Endpoint for fetching institutions as the user types.
    '''
    query = request.args.get('query')
    res = seek_client.institutions_typeahead(query)
    return jsonify(res.json())


@app.route('/')
def index():
    '''
    Home page.
    '''
    return render_template('./index.html')


@app.route('/upload', methods=['POST'])
def upload():
    '''
    Upload page. Processes the uploaded DMP file and creates a new project and users in SEEK.
    '''
    dmp = load_file(request)
    institution = request.form.get('institutionId')
    members = []

    try:
        # 1. Create users for all contributors
        people = dmp['contributor']
        for i, person in enumerate(people):
            res = seek_client.create_person(person['name'], person['mbox'])
            data = res.json()
            
            if success(res):
                members.append(  # Appends all created users to the contributor dictionary in create_project
                    (data['data']['id'], institution, person['role']))
            
            people[i]['response'] = {
                'status_code': res.status_code, 'json': data}

        # 2. Create a new project
        project = dmp['project'][0]
        res = seek_client.create_project(project, members)

        project['response'] = {
            'status_code': res.status_code, 'json': res.json()}

        return render_template('./upload.html', people=people, project=project)
    except Exception as e:
        return render_template('./upload.html', error="An error accured. Check the file format.")

# load file function


def load_file(request):
    '''
    Account for different ways of sending the file.
    Requests from this website will put the file in request.files,
    but DSW will put it in request.form.
    '''
    try:
        if len(request.files) == 0:
            # This is a request from DSW. Create a Seek client with the given credentials.
            global seek_client
            seek_client = SeekClient(
                request.headers['Authorization'].split(' ')[1])
            file = request.form['jsonFile']
            return json.loads(file)['dmp']
        else:
            file = request.files['jsonFile']
            return json.load(file)['dmp']
    except Exception as e:
        print(e)
        return True

def success(res):
    '''
    Checks if response is valid.
    Responses with the code 200 will pass.
    '''
    return res.status_code % 100 == 2

if __name__ == '__main__':
    print('Server running at http://localhost:8080')
    serve(app, host='0.0.0.0', port=8080)