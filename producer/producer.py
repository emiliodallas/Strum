from confluent_kafka import Producer
import steam_data
import json
from psql.data import insert_client, add_game_to_wishlist

def delivery_callback(err, msg):
    if err:
        print(f"Failed to deliver message: {err}")
    else:
        print(f"Message produced: {msg.topic()}[{msg.partition()}] @ offset {msg.offset()}")

# Configuration for Kafka producer
kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "game-promotions"
kafka_topic_2 = "not-promotions"
kafka_topic_wishlist = "wishlist"

# Create Kafka producer
producer = Producer({"bootstrap.servers": kafka_bootstrap_servers})

wishlist = {}

while True:
    # Retrieve game information and check for promotions
    fi_name = input("Type first name: \n")
    la_name = input("Type last name: \n")
    id_telegram = input("Type telegram ID: \n")
    id_client = insert_client(first_name=fi_name, last_name=la_name, idtelegram=id_telegram)

    
    search = input("Search game: \n")
    f_name, f_price, f_discount = steam_data.price_discount(search)
    print(f"The game {f_name} is costing {f_price} with {f_discount}% discount.\n")
    wishlist_flag = input("Add to wishlist? (y/n)\n")
    
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

producer.close()
