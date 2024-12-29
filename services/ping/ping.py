from flask import Flask, jsonify, request
import requests
import threading
import time
import random
import logging
import json
import flask.cli
from prometheus_client import Counter, generate_latest, REGISTRY

flask.cli.show_server_banner = lambda *args: None


flask_log = logging.getLogger('werkzeug')
flask_log.setLevel(logging.CRITICAL)

# Setup a custom JSON formatter
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "message": record.getMessage(),
            "levelname": record.levelname,
            "name": record.name,
            "timestamp": self.formatTime(record, self.datefmt),
        }
        return json.dumps(log)

logger = logging.getLogger("ping-service")  # For ping-service
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(JSONFormatter())
logger.addHandler(console_handler)
app = Flask(__name__)

# Variable to keep track of the current ping-pong ID
ping_id = 1

serivice_id = random.randint(1, 1000)

def send_ping():
    global ping_id
    while True:
        try:
            # Send a GET request to the pong service with the current ping ID
            response = requests.get(f'http://pong-service:5001/pong/{ping_id}')
            if response.status_code == 200:
                #print(f'Sent ping-{ping_id}, received:, service-name-ping-{serivice_id}', response.json().get("message"))
                #print(f'Sent ping-{ping_id}, received: {response.json().get("message")}, service-name-ping-{serivice_id}')
                logger.info(f'Sent ping-{ping_id}, received: {response.json().get("message")}, service-name-ping-{serivice_id}')
                ping_id += 1  # Increment the ID for the next ping
        except requests.RequestException as e:
            #print("Failed to connect to pong service:", e)
            logger.error("Failed to connect to pong service:", e)

        # Wait for 500 ms before sending the next ping
        time.sleep(0.5)

@app.route('/health', methods=['GET'])
def health_check():
    # Health check to verify if the service is working
    return jsonify({"status": "healthy", "message": "Service is running normally"}), 200

if __name__ == '__main__':
    # Start the ping-pong thread automatically
    threading.Thread(target=send_ping, daemon=True).start()

    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False, use_debugger=False)  # Run ping on port 5000