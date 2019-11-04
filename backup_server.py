from os import mkdir
from os.path import exists, join
import base64
from flask import Flask, abort, jsonify, request

DIR = './data/'
safe = lambda s: base64.urlsafe_b64encode(s.encode('utf-8')).decode('utf-8')
app = Flask(__name__)

@app.route('/get', methods=['GET'])
def get():
    publicKey = request.args.get('publicKey', '')
    key = request.args.get('key', '')
    if not publicKey or not key:
        abort(400)
    path = join(DIR, safe(publicKey), safe(key))
    if not exists(path):
        abort(404)
    with open(path, 'r') as f:
        return f.read()

@app.route('/set', methods=['POST'])
def set():
    publicKey = request.form.get('publicKey', '')
    key = request.form.get('key', '')
    data = request.form.get('data', '')
    if not publicKey or not key:
        abort(400)
    dpath = join(DIR, safe(publicKey))
    fpath = join(DIR, safe(publicKey), safe(key))
    if not exists(dpath):
        mkdir(dpath)
    with open(fpath, 'w') as f:
        f.write(data)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=False)
