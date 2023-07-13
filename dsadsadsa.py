from steam import Steam
from decouple import config
import json

KEY = "6032445966:AAGo-AkteKJIpeoNO1gtrGG4lusbppUUrNE"


terraria_app_id = 105600
steam = Steam(KEY)

# arguments: app_id
user = steam.apps.get_app_details(terraria_app_id)
name = input("name")
game_out = steam.apps.search_games(name)
game_id = game_out["apps"][0]["id"]
game_detail = json.loads(steam.apps.get_app_details(game_id))
discount = game_detail[str(game_id)]["data"]["price_overview"]["discount_percent"]
price = game_detail[str(game_id)]["data"]["price_overview"]["final_formatted"]
full_name = game_detail[str(game_id)]["data"]["name"]

print(json.dumps(game_detail[str(game_id)]["data"]))

variable = None

if input() == "y":
    variable = 13

elif input() == "n":
    # Use the variable here
    print(variable)