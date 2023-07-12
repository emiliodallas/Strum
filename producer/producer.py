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
token = "6032445966:AAGo-AkteKJIpeoNO1gtrGG4lusbppUUrNE"
bot = telebot.TeleBot(token)

# Configuration for Kafka producer
kafka_topic = "game-promotions"
kafka_topic_2 = "not-promotions"
kafka_topic_wishlist = "wishlist"

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers="localhost:9094")

def process_wishlist_data(wishlist):
    for game_name, game_info in wishlist.items():
        if game_info["promotion"]:
            # Game is in promotion, produce a topic for it
            game_data = {
                "game_name": game_name,
                "price": game_info["price"],
                "discount": game_info["discount"]
            }
            game_data_json = json.dumps(game_data).encode("utf-8")
            producer.send(kafka_topic, value=game_data_json, key=game_name.encode("utf-8")).add_callback(delivery_callback)
            producer.flush()

    wishlist_data = json.dumps(wishlist).encode("utf-8")
    producer.send(kafka_topic_wishlist, value=wishlist_data).add_callback(delivery_callback)
    producer.flush()

while True:
    try:
        wishlist = run_telegram_bot(TK=token)
        
    except Exception as e:
        print(e)

    # Process the wishlist data after the bot stops
    process_wishlist_data(wishlist)