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

    # TODO insert terms of service here
    update.message.reply_text(
        "Welcome to StudyBuddy Telegram Bot! Before we begin, we would like to ask for your permission to record your telegram handle. All information will be kept confidential in this telegram bot.", reply_markup=reply_markup
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


def update_user(update, context):
    context.chat_data["state"] = "update_user"

    user_id = context.chat_data["user_id"]
    tele_handle = context.chat_data["tele_handle"]

    cursor = db.users.find_one({"user_id": user_id})

    if cursor == None:
        db.users.insert_one({"user_id": user_id, "tele_handle": tele_handle})
    else:
        cursor["tele_handle"] = tele_handle

    return
