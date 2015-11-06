import os
from flask import request, Flask, jsonify

app = Flask(__name__)

@app.route('/events', methods=['POST'])
def create_request():
    print(request.json)
    return jsonify({'result': True})

@app.route('/events', methods=['HEAD'])
def head():
    return jsonify({'result': True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

