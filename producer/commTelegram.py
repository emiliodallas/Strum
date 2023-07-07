import telebot
import steam_data
#from psql.data import insert_client, add_game_to_wishlist

def run_telegram_bot(TK):
    bot = telebot.TeleBot(token=TK)
    bot.remove_webhook()

    start_flag = False
    wishlist_flag = False

    wishlist = {}

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        nonlocal start_flag
        if not start_flag:
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            chat_id = message.from_user.id
            print("Received /start command")
            #id_client = insert_client(first_name=first_name, last_name=last_name, idtelegram=chat_id)
            bot.send_message(chat_id, f"Hello {first_name}! Type a game.")
            start_flag = True


    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        nonlocal start_flag, wishlist_flag

        if start_flag and not wishlist_flag:
            user_text = message.text
            chat_id = message.from_user.id

            game_results = steam_data.price_discount(user_text)
            if game_results:
                for game_id, game_price, game_discount in game_results:
                    gMessage = f"The game {game_id} is costing {game_price} with {game_discount}% discount.\n"
                    print(f"Received message: {user_text}")
                    print(f"Game info: {game_id}, {game_price}, {game_discount}")
                    bot.send_message(chat_id, gMessage)
                bot.send_message(chat_id, "Add to wishlist? (y/n)")
                wishlist_flag = True
            else:
                bot.send_message(chat_id, "No game found. Please try again.")

        elif wishlist_flag:
            wishlist_flag = False
            user_input = message.text.strip().lower()
            print(f"Received input: {user_input}")
            gDiscount = 0
            gPrice = 0
            gName = 0
            chat_id = 0
            if user_input == 'y' and gDiscount > 0:
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name
                chat_id = message.from_user.id
                #add_game_to_wishlist(first_name=first_name, last_name=last_name, client_id=chat_id, game_name=gName, game_promotion=True)
                wishlist[gName] = {
                    "price": gPrice,
                    "discount": gDiscount,
                    "promotion": True
                }
                bot.send_message(chat_id, "Game added to wishlist!")
                bot.send_message(chat_id, "Do you want to add another game? (y/n)")
                start_flag = True  # Set start flag to allow input for another game
            elif user_input == 'y' and gDiscount == 0:
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name
                chat_id = message.from_user.id
                #add_game_to_wishlist(first_name=first_name, last_name=last_name, client_id=chat_id, game_name=gName, game_promotion=False)
                wishlist[gName] = {
                    "price": gPrice,
                    "discount": gDiscount,
                    "promotion": False
                }
                bot.send_message(chat_id, "Game added to wishlist!")
                bot.send_message(chat_id, "Do you want to add another game? (y/n)")
                start_flag = True  # Set start flag to allow input for another game
            elif user_input == 'n':
                bot.send_message(chat_id, "Game not added to wishlist!")
                bot.send_message(chat_id, "Type another game to search: ")
                start_flag = True

    bot.polling()  
    return wishlist

    # Start the bot
bot_token = "6032445966:AAGo-AkteKJIpeoNO1gtrGG4lusbppUUrNE"
wishlist = run_telegram_bot(TK=bot_token)
print("Wishlist:", wishlist)