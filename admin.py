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


def tele_handle(update, context):
    context.chat_data["state"] = "tele_handle"

    # update.message.reply_text(update.message.from_user.username)

    return update.message.from_user.username


def begin(update, context):
    context.chat_data["state"] = "begin"
    context.chat_data["id"] = user_id(update, context)
    context.chat_data["tele_handle"] = tele_handle(update, context)

    print("user_id: " + str(context.chat_data["id"]))
    print("tele_handle: " + str(context.chat_data["tele_handle"]))

    first_time(update, context)


def purge_data(update, context):
    context.chat_data["gender"] = ""
    context.chat_data["course"] = ""
    context.chat_data["year"] = ""
    context.chat_data["location"] = ""
    context.chat_data["pax"] = ""

    return


def create_study_session(update, context):
    # sessions
    session_id = db.sessions.insert_one(
        {"user_id_array": [context.chat_data["id"]]}).inserted_id
    filter_con = {"_id": session_id}

    new_con = {"$set": {"date": context.chat_data["initiate_date"]}}
    db.sessions.update_one(filter_con, new_con)

    new_con = {"$set": {"time": context.chat_data["initiate_time"]}}
    db.sessions.update_one(filter_con, new_con)

    new_con = {"$set": {"location": context.chat_data["location"]}}
    db.sessions.update_one(filter_con, new_con)

    new_con = {"$set": {"pax": context.chat_data["pax"]}}
    db.sessions.update_one(filter_con, new_con)

    new_con = {"$set": {"year": context.chat_data["year"]}}
    db.sessions.update_one(filter_con, new_con)

    new_con = {"$set": {"course": context.chat_data["course"]}}
    db.sessions.update_one(filter_con, new_con)

    new_con = {"$set": {"gender": context.chat_data["gender"]}}
    db.sessions.update_one(filter_con, new_con)

    new_con = {"$set": {"remarks": context.chat_data["remarks"]}}
    db.sessions.update_one(filter_con, new_con)

    # dates
    cursor = db.dates.find({"date": context.chat_data["initiate_date"]})
    if list(cursor) == []:
        date_id = db.dates.insert_one(
            {"date": context.chat_data["initiate_date"]}).inserted_id
        filter_con = {"_id": date_id}

        new_con = {"$set": {"sessions": [session_id]}}
        db.dates.update_one(filter_con, new_con)
    else:
        filter_con = {"date": context.chat_data["initiate_date"]}
        new_con = {"$push": {"sessions": session_id}}
        db.dates.update_one(filter_con, new_con)


def valid_date(date):
    cursor = db.dates.find_one({"date": date})

    if cursor == None:
        return False

    sessions = cursor["sessions"]

    for session in sessions:
        if valid_session(session):
            return True
    return False


def valid_session(session):
    cursor = db.sessions.find_one({"_id": session})

    pax = len(cursor["user_id_array"])
    total_pax = cursor["pax"][-1]

    if pax == total_pax:
        return False
    return True


# def valid_time(update, context, time):
#     date = context.chat_data["join_date"]

#     cursor = db.dates.find(
#         {"$and": [{"date": date}, {time: {"$not": {"$size": 0}}}]})
#     if list(cursor) == []:
#         return False
#     return True


def available_sessions(update, context):
    date = context.chat_data["join_date"]

    cursor = db.dates.find_one({"date": date})

    sessions = cursor["sessions"]

    valid_sessions = []
    for session in sessions:
        if valid_session(session):
            cursor = db.sessions.find_one({"_id": session})

            # current pax
            current_pax = len(cursor["user_id_array"])

            # time
            time = cursor["time"]

            # location
            location = cursor["location"]

            # pax
            pax = cursor["pax"][-1]

            # year
            if cursor["year"] == "year_one":
                year = "Y1"
            elif cursor["year"] == "year_two":
                year = "Y2"
            elif cursor["year"] == "year_three":
                year = "Y3"
            elif cursor["year"] == "year_four":
                year = "Y4"
            elif cursor["year"] == "year_five":
                year = "Y5"

            # course
            course = cursor["course"].split("_")[1]

            # gender
            gender = cursor["gender"]

            if gender == "gender_null":
                gender = ""

            # remarks
            remarks = cursor["remarks"]

            session_details = [str(year) + " " + str(course) + ", " + str(gender) + ", " + str(date) + " " + str(
                time) + " @" + str(location) + " (" + str(current_pax) + "/" + str(pax) + " pax)", session]

            valid_sessions.append(session_details)

    return valid_sessions
