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

def price_discount(name):
    game_out = steam.apps.search_games(name)
    games = game_out["apps"]
    print(game_out)
    
    if not games:
        return None, None, None
    
    for game in games:
        game_id = game["id"]
        game_detail = json.loads(steam.apps.get_app_details(game_id))
        
        if str(game_id) in game_detail:
            discount = game_detail[str(game_id)]["data"]["price_overview"]["discount_percent"]
            price = game_detail[str(game_id)]["data"]["price_overview"]["final_formatted"]
            full_name = game_detail[str(game_id)]["data"]["name"]
            
            return full_name, price, discount
    
    return None, None, None

