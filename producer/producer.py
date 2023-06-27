from confluent_kafka import Producer
import producer
import steam_data

def delivery_callback(err, msg):
    if err:
        print(f"Failed to deliver message: {err}")
    else:
        print(f"Message produced: {msg.topic()}[{msg.partition()}] @ offset {msg.offset()}")

# Configuration for Kafka producer
kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "game-promotions"
kafka_topic_2 = "not-promotions"

# Create Kafka producer
producer = Producer({"bootstrap.servers": kafka_bootstrap_servers})

while True:
    # Retrieve game information and check for promotions
    name, price, discount = steam_data.price_discount(input("Game name:"))

    game_info = {
        "name": name,
        "price": price,
        "discount": discount
    }

    if game_info["discount"] > 0:
        promo_data = f"{{\"game_name\": \"{game_info['name']}\", \"promotion\": true, \"discount\": \"{game_info['discount']}\", \"price\": \"{game_info['price']}\"}}"
        producer.produce(kafka_topic, value=promo_data, callback=delivery_callback)
    elif game_info["discount"] == 0:
        nopromo_data = f"{{\"game_name\": \"{game_info['name']}\", \"promotion\": false, \"discount\": \"{game_info['discount']}\", \"price\": \"{game_info['price']}\"}}"
        producer.produce(kafka_topic_2, value=nopromo_data, callback=delivery_callback)
    # Flush the producer to ensure all messages are delivered
    producer.flush()

producer.close()
