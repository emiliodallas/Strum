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

#user_in = get_user()

#game_in = get_game()

#user_out = steam.users.search_user("emilio")

game_out = steam.apps.search_games("wingspan")
game_id = game_out["apps"][0]["id"]

game_detail = json.loads(steam.apps.get_app_details(game_id))

price_overview = json.dumps(game_detail["1054490"]["data"]["price_overview"], indent=4)
print(price_overview)


#print(user_out["player"]["profileurl"])