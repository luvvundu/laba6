from flask import Flask, request, jsonify, render_template
import requests
import time
import threading

app = Flask(__name__)

instances = []
current_index = 0

def health_check():
    global instances
    while True:
        for instance in instances:
            try:
                response = requests.get(f"http://{instance['ip']}:{instance['port']}/health", timeout=2)
                if response.status_code != 200:
                    instance['available'] = False
            except requests.exceptions.RequestException:
                instance['available'] = False

        instances = [inst for inst in instances if inst['available']]
        time.sleep(5)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'instances': instances}), 200

@app.route('/process', methods=['GET'])
def process():
    global current_index

    if not instances:
        return jsonify({'error': 'No available instances'}), 503

    instance = instances[current_index]
    current_index = (current_index + 1) % len(instances)
    response = requests.get(f"http://{instance['ip']}:{instance['port']}/process")
    return jsonify(response.json()), response.status_code

@app.route('/')
def index():
    return render_template('index.html', instances=instances)

@app.route('/add_instance', methods=['POST'])
def add_instance():
    data = request.json
    instances.append({'ip': data['ip'], 'port': data['port'], 'available': True})
    return jsonify({'message': 'Instance added'}), 201

@app.route('/remove_instance', methods=['POST'])
def remove_instance():
    index = request.json['index']
    if 0 <= index < len(instances):
        instances.pop(index)
        return jsonify({'message': 'Instance removed'}), 200
    return jsonify({'error': 'Invalid index'}), 400

if __name__ == '__main__':
    thread = threading.Thread(target=health_check)
    thread.daemon = True
    thread.start()
    app.run(port=8080)  # запускаем балансировщик на порту 8080
