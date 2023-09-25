import json
from flask import Flask, render_template, request
from waitress import serve
from api.seek import SeekClient

app = Flask(__name__)
client = SeekClient()


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
    try: #loading the upload screen without errors
        if request.method == 'POST':
            file = request.files['jsonFile']
            y = json.load(file)
            print(y["createdBy"]["email"])
        return render_template('./upload.html', error=None)
    except  Exception as e: #catching the errors and logging them
        #printing the error for debugging purposes
        print(f"An error occurred: {e}")
        return render_template('./upload.html', error="There was an error uploading your file. Please try again.")


if __name__ == '__main__':
    print('Server running at http://localhost:8080')
    serve(app, host='0.0.0.0', port=8080)
