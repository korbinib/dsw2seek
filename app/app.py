import json
from flask import Flask, render_template, request
from waitress import serve
from api.seek import SeekClient

app = Flask(__name__)
seek_client = SeekClient()


@app.route('/')
def index():
    '''
    Home page.
    '''
    return render_template('./index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    '''
    Upload page.
    '''
    if not request.method == 'POST':
        return render_template('./upload.html', error='Please upload a file.')

    dmp = load_file(request)

    if not check_format(dmp):
        return render_template('./upload.html', error='Incorrect file format.')
    else:
        dmp = dmp['dmp']

    # 1. Create users for all contributors
    people = dmp['contributor']
    for i, person in enumerate(people):
        res = seek_client.create_person(person['name'], person['mbox'])

        people[i]['response'] = {
            'status_code': res.status_code, 'json': res.json()}

    # 2. Create a new project
    project = dmp['project'][0]
    res = seek_client.create_project(
        project, [(1, 1)])

    project['response'] = {
        'status_code': res.status_code, 'json': res.json()}

    return render_template('./upload.html', people=people, project=project)

# load file function
def load_file(request):
    '''
    Load the JSON file from the request.
    '''
    file = request.files['jsonFile']
    return json.load(file)


def check_format(file):
    '''
    Check if the file is in the correct format.
    '''
    try:
        # Check if the 'dmp' field is present in the JSON data
        if 'dmp' in file:
            #JSON file is in the right format with the "dmp" field
            return True
        else:
            #'JSON file is missing the "dmp" field.'
            return False

    except json.JSONDecodeError:
        return False



if __name__ == '__main__':
    print('Server running at http://localhost:8080')
    serve(app, host='0.0.0.0', port=8080)
