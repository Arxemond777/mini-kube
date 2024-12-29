from flask import Flask, jsonify, request
import time
import os
import random
import logging
import json
import flask.cli
from prometheus_client import Counter, generate_latest, REGISTRY

flask.cli.show_server_banner = lambda *args: None
flask_log = logging.getLogger('werkzeug')
flask_log.setLevel(logging.CRITICAL)


# Prometheus Counter
#REQUEST_COUNTER = Counter('http_requests_total_pong_123', 'Total HTTP Requests_pong_124', ['method', 'endpoint'])
REQUEST_COUNTER = Counter(
    'http_requests_total_pong_123',
    'Total HTTP Requests pong_124',
    ['method', 'endpoint', 'pod_name']
)
# Get pod name from environment variable
POD_NAME = os.getenv("POD_NAME", "unknown_pod")

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

# Sample log
#logger.info("Ping service started")

app = Flask(__name__)

# Flag to indicate if the service should fail
should_fail = False

random_int = random.randint(1, 1000)

serivice_id = random.randint(1, 1000)

@app.route('/pong/<int:ping_id>', methods=['GET'])
def respond_pong(ping_id):
    # Check if the service is in fail mode
    if should_fail:
        return jsonify({"message": f'Service failure, service-name-pong-{serivice_id}'}), 500
    #print({"message": f"pong-{ping_id}, service-name-pong-{serivice_id}"})
    #REQUEST_COUNTER.labels(method='GET', endpoint='/pong/<ping_id>').inc()
    REQUEST_COUNTER.labels(method='GET', endpoint='/pong/<ping_id>', pod_name=POD_NAME).inc()
    logger.info(f"pong-{ping_id}, service-name-pong-{serivice_id}")
    return jsonify({"message": f"pong-{ping_id} from service-name-pong-{serivice_id}"})

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

@app.route('/health', methods=['GET'])
def health_check():
    # Health check to verify if the service is working
    if should_fail:
        return jsonify({"status": "fail", "message": "Service is in failure mode"}), 500
    return jsonify({"status": "healthy", "message": "Service is running normally"}), 200

@app.route('/fail', methods=['GET'])
def trigger_failure():
    global should_fail
    should_fail = True  # Set flag to start failing responses

    # Wait for a short delay to simulate service instability before shutdown
    time.sleep(5)
    #print(f'Shutting down service due to failure mode. service-name-pong-{serivice_id}')
    logger.info(f'Shutting down service due to failure mode. service-name-pong-{serivice_id}')

    # Access Flask's internal shutdown function
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if shutdown:
        shutdown()  # Trigger the shutdown if available
    else:
        #print("Shutdown function not available.")
        logger.info("Shutdown function not available.")
        # Forcefully exit the process if the shutdown function isn't available
        os._exit(1)  # Exit with a non-zero status to indicate failure

    return jsonify({"message": "Failure mode triggered. Service will exit shortly."})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False, use_reloader=False, use_debugger=False)  # Run pong on port 5001