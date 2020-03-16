from os import mkdir
from os.path import *
import base64
from flask import Flask, abort, jsonify, request

DIR = '/var/opt/recovery-service/'

app = Flask(__name__)

@app.route('/backups/<key1>/<key2>', methods=['GET'])
def get(key1, key2):
    path = join(DIR, key1, key2)
    if not exists(path):
        abort(404)
    with open(path, 'r') as f:
        return f.read()

@app.route('/backups/<key1>/<key2>', methods=['PUT'])
def set(key1, key2):
    if request.json is None:
        abort(400)
    data = request.json.get('data', '')
    dpath = join(DIR, key1)
    fpath = join(DIR, key1, key2)
    if not exists(dpath):
        mkdir(dpath)
    if key1 == 'immutable' and exists(fpath):
        abort(403)
    with open(fpath, 'w') as f:
        f.write(data)
    return jsonify(success=True)

if __name__ == '__main__':
    DIR = './data/'
    DIR = join(dirname(abspath(__file__)), DIR)
    if not exists(DIR): mkdir(DIR)
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)

