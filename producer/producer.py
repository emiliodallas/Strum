from flask import Flask, request
from kafka import KafkaProducer
import steam_data
import json
import telebot
from psql.data import insert_client, add_game_to_wishlist
import commTelegram

app = Flask(__name__)

# Error Handling
def delivery_callback(err, msg):
    if err:
        print(f"Failed to deliver message: {err}")
    else:
        print(f"Message produced: {msg.topic()}[{msg.partition()}] @ offset {msg.offset()}")


# Telegram Parameters
token = "6032445966:AAGo-AkteKJIpeoNO1gtrGG4lusbppUUrNE"
bot = telebot.TeleBot(token)
client_id = '1224465429'

# Configuration for Kafka producer
kafka_topic = "game-promotions"
kafka_topic_2 = "not-promotions"
kafka_topic_wishlist = "wishlist"

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers = "kafka:9092")

wishlist = {}

while True:

    @app.route('/start', methods=["POST"])
    def handle_start():

        tele = commTelegram.Telegram(token=token, destinationID=client_id)

        tele.messageWR('Welcome! Type the game you want to search:')     
    
        # User types the game, automatically get user first and last names, game name and telegram_id
    
        fi_name , la_name, g_name, id_telegram = tele.messageRD_first()

        # Update table with client

        id_client = insert_client(first_name=fi_name, last_name=la_name, idtelegram=id_telegram)

        # Access Steam API

        f_name, f_price, f_discount = steam_data.price_discount(g_name)

        # Send the game info through Telegram

        gMessage = f"The game {f_name} is costing {f_price} with {f_discount}% discount.\n"
        tele.messageWR(gMessage)

        # Requests wishlist confirmation

        wishlistConfirm = "Add to wishlist? (y/n)\n"
        tele.messageWR(wishlistConfirm)

        # Receives if user wants to add to wishlist
        wishlist_flag = tele.wishlist_confirmation()
        
        if wishlist_flag == 'y' and f_discount == 0:
            wishlist[f_name] = {
                "price": f_price,
                "discount": f_discount,
                "promotion": False
            }
            add_game_to_wishlist(id_client, f_name, f_price, f_discount, False)

        elif wishlist_flag == 'y' and f_discount > 0:
            wishlist[f_name] = {
                "price": f_price,
                "discount": f_discount,
                "promotion": True
            }
            add_game_to_wishlist(id_client, f_name, f_price, f_discount, True)

        wishlist_data = json.dumps(wishlist)
        producer.produce(kafka_topic_wishlist, value=wishlist_data, callback=delivery_callback)
        producer.flush()

        return 'OK'
    
    if __name__ == '__main__':
        app.run()

    producer.close()
