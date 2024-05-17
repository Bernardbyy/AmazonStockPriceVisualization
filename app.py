import sys
from flask import Flask, render_template, jsonify
from pyspark.sql import SparkSession

app = Flask(__name__)

# Create a Spark session
spark = SparkSession.builder \
    .appName("Stock Data Visualization") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .enableHiveSupport() \
    .getOrCreate()

# Number of records to display, defaulting to 20 if not specified
num_records = int(sys.argv[1]) if len(sys.argv) > 1 else 20

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def get_data():
    amazonStock = spark.sql(f"SELECT timestamp, price, flag FROM stock.amazon_stock_minute ORDER BY timestamp DESC LIMIT {num_records}")
    amazonStock_df = amazonStock.toPandas()
    amazonStock_df.sort_values(by='timestamp', inplace=True)
    data = {
        'timestamp': amazonStock_df['timestamp'].tolist(),
        'price_data': amazonStock_df['price'].tolist(),
        'flags': amazonStock_df['flag'].tolist()
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)