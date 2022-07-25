from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from datetime import datetime, timedelta

from admin import valid_date, valid_time, available_sessions


def join_date(update, context):
    context.chat_data["state"] = "join_date"

    keyboard = []

    col = 0
    row = -1

    for i in range(7):
        if col == 0:
            keyboard.append([])
            row += 1

        curr_date = datetime.now() + timedelta(days=i)
        curr_day = str(curr_date.day)
        curr_month = str(curr_date.month)
        curr_year = str(curr_date.year)

        date = curr_day + "/" + curr_month + "/" + curr_year

        if valid_date(update, context, date):
            keyboard[row].append(InlineKeyboardButton(
                date, callback_data="join_date_"+str(i + 1)))

            col += 1
            col %= 3
    for elem in keyboard:
        if elem != []:
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.callback_query.message.reply_text(
                "Please select your desired date for your study session.", reply_markup=reply_markup)
            return

    no_sessions(update, context)
    return


def no_sessions(update, context):
    context.chat_data["state"] = "no_sessions"
    keyboard = [
        [InlineKeyboardButton("initiate", callback_data="initiate")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "There are no study sessions available at the moment, would you like to initiate one?", reply_markup=reply_markup)
    return


def join_time(update, context):
    context.chat_data["state"] = "join_time"

    keyboard = []

    timings = ["morning", "afternoon", "evening"]
    timings_texts = [
        "Morning <1200",
        "Afternoon 1200<=x<=1800",
        "Evening >1800"
    ]

    for i in range(len(timings)):
        time = timings[i]

        if valid_time(update, context, time):
            keyboard.append([InlineKeyboardButton(
                timings_texts[i], callback_data="join_"+time)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "What time would you like to have your study session?", reply_markup=reply_markup)

    return


def join_sessions(update, context):
    keyboard = []

    sessions = available_sessions(update, context)

    for sess in sessions:
        session = sess[0]
        sess_ID = sess[1]
        keyboard.append([InlineKeyboardButton(
            session, callback_data="contact_" + str(sess_ID))])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Which session would you like to join?", reply_markup=reply_markup)

    return


def prompt_contact(update, context):
    contact = context.chat_data["initiator_telegram_handle"]

    update.callback_query.message.reply_text(
        "Please kindly contact your initiator @" + contact)

    return
