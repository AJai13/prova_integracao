from flask import Flask, request, jsonify
import redis
import json
from threading import Thread
from rabbitmq_consumer import start_consumer
from redis_client import get_redis_connection

app = Flask(__name__)

r = get_redis_connection()

events = []

@app.route('/event', methods=['POST'])
def receive_event():
    data = request.json
    events.append(data)
    r.set('events', json.dumps(events), ex=60)
    return 'Evento recebido!'

@app.route('/events', methods=['GET'])
def get_events():
    cached = r.get('events')
    if cached:
        return jsonify(json.loads(cached))
    return jsonify(events)

if __name__ == '__main__':
    Thread(target=start_consumer, daemon=True).start()
    app.run(port=5000)
