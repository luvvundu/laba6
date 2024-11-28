from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK', 'instance_id': os.environ.get('INSTANCE_ID')}), 200

@app.route('/process', methods=['GET'])
def process():
    return jsonify({'instance_id': os.environ.get('INSTANCE_ID')}), 200

if __name__ == '__main__':
    instance_id = os.getenv('INSTANCE_ID', '1')
    app.config['INSTANCE_ID'] = instance_id
    app.run(port=int(instance_id) + 5000)  # порты 5001, 5002, 5003
