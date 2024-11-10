from flask import Flask, jsonify, request
import requests
import threading
import time

app = Flask(__name__)

# Variable to keep track of the current ping-pong ID
ping_id = 1

def send_ping():
    global ping_id
    while True:
        try:
            # Send a GET request to the pong service with the current ping ID
            response = requests.get(f'http://localhost:5001/pong/{ping_id}')
            if response.status_code == 200:
                print(f'Sent ping-{ping_id}, received:', response.json().get("message"))
                ping_id += 1  # Increment the ID for the next ping
        except requests.RequestException as e:
            print("Failed to connect to pong service:", e)

        # Wait for 500 ms before sending the next ping
        time.sleep(0.5)

@app.route('/health', methods=['GET'])
def health_check():
    # Health check to verify if the service is working
    return jsonify({"status": "healthy", "message": "Service is running normally"}), 200

if __name__ == '__main__':
    # Start the ping-pong thread automatically
    threading.Thread(target=send_ping, daemon=True).start()
    app.run(port=5000)  # Run ping on port 5000