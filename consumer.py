from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import sys

UPPER_LIMIT = float(sys.argv[1])
LOWER_LIMIT = float(sys.argv[2])

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Stock Data Processor with RDD") \
    .master("local[*]") \
    .enableHiveSupport() \
    .getOrCreate()

# Define the schema based on the incoming data
schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("symbol", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("currency", StringType(), True),
    StructField("previousClose", DoubleType(), True),
    StructField("volume", IntegerType(), True),
    StructField("high", DoubleType(), True),
    StructField("low", DoubleType(), True),
    StructField("open_price", DoubleType(), True),
    StructField("adj_close", DoubleType(), True)
])

# Subscribe to the Kafka topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "amzn-events") \
    .option("startingOffsets", "earliest") \
    .load()

# Select message value and convert to string
df = df.selectExpr("CAST(value AS STRING)")

# Parse JSON to DataFrame with specific schema
parsed_df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Define function to process each batch
def process_batch(df, epoch_id):
    # Create Hive table if it doesn't exist
    spark.sql("""
        CREATE TABLE IF NOT EXISTS stock.amazon_stock_minute (
            timestamp STRING, 
            symbol STRING, 
            price DOUBLE, 
            currency STRING, 
            previousClose DOUBLE, 
            volume INT, 
            high DOUBLE, 
            low DOUBLE, 
            open_price DOUBLE, 
            adj_close DOUBLE,
            flag INT
        )
    """)

    # Convert DataFrame to RDD
    rdd = df.rdd

    # Transform RDD: Convert data types, round, and add flag
    transformed_rdd = rdd.map(lambda row: (
        row.timestamp,
        row.symbol,
        round(row.price, 2),
        row.currency,
        round(row.previousClose, 2),
        int(row.volume),
        round(row.high, 2),
        round(row.low, 2),
        round(row.open_price, 2),
        round(row.adj_close, 2),
        1 if row.price > UPPER_LIMIT else (-1 if row.price < LOWER_LIMIT else 0)
    ))

    # Convert back to DataFrame
    new_df = transformed_rdd.toDF([
        "timestamp",
        "symbol",
        "price",
        "currency",
        "previousClose",
        "volume",
        "high",
        "low",
        "open_price",
        "adj_close",
        "flag"
    ])

    # Show or write DataFrame (for demonstration, we'll show it)
    new_df.show()

    # Store DataFrame into Hive table
    new_df.write.mode("append").insertInto("stock.amazon_stock_minute")

# Apply the RDD operations on each batch
query = parsed_df.writeStream \
    .outputMode("update") \
    .foreachBatch(process_batch) \
    .start()

query.awaitTermination()
