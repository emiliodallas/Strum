from steam import Steam
from decouple import config
import json

KEY = config("STEAM_API_KEY")
steam = Steam(KEY) 

def get_game():
    game_in = input("Type game name: \n")
    return game_in

def get_user():
    user_in = input("Type username: \n")
    return user_in

import requests

def price_discount(name):
    game_out = steam.apps.search_games(name)
    game_id = game_out["apps"][0]["id"]
    game_detail = json.loads(steam.apps.get_app_details(game_id))
    discount = game_detail[str(game_id)]["data"]["price_overview"]["discount_percent"]
    price = game_detail[str(game_id)]["data"]["price_overview"]["final_formatted"]
    full_name = game_detail[str(game_id)]["data"]["name"]

    return full_name, price, discount


