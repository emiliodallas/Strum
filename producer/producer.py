from kafka import KafkaProducer
import json
import telebot
from commTelegram import run_telegram_bot
import os

# Error Handling
def delivery_callback(err, msg):
    if err:
        print(f"Failed to deliver message: {err}")
    else:
        print(f"Message produced: {msg.topic()}[{msg.partition()}] @ offset {msg.offset()}")


# Telegram Parameters
token = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(token)

# Configuration for Kafka producer
kafka_topic = "game-promotions"
kafka_topic_2 = "not-promotions"
kafka_topic_wishlist = "wishlist"

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers="kafka:9092")

wishlist = {}

def process_wishlist_data():
    wishlist_data = json.dumps(wishlist)
    producer.produce(kafka_topic_wishlist, value=wishlist_data, callback=delivery_callback)
    producer.flush()

while True:
    try:
        run_telegram_bot(TK=token)
    except Exception as e:
        print(e)

    # Process the wishlist data after the bot stops
    process_wishlist_data()