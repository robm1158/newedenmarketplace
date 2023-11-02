from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo
import os
import sys
sys.path.append('/root/code/eve-aws')
from utils import mongodbData as mdb
from utils import utilities as utils
import pandas as pd
import json
from utils import ItemIdEnum as item
import numpy as np
from pathlib import Path

app = Flask(__name__)

# Use CORS with your app
# CORS(app, resources={r"/*": {"origins": ["https://elaborate-gnome-ee1359.netlify.app", "http://localhost:3000"]}})
CORS(app)

db = mdb.mongoData('eve-orders-the-forge')

dbh = mdb.mongoData('eve-historical-daily-the-forge')

BASE_DIR = Path(__file__).resolve().parent

@app.route('/')
def index():
    return jsonify(message="Hello from Flask!")

@app.route('/get_bubble_data', methods=['POST'])
def get_bubble_data():
    # Ensure type_id is defined; this can be passed as a parameter if needed
    data = request.json
    type_id = data.get('selectedValue')
    print(type_id)
    if not type_id:
        return jsonify({"error": "selectedValue not provided in the request."}), 400
    with open(BASE_DIR / "visualization" / "marketGroups.json", "r") as f:
        market_data = json.load(f)
    
    # Extract types for a specific market group id
    all_entries = utils.extract_types_for_market_group(market_data, type_id)
    # Fetch data for these types
    combined_df = pd.DataFrame()
    for entry in all_entries:
        temp_df = pd.DataFrame(dbh.syncPullAllCollectionDocuments(entry['item_name']))
        temp_df = temp_df.sort_values(by=['date'], ascending=False)
        top_row = temp_df.iloc[[0]] # Note: Using [[0]] will ensure we still get a DataFrame, not a Series
        top_row["percent_profit"] = (top_row['average'] - top_row['lowest']) / top_row['lowest'] * 100
        combined_df = pd.concat([combined_df, top_row], ignore_index=True) # Combine the dataframes
    combined_df['volume'] = combined_df['volume'].astype(float)
    combined_df['adjusted_volume'] = np.sqrt(combined_df['volume'])
    combined_df = combined_df.sort_values(by='percent_profit', ascending=False)
    
    # Convert DataFrame to JSON and return
    return combined_df.to_json(orient="records"), 200

@app.route('/get_item/<item_name>')
def get_item(item_name: str):
    
    df = db.syncPullLastDocument(item_name)
    df = df.sort_values(by=['issued'], ascending=False)

    if df is not None:
        return df.to_json(orient="records"), 200
    return jsonify({"error": "Data not found for the given ID"}), 404


@app.route('/get_graph_data', methods=['POST'])
async def get_graph_data():
    await db.checkConnection()
    # Extract selected value from request
    data = request.json
    selected_value = data.get('selectedValue')
    if not selected_value:
        return jsonify({"error": "selectedValue not provided in the request."}), 400

    # Process data based on selected value...
    df = dbh.syncPullAllCollectionDocuments(selected_value)
    if df is None:
        return jsonify({"error": "No data found for the selected value."}), 404

    df = df.sort_values(by=['date'], ascending=False)

    return df.to_json(orient="records"), 200



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
