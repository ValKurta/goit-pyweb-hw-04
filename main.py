from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO
import os
import json
from datetime import datetime
import socket
import threading

STORAGE_DIR = 'storage'
DATA_FILE = os.path.join(STORAGE_DIR, 'data.json')

app = Flask(__name__)
socketio = SocketIO(app)

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/message.html')
def message():
    return render_template('message.html')


@app.route('/style.css')
def style():
    return send_from_directory('static', 'style.css')


@app.route('/logo.png')
def logo():
    return send_from_directory('static', 'logo.png')


@app.route('/message', methods=['POST'])
def handle_message():
    username = request.form['username']
    message = request.form['message']
    data = json.dumps({'username': username, 'message': message})

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data.encode('utf-8'), ('localhost', 5000))

    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404


def socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 5000))

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode('utf-8')
        timestamp = datetime.now().isoformat()

        with open(DATA_FILE, 'r') as f:
            data = json.load(f)

        data[timestamp] = json.loads(message)

        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == '__main__':
    threading.Thread(target=socket_server).start()
    socketio.run(app, host='0.0.0.0', port=3000, allow_unsafe_werkzeug=True)
