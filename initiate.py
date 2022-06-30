from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from datetime import datetime, timedelta

from pymongo import *
from credentials import *


def gender(update, context):
    context.chat_data["state"] = "gender"

    keyboard = [
        [
            InlineKeyboardButton("Male", callback_data="male"),
            InlineKeyboardButton("Female", callback_data="female"),
            InlineKeyboardButton("Prefer not to say",
                                 callback_data="gender_null")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "What is your gender? (Note that you will not have a say in the gender of your study buddies if you choose ‘prefer not to say’)", reply_markup=reply_markup)

    return


def initiate_date(update, context):
    context.chat_data["state"] = "date"

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
            curr_day + "/" + curr_month + "/" + curr_year, callback_data="date_"+str(i + 1)))

        col += 1
        col %= 3

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Please select your desired date for your study session", reply_markup=reply_markup)

    return


def initiate_time(update, context):
    context.chat_data["state"] = "time"

    keyboard = [
        [
            InlineKeyboardButton("Morning <1200", callback_data="morning")
        ],
        [
            InlineKeyboardButton("Afternoon 1200<=x<=1800",
                                 callback_data="afternoon")
        ],
        [
            InlineKeyboardButton("Evening >1800", callback_data="evening")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "What time would you like to have your study session", reply_markup=reply_markup)

    return


def course(update, context):
    context.chat_data["state"] = "course"
    keyboard = [
        [
            InlineKeyboardButton("Computer Engineering", callback_data="CEG")
        ],
        [
            InlineKeyboardButton("Electrical Engineering", callback_data="EE")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "What is your course?", reply_markup=reply_markup)

    return



def year(update, context):
    context.chat_data["state"] = "year"

    keyboard = [
        [
            InlineKeyboardButton("Year One", callback_data="year_one"),
            InlineKeyboardButton("Year Two", callback_data="year_two")
        ],
        [
            InlineKeyboardButton("Year Three", callback_data="year_three"),
            InlineKeyboardButton("Year Four", callback_data="year_four")
        ],
        [
            InlineKeyboardButton("Year Five", callback_data="year_five")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "What year are you in?", reply_markup=reply_markup)

    return


def location(update, context):
    context.chat_data["state"] = "location"

    update.callback_query.message.reply_text("Where would you like to study?")

    return


def pax(update, context):
    context.chat_data["state"] = "pax"

    keyboard = [
        [
            InlineKeyboardButton("2", callback_data="pax_two")
        ],
        [
            InlineKeyboardButton("3", callback_data="pax_three")
        ],
        [
            InlineKeyboardButton("4", callback_data="pax_four")
        ],
        [
            InlineKeyboardButton("5", callback_data="pax_five")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "How many people would you like in your study session?", reply_markup=reply_markup)

    return


def remark(update, context):
    context.chat_data["state"] = "remark"

    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="remark_yes")
        ],
        [
            InlineKeyboardButton("No", callback_data="remark_no")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Any additional remarks?", reply_markup=reply_markup)

    return


def add_remark(update, context):
    context.chat_data["state"] = "add_remark"

    update.callback_query.message.reply_text(
        "What remark would you like to add?")

    return


def store_data(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="store_data_yes"),
            InlineKeyboardButton("No", callback_data="store_data_no")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if context.chat_data["state"] == "add_remark":
        # catch error when user clicks "remark_no" after "remark_yes"
        try:
            update.message.reply_text(
                "Would you like your data to be stored?", reply_markup=reply_markup)
        except:
            update.callback_query.message.reply_text(
                "Would you like your data to be stored?", reply_markup=reply_markup)
    elif context.chat_data["state"] == "remark":
        update.callback_query.message.reply_text(
            "Would you like your data to be stored?", reply_markup=reply_markup)
    # catch potential error
    else:
        try:
            update.callback_query.message.reply_text(
                "Would you like your data to be stored?", reply_markup=reply_markup)
        except:
            update.message.reply_text(
                "Would you like your data to be stored?", reply_markup=reply_markup)

    context.chat_data["state"] = "store_data"

    return


def which_data(update, context):
    context.chat_data["state"] = "which_data"

    keyboard = [
        [
            InlineKeyboardButton("Gender", callback_data="gender")
        ],
        [
            InlineKeyboardButton("Course", callback_data="course")
        ],
        [
            InlineKeyboardButton("Year", callback_data="year")
        ],
        [
            InlineKeyboardButton("Location", callback_data="location")

        ],
        [
            InlineKeyboardButton("Pax", callback_data="pax")
        ],
        [
            InlineKeyboardButton("Done", callback_data="done")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Which data would you like to store?", reply_markup=reply_markup)

    return


def end(update, context):
    context.chat_data["state"] = "end"

    update.callback_query.message.reply_text(
        "Your study session has been posted successfully! We will update you when someone joined your session")

    return ConversationHandler.END
