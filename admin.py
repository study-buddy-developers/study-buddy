from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from pymongo import *
from credentials import *
from first_time import first_time, initiate_or_join


###
# commands
###


def start(update: Update, context: CallbackContext):
    context.chat_data["state"] = "start"

    context.chat_data["user_id"] = str(update.message.from_user.id)
    context.chat_data["tele_handle"] = str(update.message.from_user.username)

    print("user_id: " + context.chat_data["user_id"])
    print("tele_handle: " + context.chat_data["tele_handle"])

    user_identification(update, context)

    return


def help(update: Update, context: CallbackContext):
    context.chat_data["state"] = "help"

    update.message.reply_text(
        """
    Available Commands:
    /start - Start Study Buddy Telegram Bot
    """
    )

    return


def unknown_command(update: Update, context: CallbackContext):
    context.chat_data["state"] = "unknown_command"

    update.message.reply_text(
        "Sorry \"%s\" is not a valid command" % update.message.text)

    return


def unknown_text(update: Update, context: CallbackContext):
    context.chat_data["state"] = "unknown_text"

    update.message.reply_text(
        "Sorry I can't recognize you , you said \"%s\". Please use /start to start again." % update.message.text)

    return


###
# helper functions
###


def user_identification(update, context):
    context.chat_data["state"] = "user_identification"

    cursor = db.users.find_one({"user_id": context.chat_data["user_id"]})

    if cursor == None:
        first_time(update, context)
    else:
        update.message.reply_text(
            "Welcome back " + context.chat_data["tele_handle"] + "! What do we have planned for this week?")

        initiate_or_join(update, context)

    return
