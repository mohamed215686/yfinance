from confluent_kafka import Producer
import json
import uuid
import os
from dotenv import load_dotenv
from yfinance_api import test

def delivery_report(err, msg):
    if err:
        print(f"delivery failed : {err}")
    else:
        print(f"message delivered : {msg.value().decode('utf-8')}")

def main():
    load_dotenv()

    # confluent_kafka uses librdkafka (C-based), so you do NOT use Java JAAS strings
    producer_config = {
        'bootstrap.servers': os.getenv("BOOTSTRAP_SERVER"),
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': os.getenv("CONFLUENT_API_KEY"),
        'sasl.password': os.getenv("CONFLUENT_API_SECRET")
    } 

    producer = Producer(producer_config)
    topic_name = os.getenv("TOPIC_NAME")

    while True:
        try:
            # Call your external function
            test_data = test()

            # Renamed variable from 'test' to 'payload' to avoid shadowing the 'test()' function
            payload = {
                "id": uuid.uuid4().hex,
                "data": test_data
            }

            producer.produce(
                topic=topic_name, 
                value=json.dumps(payload).encode('utf-8'),
                callback=delivery_report
            )
            producer.flush()

        except Exception as e:
            print(f"Unexpected error in loop: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Producer manually stopped. Shutting down cleanly.")