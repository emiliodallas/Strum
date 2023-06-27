from confluent_kafka import Consumer, KafkaError
import telebot  
import json


bot = telebot.TeleBot(token='6032445966:AAGo-AkteKJIpeoNO1gtrGG4lusbppUUrNE')
chat_id = '1224465429'


# Configuration for Kafka consumer
kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "game-promotions"
kafka_topic_2 = "not-promotions"
kafka_group_id = "my-consumer-group"

# Create Kafka consumer
consumer = Consumer({
    "bootstrap.servers": kafka_bootstrap_servers,
    "group.id": kafka_group_id,
    "auto.offset.reset": "earliest"  # Start consuming from the beginning of the topic
})

# Subscribe to the Kafka topic
consumer.subscribe([kafka_topic,kafka_topic_2])

try:
    while True:
        msg = consumer.poll(1.0)  # Poll for new messages
        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error occurred: {msg.error().str()}")
                break

        # Process the received message
        
        event_data = msg.value().decode("utf-8")
        print("Received event data:", event_data)

        

        # Parse the JSON data
        data = json.loads(event_data)
        game_name = data["game_name"]
        price = data["price"]
        discount = data["discount"]

        if data['promotion']:
            message = f'The game {game_name} is costing {price} with {discount}% off!'
        else:
            message = f'The game {game_name} is not in promotion costing {price}.'
        bot.send_message(chat_id=chat_id, text=message)


        # Send notification to the user's smartphone using Telegram or another messaging service

except KeyboardInterrupt:
    pass

# Close the Kafka consumer
consumer.close()
