from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from email_verification import email_verification


def first_time(update, context):
    context.chat_data["state"] = "first_time"

    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="first_time_yes"),
            InlineKeyboardButton("No", callback_data="first_time_no")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Hi! Welcome to Study Buddy Telegram Bot! Is this your first time using this bot?", reply_markup=reply_markup)

    return


def permission(update, context):
    context.chat_data["state"] = "permission"

    keyboard = [
        [
            InlineKeyboardButton("Allow", callback_data="permission_allow")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Welcome to StudyBuddy Telegram Bot! Before we begin, we would like to ask for your permission to record your telegram handle. All information will be kept confidential in this telegram bot.", reply_markup=reply_markup)

    return


def email(update, context):
    context.chat_data["state"] = "email"

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi! Welcome to StudyBuddy Bot! To verify your identity, what is your NUS email? (ending with @u.nus.edu)")

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
    keyboard = [
        [
            InlineKeyboardButton("Initiate", callback_data="initiate"),
            InlineKeyboardButton("Join", callback_data="join")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if context.chat_data["state"] == "first_time":
        update.callback_query.message.reply_text(
            "Greetings! Would you like to join a study session or initiate one yourself?", reply_markup=reply_markup)
    elif context.chat_data["state"] == "code":
        update.message.reply_text(
            "Greetings! Would you like to join a study session or initiate one yourself?", reply_markup=reply_markup)
    # catch error when user clicks "first_time_no" after clicking "first_time_yes"
    else:
        print("SOMETHING WENT WRONG HERE")

        try:
            update.callback_query.message.reply_text(
                "Greetings! Would you like to join a study session or initiate one yourself?", reply_markup=reply_markup)
        except:
            update.message.reply_text(
                "Greetings! Would you like to join a study session or initiate one yourself?", reply_markup=reply_markup)

    context.chat_data["state"] = "initiate_or_join"

    return
