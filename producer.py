from confluent_kafka import Producer
import yfinance as yf
import time
import requests
import json
from datetime import datetime

# Kafka producer configuration
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
}

conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'stock-price-producer'
}

# Create a Kafka producer instance
producer = Producer(conf)

# Kafka topic to send stock price data
topic = 'amzn-events'

# Ticker symbol of the stock (e.g., Apple Inc.)
ticker_symbol = 'AMZN'

# Function to fetch stock price and send to Kafka
def fetch_and_send_stock_price():
    while True:
        try:
            url = 'https://query2.finance.yahoo.com/v8/finance/chart/amzn'

            response = requests.get(url, headers=headers)
            data = json.loads(response.text)
            
            # Extract additional data points
            result = data["chart"]["result"][0]["meta"]
            price = result["regularMarketPrice"]
            symbol = result["symbol"]
            currency = result["currency"]
            previousClose = result["previousClose"]
            volume = result["regularMarketVolume"]
            high = result["regularMarketDayHigh"]
            low = result["regularMarketDayLow"]

            
            # Extract adjusted close price
            timestamps = data["chart"]["result"][0]["timestamp"]
            indicators = data["chart"]["result"][0]["indicators"]["quote"][0]
            adj_close_prices = indicators["close"]

            # Extract the list of open prices
            open_price = indicators["open"][0]
        
            # Get the most recent adjusted close price
            adj_close = adj_close_prices[-1] if adj_close_prices else None

            # Get the current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Combine data into a dictionary excluding recommendations and news
            combined_data = {
                "timestamp":timestamp,
                "symbol": symbol,
                "price": price,
                "currency": currency,
                "previousClose": previousClose,
                "volume": volume,
                "high": high,
                "low": low,
                "open_price": open_price,
                "adj_close": adj_close
            }

            # Produce the combined data to the Kafka topic
            producer.produce(topic, key=ticker_symbol, value=json.dumps(combined_data))

            producer.flush()


            # Print the message with timestamp
            print(f"{timestamp} - Sent {ticker_symbol} data to Kafka: {price,currency,previousClose,volume,high,low, open_price,adj_close}")

        except Exception as e:
            print(f"Error fetching/sending stock price: {e}")

        # Sleep for a specified interval (e.g., 5 seconds) before fetching the next price
        time.sleep(5)

# Start sending stock price data
fetch_and_send_stock_price()
