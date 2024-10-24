from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Das ist ein neuer TEST'

if __name__ == '__main__':
    app.run(host='0.0.0.0')