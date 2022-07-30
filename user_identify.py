from telegram.ext import CallbackContext
from datetime import datetime, timedelta
from bson.objectid import ObjectId

from initiate import *

def user_identify(update, context):
    print("Start user identify")
    cursor = db.users.find({"user_id": context.chat_data["id"]})
    if bool(list(cursor)) == False: # Checcking if the system has records for the user, empty list means this is a first time user.
        print("New user")
        db.users.insert_one(
            {"user_id": context.chat_data["id"]}
        ) 
        update.message.reply_text(
            "Hi! Welcome to Study Buddy Telegram Bot! There are a few things to take note of before we begin...",
            "1",
            "Come up with Term Of Use" # Insert Term Of Use here once it's properly drafted out
        )
        print(cursor)
    else:
        print("Existing user")
        user_handle = db.users.find({"user_id":context.chat_data["tele_handle"]})
        update.message.reply_text(
            "Welcome back :{}".format(user_handle) + "! What do we have planned for this week?"
        )
        print("Welcome msg sent")

        return