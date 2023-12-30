from flask import Flask, request, jsonify
from werkzeug.serving import make_server
import os
import signal

app = Flask(__name__)


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def api_common(path):
    re_method = request.method
    if path == 'shutdown' and re_method == 'POST':
        os.kill(os.getpid(), signal.SIGINT)
        return 'Server shutting down...', 200
    print(request.url)
    print(request.data)
    return jsonify({'msg': 'success'}), 200


def server_run():
    server = make_server('127.0.0.1', 899, app)
    server.serve_forever()
