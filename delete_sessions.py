from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from pymongo import *
from credentials import *
from bson.objectid import ObjectId

# "delete_session" + str(sess)
# def delete_sessions(update,context,sess):
#     context.chat_data["state"] = "delete_session"
#     sessid = ObjectId(sess)
    
