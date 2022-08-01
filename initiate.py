from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from datetime import datetime, timedelta

from pymongo import *
from credentials import *


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
            InlineKeyboardButton("0900", callback_data="0900"),
            InlineKeyboardButton("1000", callback_data="1000"),
            InlineKeyboardButton("1100", callback_data="1100"),
            InlineKeyboardButton("1200", callback_data="1200"),
            InlineKeyboardButton("1300", callback_data="1300")
        ],
        [
            InlineKeyboardButton("1400", callback_data="1400"),
            InlineKeyboardButton("1500", callback_data="1500"),
            InlineKeyboardButton("1600", callback_data="1600"),
            InlineKeyboardButton("1700", callback_data="1700"),
            InlineKeyboardButton("1800", callback_data="1800")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "What time would you like to have your study session", reply_markup=reply_markup)

    return


def update_data(update, context):
    context.chat_data["state"] = "update_data"

    stored_data = context.chat_data["stored_data"]

    keyboard = []
    for data in stored_data:
        keyboard.append(
            [
                InlineKeyboardButton(
                    data.capitalize(), callback_data="update_" + data)
            ]
        )
    keyboard.append([InlineKeyboardButton(
        "Done", callback_data="update_done")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "We noted that you have stored the following data previously. Would you like to update them?", reply_markup=reply_markup)

    return


def edit_update_data(update, context):
    context.chat_data["state"] = "edit_update_data"

    stored_data = context.chat_data["stored_data"]

    keyboard = []
    for data in stored_data:
        keyboard.append(
            [
                InlineKeyboardButton(
                    data.capitalize(), callback_data="update_" + data)
            ]
        )
    keyboard.append([InlineKeyboardButton(
        "Done", callback_data="update_done")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    context.bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )

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

    try:
        update.message.reply_text(
            "What year are you in?", reply_markup=reply_markup)
    except:
        update.callback_query.message.reply_text(
            "What year are you in?", reply_markup=reply_markup)

    return


def course(update, context):
    context.chat_data["state"] = "course"
    keyboard = [
        [
            InlineKeyboardButton(
                "Electrical Engineering (EE)", callback_data="CDE_EE")
        ],
        [
            InlineKeyboardButton(
                "Computer Engineering (CEG)", callback_data="CDE_CEG")
        ]

        # [
        #     InlineKeyboardButton("Architecture (ARCH)",
        #                          callback_data="CDE_ARCH")
        # ],
        # [
        #     InlineKeyboardButton(
        #         "Biomedical Engineering (BME)", callback_data="CDE_BME")
        # ],
        # [
        #     InlineKeyboardButton(
        #         "Chemical Engineering (CHBE)", callback_data="CDE_CHBE")
        # ],
        # [
        #     InlineKeyboardButton("Civil Engineering (CEE)",
        #                          callback_data="CDE_CEE")
        # ],
        # [
        #     InlineKeyboardButton(
        #         "Engineering Science Programme (ESP)", callback_data="CDE_ESP")
        # ],
        # [
        #     InlineKeyboardButton(
        #         "Environmental Engineering (ENV)", callback_data="CDE_ENV")
        # ],
        # [
        #     InlineKeyboardButton("Industrial Design (DID)",
        #                          callback_data="CDE_DID")
        # ],
        # [
        #     InlineKeyboardButton(
        #         "Industrial Systems Engineering and Management (ISEM)", callback_data="CDE_ISEM")
        # ],
        # [
        #     InlineKeyboardButton(
        #         "Infrastructure and project management (IPM)", callback_data="CDE_IPM")
        # ],
        # [
        #     InlineKeyboardButton(
        #         "Landscape architecture (LRCH)", callback_data="CDE_LRCH")
        # ],
        # [
        #     InlineKeyboardButton(
        #         "Material Science and Engineering (MSE)", callback_data="CDE_MSE")
        # ],
        # [
        #     InlineKeyboardButton(
        #         "Mechanical Engineering (ME)", callback_data="CDE_ME")
        # ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.message.reply_text(
            "What is your course?", reply_markup=reply_markup)
    except:
        update.callback_query.message.reply_text(
            "What is your course?", reply_markup=reply_markup)

    return


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

    try:
        update.message.reply_text(
            "What is your gender? (Note that you will not have a say in the gender of your study buddies if you choose ‘prefer not to say’)", reply_markup=reply_markup)
    except:
        update.callback_query.message.reply_text(
            "What is your gender? (Note that you will not have a say in the gender of your study buddies if you choose ‘prefer not to say’)", reply_markup=reply_markup)

    return


def location(update, context):
    context.chat_data["state"] = "location"

    try:
        update.message.reply_text("Where would you like to study?")
    except:
        update.callback_query.message.reply_text(
            "Where would you like to study?")

    return


def pax(update, context):
    context.chat_data["state"] = "pax"

    keyboard = [
        [
            InlineKeyboardButton("2", callback_data="pax_2")
        ],
        [
            InlineKeyboardButton("3", callback_data="pax_3")
        ],
        [
            InlineKeyboardButton("4", callback_data="pax_4")
        ],
        [
            InlineKeyboardButton("5", callback_data="pax_5")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.message.reply_text(
            "How many people would you like in your study session?", reply_markup=reply_markup)
    except:
        update.callback_query.message.reply_text(
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

    try:
        update.message.reply_text(
            "Any additional remarks?", reply_markup=reply_markup)
    except:
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

    try:
        update.message.reply_text(
            "Would you like your data to be stored?", reply_markup=reply_markup)
    except:
        update.callback_query.message.reply_text(
            "Would you like your data to be stored?", reply_markup=reply_markup)

    context.chat_data["state"] = "store_data"

    return


def which_data(update, context):
    context.chat_data["state"] = "which_data"

    stored_data = context.chat_data["stored_data"]

    keyboard = []
    for data in stored_data:
        if data in context.chat_data:
            keyboard.append([InlineKeyboardButton(
                data.capitalize(), callback_data=data)])
    keyboard.append([InlineKeyboardButton("Done", callback_data="store_done")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Which data would you like to store?", reply_markup=reply_markup)

    return


def edit_which_data(update, context):
    context.chat_data["state"] = "edit_which_data"

    stored_data = context.chat_data["stored_data"]

    keyboard = []
    for data in stored_data:
        if data in context.chat_data:
            keyboard.append([InlineKeyboardButton(
                data.capitalize(), callback_data=data)])
    keyboard.append([InlineKeyboardButton("Done", callback_data="store_done")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    context.bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )

    return


def end(update, context):
    context.chat_data["state"] = "end"

    create_study_session(update, context)

    purge_data(update, context)

    update.callback_query.message.reply_text(
        "Your study session has been posted successfully! We will update you when someone joined your session")

    return ConversationHandler.END


###
# helper functions
###


def check_data(update, context):
    cursor = db.users.find_one({"user_id": context.chat_data["user_id"]})

    stored_data = []

    data = ["year", "course", "gender", "location", "pax", "remarks"]

    for d in data:
        if cursor[d] != "":
            stored_data.append(d)

    context.chat_data["stored_data"] = stored_data

    return stored_data


def next_data(update, context):
    data = ["year", "course", "gender", "location", "pax", "remarks"]

    for d in data:
        if d not in context.chat_data["stored_data"]:
            if d == "year":
                year(update, context)
                context.chat_data["stored_data"].append("year")
            elif d == "course":
                course(update, context)
                context.chat_data["stored_data"].append("course")
            elif d == "gender":
                gender(update, context)
                context.chat_data["stored_data"].append("gender")
            elif d == "location":
                location(update, context)
                context.chat_data["stored_data"].append("location")
            elif d == "pax":
                pax(update, context)
                context.chat_data["stored_data"].append("pax")
            elif d == "remarks":
                remark(update, context)
                context.chat_data["stored_data"].append("remarks")
            return

    store_data(update, context)

    return


def create_study_session(update, context):
    # sessions
    session_id = db.sessions.insert_one(
        {"user_id_array": [context.chat_data["user_id"]]}).inserted_id
    filter_con = {"_id": session_id}

    new_con = {"$set": {"date": context.chat_data["initiate_date"]}}
    db.sessions.update_one(filter_con, new_con)

    new_con = {"$set": {"time": context.chat_data["initiate_time"]}}
    db.sessions.update_one(filter_con, new_con)

    data = ["year", "course", "gender", "location", "pax", "remarks"]

    for d in data:
        if d in context.chat_data:
            new_con = {"$set": {d: context.chat_data[d]}}
        else:
            cursor = db.users.find_one(
                {"user_id": context.chat_data["user_id"]})
            new_con = {"$set": {d: cursor[d]}}
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


def purge_data(update, context):
    context.chat_data.clear()

    return
