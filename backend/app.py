from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo
import sys
sys.path.append('/root/code/eve-aws')
from utils import mongodbData as mdb
import pandas as pd
from utils import ItemIdEnum as item

app = Flask(__name__)

# Use CORS with your app
CORS(app)

db = mdb.mongoData('eve-orders-the-forge')
dbh = mdb.mongoData('eve-historical-daily-the-forge')

@app.route('/')
def index():
    return jsonify(message="Hello from Flask!")

@app.route('/get_item/<item_name>')
def get_item(item_name: str):
    df = db.syncPullData(item_name)
    df = df.sort_values(by=['issued'], ascending=False)
    print(df)
    if df is not None:
        return df.to_json(orient="records"), 200
    return jsonify({"error": "Data not found for the given ID"}), 404


@app.route('/get_graph_data', methods=['POST'])
async def get_graph_data():
    
    # Extract selected value from request
    data = request.json
    selected_value = data.get('selectedValue')
    print(selected_value)
    if not selected_value:
        return jsonify({"error": "selectedValue not provided in the request."}), 400

    # Process data based on selected value...
    df = dbh.syncPullAllCollectionDocuments(selected_value)
    if df is None:
        return jsonify({"error": "No data found for the selected value."}), 404

    df = df.sort_values(by=['date'], ascending=False)

    return df.to_json(orient="records"), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)