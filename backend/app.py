from flask import Flask, jsonify
from flask_cors import CORS
import pymongo
import sys
print(sys.path)
sys.path.append('/root/code/utils')
print(sys.path)
from utils import mongodbData
# from utils import s3PullData
import pandas as pd

app = Flask(__name__)

# Use CORS with your app
CORS(app)

db = mongodbData('eve-market-order-history-the-forge')

@app.route('/')
def index():
    return jsonify(message="Hello from Flask!")

@app.route('/get_item/<item_name>')
def get_column(item_name: str):
    df = db.pullData(item_name)
    if df is not None:
        return df.to_json(orient="list"), 200
    return jsonify({"error": "Data not found for the given ID"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)