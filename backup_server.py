from os import mkdir
from os.path import *
import base64
from flask import Flask, abort, jsonify, request

DIR = './data/'

DIR = join(dirname(abspath(__file__)), DIR)
app = Flask(__name__)

@app.route('/get', methods=['GET'])
def get():
    key1 = request.args.get('key1', '')
    key2 = request.args.get('key2', '')
    if not key1 or not key2:
        abort(400)
    path = join(DIR, key1, key2)
    if not exists(path):
        abort(404)
    with open(path, 'r') as f:
        return f.read()

@app.route('/set', methods=['POST'])
def set():
    key1 = request.json.get('key1', '')
    key2 = request.json.get('key2', '')
    data = request.json.get('data', '')
    if not key1 or not key2:
        abort(400)
    dpath = join(DIR, key1)
    fpath = join(DIR, key1, key2)
    if not exists(dpath):
        mkdir(dpath)
    with open(fpath, 'w') as f:
        f.write(data)
    return jsonify(success=True)

if __name__ == '__main__':
    if not exists(DIR): mkdir(DIR)
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)
