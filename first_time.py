from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from pymongo import *
from credentials import *
from email_verification import email_verification


def first_time(update, context):
    context.chat_data["state"] = "first_time"

    keyboard = [
        [
            InlineKeyboardButton("I acknowledge!", callback_data="acknowledge")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # terms and conditions
    update.message.reply_text(
        "Welcome to StudyBuddy Telegram Bot!\nBefore we begin, please read through these terms and conditions carefully.\n\n*Our mission is to provide a platform for ECE students to find their study buddies*\n\n*All the data that is collected by the bot will be kept confidential*\n\n*Your telegram handle will be sent to the students who are in the same session*\n\nOur terms and conditions were last updated on 30th Jul 2022.\n\nWith all that have been said, have fun with the bot and happy studying!", reply_markup=reply_markup
    )

    return


def email(update, context):
    context.chat_data["state"] = "email"

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="To verify your identity, what is your NUS email? (ending with @u.nus.edu)"
    )

    return


def verification(update, context):
    context.chat_data["state"] = "verification"

    text = update.message.text

    context.chat_data["email"] = text

    if text.endswith("@u.nus.edu"):
        context.chat_data["verification_code"] = email_verification(
            context.chat_data["email"])

        update.message.reply_text(
            "A verification code has been sent to " + str(text) + " Please check and enter the code here to complete the verification. The code may be in your spam folder.")

    else:
        update.message.reply_text(
            "Sorry, I do not recognise that email. You entered: " + text)

        email(update, context)

    return


def code(update, context):
    context.chat_data["state"] = "code"

    code = update.effective_message.text

    verification_code = context.chat_data["verification_code"]

    if code == verification_code:
        update.message.reply_text(
            "Thank you! Your email has been verified!")

        context.chat_data["verification_code"] = ""

        initiate_or_join(update, context)

    else:
        update.message.reply_text(
            "Sorry, the verification code you have entered is incorrect.")

        context.chat_data["verification_code"] = ""

        wrong_code(update, context)

    return


def wrong_code(update, context):
    context.chat_data["state"] = "wrong_code"

    keyboard = [
        [
            InlineKeyboardButton("Resend", callback_data="resend")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Please click the resend button for a new code."
        " If you have entered your email incorrectly, please send your email (ending with @u.nus.edu) again.", reply_markup=reply_markup)

    return


def new_code(update, context):
    context.chat_data["state"] = "new_code"

    context.chat_data["verification_code"] = email_verification(
        context.chat_data["email"])

    update.callback_query.message.reply_text(
        "A new code has been sent to your email. Please check and enter the code here to complete the verification. The code may be in your spam folder.")

    return


def initiate_or_join(update, context):
    update_user(update, context)

    context.chat_data["state"] = "initiate_or_join"
    user_id = context.chat_data["user_id"]
    cursor = db.users.find_one({"$and":[{"user_id": user_id},{"sessions_initiated": { "$exists": "True" }}]})
    if cursor and cursor["sessions_initiated"]!=[]:
        keyboard = [
            [
                InlineKeyboardButton("Initiate", callback_data="initiate"),
            ],
            [    
                InlineKeyboardButton("Join", callback_data="join"),
            ],
            [
                InlineKeyboardButton("Edit sessions", callback_data="editable_sessions_edit"),
            ],    
            [    
                InlineKeyboardButton("View upcoming sessions", callback_data="editable_sessions_view"),
            ],    
            [   
                InlineKeyboardButton("Delete sessions", callback_data="deletable_sessions"),
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton("Initiate", callback_data="initiate"),
                InlineKeyboardButton("Join", callback_data="join")
            ]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        update.callback_query.message.reply_text(
            "Greetings! Would you like to join a study session or initiate one yourself?", reply_markup=reply_markup)
    except:
        update.message.reply_text(
            "Greetings! Would you like to join a study session or initiate one yourself?", reply_markup=reply_markup)

    return

###
# helper functions
###


def update_user(update, context):
    context.chat_data["state"] = "update_user"

    user_id = context.chat_data["user_id"]
    tele_handle = context.chat_data["tele_handle"]

    cursor = db.users.find_one({"user_id": user_id})

    if cursor == None:
        db.users.insert_one({"user_id": user_id, "tele_handle": tele_handle, "year": "",
                            "course": "", "gender": "", "location": "", "pax": "", "remarks": ""})
    else:
        filter_con = {"user_id": user_id}
        new_con = {"$set": {"tele_handle": tele_handle}}
        db.users.update_one(filter_con, new_con)

    return
