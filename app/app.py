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


@app.route('/upload', methods=['POST'])
def upload():
    '''
    Upload page.
    '''
    if not request.method == 'POST':
        return render_template('./upload.html', error="Please upload a file.")

    file = request.files['jsonFile']
    dmp = json.load(file)['dmp']

    projectComplete = "Project creation failed."
    accountComplete = []

    # 1. Create a new project
    res = seek_client.create_project(dmp['title'])
    if res.status_code == 200:
        projectComplete = "Project created succesfully"
    print(res.status_code)

    # 2. Create users for all contributors
    for person in dmp['contributor']:
        name = person['name']
        email = person['mbox']
        res = seek_client.create_person(name, email)
        if res.status_code == 200: #correct went thru
            message = "User " + str(name) + " was succesfully created. " + str(email)
            accountComplete.append(message)
        elif res.status_code == 422: #Unprocessable Entity / duplicate
            message = "User " + str(name) + " has failed to be created. " + str(email)
            accountComplete.append(message) #this might be changed out with "status": "Account already exists"

        print(res.status_code)
        

    return render_template('./upload.html', projectStatus = projectComplete, accountStatus = accountComplete)


if __name__ == '__main__':
    print('Server running at http://localhost:8080')
    serve(app, host='0.0.0.0', port=8080)
