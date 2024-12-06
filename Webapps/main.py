from flask import Flask, render_template, request
import socket
import threading
import json
from datetime import datetime
from pathlib import Path


STORAGE_DIR = Path('./storage')
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
DATA_FILE = STORAGE_DIR / 'data.json'


if not DATA_FILE.exists():
    DATA_FILE.write_text('{}')

app = Flask(__name__, template_folder='front-end/templates', static_folder='front-end/static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/message', methods=['GET', 'POST'])
def message_handler():
    if request.method == 'POST':
        username = request.form.get('username')
        message_content = request.form.get('message')
        if username and message_content:
            send_to_socket_server({"username": username, "message": message_content})
            return render_template('message.html', success=True)
        return render_template('message.html', success=False)
    return render_template('message.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


def send_to_socket_server(data):
    app.logger.debug(f'Отправка данных на сокет-сервер: {data}')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(json.dumps(data).encode('utf-8'), ('127.0.0.1', 5000))


def socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind(('127.0.0.1', 5000))
        app.logger.debug('Сокет-сервер запущен и ожидает данные')
        while True:
            data, _ = server.recvfrom(4096)
            app.logger.debug(f'Получены данные от сокета: {data}')
            try:
                message = json.loads(data.decode('utf-8'))
                timestamp = datetime.now().isoformat()
                with DATA_FILE.open('r+') as file:
                    content = json.load(file)
                    content[timestamp] = message
                    file.seek(0)
                    json.dump(content, file, indent=2)
                app.logger.debug('Данные успешно записаны в data.json')
            except Exception as e:
                app.logger.error(f'Ошибка при записи данных: {e}')


if __name__ == '__main__':
    threading.Thread(target=socket_server, daemon=True).start()
    app.run(host='0.0.0.0', port=3000)




