import telebot
import steam_data
from psql.data import insert_client, add_game_to_wishlist

def run_telegram_bot(TK):
    bot = telebot.TeleBot(token=TK)
    bot.remove_webhook()

    start_flag = False

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
        nonlocal start_flag

        if start_flag:
            user_text = message.text
            chat_id = message.from_user.id
            gName, gPrice, gDiscount = steam_data.price_discount(user_text)
            gMessage = f"The game {gName} is costing {gPrice} with {gDiscount}% discount.\n"
            print(f"Received message: {user_text}")
            print(f"Game info: {gName}, {gPrice}, {gDiscount}")
            bot.send_message(chat_id, gMessage)
            bot.send_message(chat_id, "Add to wishlist? (y/n)")
            print(gName, gPrice, gDiscount)
            user_input = message.text.strip().lower()
            print("blau")
            
            if user_input == 'y' and gDiscount > 0:
                chat_id = message.from_user.id
                print("blau1")
                add_game_to_wishlist(client_id=chat_id, game_name=gName, game_price= gPrice, game_discount=gDiscount, game_promotion=True)
                print("blau1")

                wishlist[gName] = {
                    "price": gPrice,
                    "discount": gDiscount,
                    "promotion": True
                }
                bot.send_message(chat_id, "Game added to wishlist!")
                bot.send_message(chat_id, "Do you want to add another game? (y/n)")
                start_flag = True  # Set start flag to allow input for another game
            elif user_input == 'y' and gDiscount == 0:
                chat_id = message.from_user.id
                add_game_to_wishlist(client_id=chat_id, game_name=gName, game_price= gPrice, game_discount=gDiscount, game_promotion=True)
                wishlist[gName] = {
                    "price": gPrice,
                    "discount": gDiscount,
                    "promotion": False
                }
                bot.send_message(chat_id, "Game added to wishlist!")
                bot.send_message(chat_id, "Do you want to add another game? (y/n)")
                start_flag = True  # Set start flag to allow input for another game
            elif user_input == 'n':
                chat_id = message.from_user.id
                bot.send_message(chat_id, "Game not added to wishlist!")
                bot.send_message(chat_id, "Do you want to add another game? (y/n)")
                start_flag = True  # Set start flag to allow input for another game


    bot.polling()  
    return wishlist

    # Start the bot
bot_token = "6032445966:AAGo-AkteKJIpeoNO1gtrGG4lusbppUUrNE"
wishlist = run_telegram_bot(TK=bot_token)
print("Wishlist:", wishlist)

