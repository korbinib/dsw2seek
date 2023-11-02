import json
from flask import Flask, render_template, request, jsonify
from waitress import serve
from api.seek import SeekClient

app = Flask(__name__)

# This will be set by the login endpoint below.
seek_client = None


@app.route('/login', methods=['POST'])
def __seek_login():
    '''
    Receive a username and password and use these to log into Seek.
    '''
    global seek_client
    data = request.json
    seek_client = SeekClient(data['username'], data['password'])
    return jsonify({'success': True})


@app.route('/typeahead')
def __institutions_typeahead():
    '''
    Endpoint for fetching institutions as the user types.
    '''
    query = request.args.get('query')
    res = seek_client.institutions_typeahead(query)
    return res.json()


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

    # 1. Create users for all contributors
    people = dmp['contributor']
    for i, person in enumerate(people):
        res = seek_client.create_person(person['name'], person['mbox'])

        people[i]['response'] = {
            'status_code': res.status_code, 'json': res.json()}

    # 2. Create a new project
    project = dmp['project'][0]
    res = seek_client.create_project(
        project, [(1, institution)])

    project['response'] = {
        'status_code': res.status_code, 'json': res.json()}

    return render_template('./upload.html', people=people, project=project)


def load_file(request):
    file = request.files['jsonFile']
    return json.load(file)['dmp']


if __name__ == '__main__':
    print('Server running at http://localhost:8080')
    serve(app, host='0.0.0.0', port=8080)
