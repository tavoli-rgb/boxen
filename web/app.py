from flask import Flask
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    repo_url = os.getenv('REPO_URL')
    if repo_url:
        if not os.path.exists('.git'):
            subprocess.run(['git', 'clone', repo_url, '.'])
        else:
            subprocess.run(['git', 'pull', 'origin', 'main'])
    app.run(host='0.0.0.0')