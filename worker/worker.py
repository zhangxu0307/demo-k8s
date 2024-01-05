from flask import Flask
app = Flask(__name__)


@app.route('/local_time')
def get_local_time():
    import datetime
    return str(datetime.datetime.now())


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)