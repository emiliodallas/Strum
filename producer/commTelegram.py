import requests
import telebot
from flask import Flask



class Telegram:
    """
    Telegram Bot!
    """

    def __init__(self, token, destinationID):
        self.token = token
        self.destID = destinationID
        self.urlWR = f'https://api.telegram.org/bot{token}/sendMessage'
        self.urlRD = f'https://api.telegram.org/bot{token}/getUpdates'


    def messageWR(self, message):

        # Create URL
        # Create Message
        to_send = message

        # Send message
        requests.post(url = self.urlWR, data={"text": to_send})

    def messageRD_first(self):

        r = (requests.get(url=self.urlRD)).json()

        rData = r["result"]
        fName = rData[-1]["message"]["from"]["first_name"]
        lName = rData[-1]["message"]["from"]["last_name"]
        fId = rData[-1]["message"]["from"]["id"]
        lGame = rData[-1]["message"]["text"]
        return fName, lName, lGame, fId
    
    def wishlist_confirmation(self):
        

        r = (requests.get(url=self.urlRD)).json()

        rData = r["result"]
        wishlistFlag = rData[-1]["message"]["text"]
        return wishlistFlag.lower()