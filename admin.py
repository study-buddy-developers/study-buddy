from turtle import up
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from first_time import first_time

from pymongo import *
from credentials import *


def start(update: Update, context: CallbackContext):
    context.chat_data["state"] = "start"

    update.message.reply_text(
        "Hello there, Welcome to the Bot. Please write /help to see the commands available.")

    return


def help(update: Update, context: CallbackContext):
    context.chat_data["state"] = "help"

    update.message.reply_text(
        """
    Available Commands:
    /begin - Start Study Buddy Telegram Bot
    """
    )

    return


def unknown_command(update: Update, context: CallbackContext):
    context.chat_data["state"] = "unknown_command"

    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)

    return


def unknown_text(update: Update, context: CallbackContext):
    context.chat_data["state"] = "unknown_text"

    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'. Please use /begin to start again." % update.message.text)

    return


def user_id(update, context):
    context.chat_data["state"] = "user_id"

    # update.message.reply_text(update.message.from_user.id)

    return update.message.from_user.id


def begin(update, context):
    context.chat_data["state"] = "begin"
    context.chat_data["id"] = user_id(update, context)

    print("User_id: " + str(context.chat_data["id"]))

    first_time(update, context)


def purge_data(update, context):
    context.chat_data["gender"] = ""
    context.chat_data["course"] = ""
    context.chat_data["year"] = ""
    context.chat_data["location"] = ""
    context.chat_data["pax"] = ""

    return


def create_study_session(update, context):
    # date
    # time
    # pax
    # user_id []
    date_time = str(context.chat_data["initiate_date"]) + \
        " " + str(context.chat_data["initiate_time"])

    cursor = db.sessions.find(
        {"$and": [{"date_time": date_time}, {"user_id_array.0": context.chat_data["id"]}]})
    if list(cursor) == []:
        db.sessions.insert_many(
            [{"date_time": date_time}, {"user_id_array.0": context.chat_data["id"]}])

    # filter_con = {"userid": context.chat_data["id"]}
    # new_con = {"$set": {query.data: context.chat_data[query.data]}}
    # db.users.update_one(filter_con, new_con)
