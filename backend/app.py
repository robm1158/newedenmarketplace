from flask import Flask, jsonify
# Import CORS
from flask_cors import CORS

app = Flask(__name__)

# Use CORS with your app
CORS(app)

@app.route('/')
def index():
    return jsonify(message="Hello from Flask!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)