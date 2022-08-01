from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from datetime import datetime, timedelta
from bson.objectid import ObjectId

from pymongo import *
from credentials import *


def join_date(update, context):
    context.chat_data["state"] = "join_date"

    keyboard = [[]]

    col = 0
    row = -1

    for i in range(7):
        curr_date = datetime.now() + timedelta(days=i)
        curr_day = str(curr_date.day)
        curr_month = str(curr_date.month)
        curr_year = str(curr_date.year)

        date = curr_day + "/" + curr_month + "/" + curr_year

        if valid_date(update, context, date):
            keyboard[row].append(InlineKeyboardButton(
                date, callback_data="join_date_"+str(i)))

            col += 1
            col %= 3

            if col == 0:
                keyboard.append([])
                row += 1
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Please select your desired date for your study session.", reply_markup=reply_markup)

    return


def no_sessions(update, context):
    context.chat_data["state"] = "no_sessions"

    keyboard = [
        [InlineKeyboardButton("Initiate", callback_data="initiate")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "There are no study sessions available at the moment, would you like to initiate one?", reply_markup=reply_markup)

    return


def join_sessions(update, context):
    keyboard = []

    sessions = available_sessions(update, context)

    for session in sessions:
        session_details = session[0]
        session_id = session[1]
        keyboard.append([InlineKeyboardButton(session_details,
                        callback_data="join_session_" + str(session_id))])
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Which session would you like to join?", reply_markup=reply_markup)

    return


def prompt_contact(update, context):
    contact = context.chat_data["initiator_telegram_handle"]

    update.callback_query.message.reply_text(
        "Please kindly contact your initiator @" + contact)

    return


###
# helper functions
###


def valid_date(update, context, date):
    cursor = db.dates.find_one({"date": date})

    if cursor == None:
        return False

    sessions = cursor["sessions"]

    for session in sessions:
        if valid_session(update, context, session):
            return True
    return False


def valid_session(update, context, session):
    cursor = db.sessions.find_one({"_id": session})

    if context.chat_data["user_id"] in cursor["user_id_array"]:
        return False

    pax = len(cursor["user_id_array"])
    total_pax = int(cursor["pax"][-1])

    if pax == total_pax:
        return False
    return True


def available_sessions(update, context):
    date = context.chat_data["join_date"]

    cursor = db.dates.find_one({"date": date})

    sessions = cursor["sessions"]

    valid_sessions = []
    for session in sessions:
        if valid_session(update, context, session):
            cursor = db.sessions.find_one({"_id": session})

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

            # time
            time = cursor["time"]

            # location
            location = cursor["location"]

            # current pax
            current_pax = len(cursor["user_id_array"])

            # pax
            pax = cursor["pax"][-1]

            # remarks
            remarks = cursor["remarks"]

            if gender == "gender_null":
                session_details = [str(year) + " " + str(course) + ", " + str(date) + " " + str(time) + "H @" + str(
                    location) + " (Remarks: " + str(remarks) + ") (" + str(current_pax) + "/" + str(pax) + " pax)", session]
            else:
                session_details = [str(year) + " " + str(course) + ", " + str(gender).capitalize() + ", " + str(date) + " " + str(
                    time) + "H @" + str(location) + " (Remarks: " + str(remarks) + ") (" + str(current_pax) + "/" + str(pax) + " pax)", session]

            valid_sessions.append(session_details)

    return valid_sessions
