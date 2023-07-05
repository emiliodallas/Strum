from kafka import KafkaConsumer
from kafka.errors import KafkaError
import telebot  
import json


bot = telebot.TeleBot(token='6032445966:AAGo-AkteKJIpeoNO1gtrGG4lusbppUUrNE')
chat_id = '1224465429'


# Configuration for Kafka consumer
kafka_bootstrap_servers = "kafka:9092"
kafka_topic_wishlist = "wishlist"
kafka_group_id = "my-consumer-group"

# Create Kafka consumer
consumer = KafkaConsumer(kafka_topic_wishlist, bootstrap_servers = "kafka:9092", group_id = 'my-consumer-group')

# Subscribe to the Kafka topic
consumer.subscribe([kafka_topic_wishlist])

try:
    while True:
        msgs = consumer.poll()  # Poll for new messages

        for topic_partition, messages in msgs.items():
            for message in messages:
                if 'error' in message:
                    if message['error'].code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f"Error occurred: {message['error'].str()}")
                        break

                # Process the received message
                event_data = message.value.decode("utf-8")
                print("Received event data:", event_data)

except KeyboardInterrupt:
    pass

# Close the Kafka consumer
consumer.close()
'''
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

'''
        # Send notification to the user's smartphone using Telegram or another messaging service

