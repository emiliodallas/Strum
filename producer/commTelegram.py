import telebot
import steam_data
from psql.data import add_game_to_wishlist, insert_client

def run_telegram_bot(TK):
    bot = telebot.TeleBot(token=TK)
    bot.remove_webhook()

    wishlist = {}
    game_info_dict = {}

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        chat_id = message.from_user.id
        print("Received /start command")

        bot.send_message(chat_id, f"Hello {first_name} {last_name}! Type a game.")
        insert_client(first_name=first_name, last_name=last_name, idtelegram=chat_id)

        bot.register_next_step_handler(message, handle_game_name)
        
    def handle_game_name(message):

        chat_id = message.from_user.id
        user_text = message.text

        gName, gPrice, gDiscount = steam_data.price_discount(user_text)
        gMessage = f"The game {gName} is costing {gPrice} with {gDiscount}% discount."

        print(f"Received message: {user_text}")
        print(f"Game info: {gName}, {gPrice}, {gDiscount}")

        bot.send_message(chat_id, gMessage)
        bot.send_message(chat_id, "Add to wishlist? (y/n)")

        # Store the game info as custom properties of the chat object
        game_info_dict[chat_id] = {
            "gName": gName,
            "gPrice": gPrice,
            "gDiscount": gDiscount
        }


        bot.register_next_step_handler(message, handle_wishlist)

    def handle_wishlist(message):

        chat_id = message.from_user.id
        user_input = message.text.strip().lower()

        if user_input == 'n':
            bot.send_message(chat_id, "Game not added to wishlist!")
            bot.send_message(chat_id, "Do you want to add another game? (y/n)")
            bot.register_next_step_handler(message, handle_repeat)

        else:
        # Retrieve the game info from the dictionary
            game_info = game_info_dict.get(chat_id)
            if game_info:
                gName = game_info.get("gName")
                gPrice = game_info.get("gPrice")
                gDiscount = game_info.get("gDiscount")

                if gName is not None and gPrice is not None and gDiscount is not None:                    
                    if gDiscount > 0:
                        add_game_to_wishlist(client_id=chat_id, game_name=gName, game_price= gPrice, game_discount=gDiscount, game_promotion=True)
                        bot.send_message(chat_id, "Game added to wishlist!")
                    else:
                        add_game_to_wishlist(client_id=chat_id, game_name=gName, game_price= gPrice, game_discount=gDiscount, game_promotion=False)
                        bot.send_message(chat_id, "Game added to wishlist!")

                    bot.send_message(chat_id, "Do you want to add another game? (y/n)")
                    bot.register_next_step_handler(message, handle_repeat)
                else:
                    print(gName, gPrice, gDiscount)
                    bot.send_message(chat_id, "Game information not found.")
                    print('1')
            else:
                bot.send_message(chat_id, "Game information not found.")
                print('2')

    def handle_repeat(message):

        chat_id = message.chat.id
        user_input = message.text.strip().lower()

        if user_input == 'y':
            bot.send_message(chat_id, "Type another game.")
            bot.register_next_step_handler(message, handle_game_name)
        else:
            bot.send_message(chat_id, "Goodbye!")
            


    bot.polling()  
    return wishlist

# Start the bot
bot_token = "6032445966:AAGo-AkteKJIpeoNO1gtrGG4lusbppUUrNE"
wishlist = run_telegram_bot(TK=bot_token)
print("Wishlist:", wishlist)
