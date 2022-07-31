from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from datetime import datetime, timedelta

from admin import valid_date, available_sessions


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

        if valid_date(date):
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
        [InlineKeyboardButton("initiate", callback_data="initiate")]
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
