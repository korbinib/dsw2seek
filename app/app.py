from flask import Flask, render_template
from waitress import serve

app = Flask(__name__)


@app.route("/")
def index():
    '''
    Home page.
    '''
    return render_template('./index.html')


if __name__ == '__main__':
    print('Server running at http://localhost:8080')
    serve(app, host='0.0.0.0', port=8080)
