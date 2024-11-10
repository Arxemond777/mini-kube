from flask import Flask, jsonify, request
import time
import os

app = Flask(__name__)

# Flag to indicate if the service should fail
should_fail = False

@app.route('/pong/<int:ping_id>', methods=['GET'])
def respond_pong(ping_id):
    # Check if the service is in fail mode
    if should_fail:
        return jsonify({"message": "Service failure"}), 500
    print({"message": f"pong-{ping_id}"})
    return jsonify({"message": f"pong-{ping_id}"})

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
    print("Shutting down service due to failure mode.")

    # Access Flask's internal shutdown function
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if shutdown:
        shutdown()  # Trigger the shutdown if available
    else:
        print("Shutdown function not available.")
        # Forcefully exit the process if the shutdown function isn't available
        os._exit(1)  # Exit with a non-zero status to indicate failure

    return jsonify({"message": "Failure mode triggered. Service will exit shortly."})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)  # Run pong on port 5001