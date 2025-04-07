from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint."""
    return jsonify({"message": "pong"})

if __name__ == '__main__':
    # Run the app on port 8000 for local testing
    app.run(host='0.0.0.0', port=8000)
