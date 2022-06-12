from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from datetime import datetime, timedelta


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

        keyboard[row].append(InlineKeyboardButton(
            curr_day + "/" + curr_month + "/" + curr_year, callback_data="join_date_"+str(i + 1)))

        col += 1
        col %= 3

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Please select your desired date for your study session", reply_markup=reply_markup)

    return


def join_time(update, context):
    context.chat_data["state"] = "join_time"

    keyboard = [
        [
            InlineKeyboardButton("Morning <1200", callback_data="join_morning")
        ],
        [
            InlineKeyboardButton("Afternoon 1200<=x<=1800",
                                 callback_data="join_afternoon")
        ],
        [
            InlineKeyboardButton("Evening >1800", callback_data="join_evening")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "What time would you like to have your study session", reply_markup=reply_markup)

    return


def available(update, context, time):
    keyboard = [
        [
            InlineKeyboardButton("Display", callback_data="contact")
        ],
        [
            InlineKeyboardButton("Available",
                                 callback_data="contact")
        ],
        [
            InlineKeyboardButton("Timings", callback_data="contact")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(
        time, reply_markup=reply_markup)

    return


def prompt_contact(update, context):
    update.callback_query.message.reply_text(
        "Please kindly contact your initiator @initiator_telegram_handle")
    return
