import telebot
import steam_data
from psql.data import insert_client, add_game_to_wishlist

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
            id_client = insert_client(first_name=first_name, last_name=last_name, idtelegram=chat_id)
            bot.send_message(chat_id, "Hello! Type a game.")
            start_flag = True


    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        nonlocal start_flag, wishlist_flag

        if start_flag and not wishlist_flag:
            user_text = message.text
            chat_id = message.from_user.id
            gName, gPrice, gDiscount = steam_data.get_game(user_text)
            gMessage = f"The game {gName} is costing {gPrice} with {gDiscount}% discount.\n"
            bot.send_message(chat_id, gMessage)
            bot.send_message(chat_id, "Add to wishlist? (y/n)")
            wishlist_flag = True

        elif wishlist_flag:
            wishlist_flag = False
            user_input = message.text.strip().lower()
            if user_input == 'y' and gDiscount > 0:
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name
                chat_id = message.from_user.id
                add_game_to_wishlist(first_name=first_name, last_name=last_name, client_id=chat_id, game_name=gName, game_promotion=True)
                wishlist[gName] = {
                    "price": gPrice,
                    "discount": gDiscount,
                    "promotion": True
                }
                bot.send_message(chat_id, "Game added to wishlist!")
            elif user_input == 'y' and gDiscount == 0:
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name
                chat_id = message.from_user.id
                add_game_to_wishlist(first_name=first_name, last_name=last_name, client_id=chat_id, game_name=gName, game_promotion=False)
                wishlist[gName] = {
                    "price": gPrice,
                    "discount": gDiscount,
                    "promotion": False
                }
                bot.send_message(chat_id, "Game added to wishlist!")
            elif user_input == 'n':
                bot.send_message(chat_id, "Game not added to wishlist!")

    # Start the bot
    bot.polling()   