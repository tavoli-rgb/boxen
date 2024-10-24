from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    os.system('git pull origin main')
    app.run(host='0.0.0.0')