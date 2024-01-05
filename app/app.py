from flask import Flask
import requests
app = Flask(__name__)


@app.route('/hello')
def hello():
    return "Hello, welcome to the K8s example!"


@app.route('/time')
def get_time():
    url = "http://127.0.0.1:5000/local_time"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)