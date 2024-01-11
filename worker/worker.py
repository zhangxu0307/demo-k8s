from flask import Flask
app = Flask(__name__)


@app.route('/local_time')
def get_local_time():
    import datetime
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('/data/logs.txt', 'a') as f:
        f.write(current_time + '\n')
    return current_time


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)