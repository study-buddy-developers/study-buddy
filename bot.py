from sqlite3 import Date
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler
from telegram.ext import CallbackQueryHandler, Filters, ContextTypes
from datetime import datetime, timedelta
from credentials import *
import pymongo

API_KEY = "5371570532:AAEWry3st7_CFoQo7hJwwehMJvkD0NR-P9Q"


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello there, Welcome to the Bot.Please write /help to see the commands available.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """
    Available Commands:
	/youtube - To get the youtube URL
    /echo - Echo message
    /id - Display user id
    /begin - Start Study Buddy Telegram Bot
    """
    )


def youtube_url(update: Update, context: CallbackContext):
    update.message.reply_text("Youtube Link =>https://www.youtube.com/")


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


def test(update, context):
    update.message.reply_text("this is a test")

    # dp.remove_handler(MessageHandler(
    #     Filters.regex("@u.nus.edu"), test))

def transfer_message_to_db(update,info_type):
    info = str(update.message.text)
    db.users.insert_one({info_type:info})


def echo(update, context):
    update.message.reply_text(update.message.text)


def user_id(update, context):
    update.message.reply_text(update.message.from_user.id)


def begin(update, context):
    first_time(update)


def first_time(update):
    keyboard = [[
        InlineKeyboardButton("Yes", callback_data="first_time_yes"),
        InlineKeyboardButton("No", callback_data="first_time_no")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Hi! Welcome to Study Buddy Telegram Bot! Is this your first time using this bot?", reply_markup=reply_markup)
    return


def permission(update):
    keyboard = [[
        InlineKeyboardButton("Allow", callback_data="permission_allow")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Welcome to StudyBuddy Telegram Bot! Before we begin, we would like to ask for your permission to record your telegram handle. All information will be kept confidential in this telegram bot.", reply_markup=reply_markup)
    return


def email(update):
    update.callback_query.message.reply_text(
        "Hi! Welcome to StudyBuddy Bot! To verify your identity, What is your NUS email? (ending with @u.nus.edu)")

    # dp.add_handler(
    #     MessageHandler(Filters.regex("@u.nus.edu"), test))

    return


def verification(update):
    update.callback_query.message.reply_text(
        "A verification code has been sent to your email, please check and enter the code here to complete the verification.")

    return


def initiate_or_join(update):
    keyboard = [[
        InlineKeyboardButton("Initiate", callback_data="initiate"),
        InlineKeyboardButton("Join", callback_data="join")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Greetings! Would you like to join a study session or initiate one yourself?", reply_markup=reply_markup)
    return


def gender(update):
    keyboard = [[
        InlineKeyboardButton("Male", callback_data="male"),
        InlineKeyboardButton("Female", callback_data="female"),
        InlineKeyboardButton("Prefer not to say", callback_data="gender_null")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "What is your gender? (Note that you will not have a say in the gender of your study buddies if you choose ‘prefer not to say’)", reply_markup=reply_markup)
    return


def date(update):
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
            curr_day + "/" + curr_month + "/" + curr_year, callback_data=str(i)))

        col += 1
        col %= 3

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Please select your desired date for your study session", reply_markup=reply_markup)
    return


def time(update):
    keyboard = [[
        InlineKeyboardButton("Morning <1200", callback_data="morning"),
        InlineKeyboardButton("Afternoon 1200<=x<=1800",
                             callback_data="afternoon"),
        InlineKeyboardButton("Evening >1800", callback_data="evening")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "What time would you like to have your study session", reply_markup=reply_markup)
    return


def course(update):
    update.callback_query.message.reply_text(
        "What is your course?")
    return


def handle_callback_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    db.users.insert_one({"userid":update.callback_query.message.from_user.id})

    # first_time
    if query.data == "first_time_yes":
        permission(update)
    elif query.data == "first_time_no":
        initiate_or_join(update)

    # permission
    elif query.data == "permission_allow":
        email(update)


    # initiate_or_join
    elif query.data == "initiate":
        gender(update)
    elif query.data == "join":
        update.callback_query.message.reply_text("handle join")

    # gender
    elif query.data == "male" or query.data == "female":
        date(update)

    # date
    elif query.data == "1" or query.data == "2" or query.data == "3" or query.data == "4" or query.data == "5" or query.data == "6" or query.data == "7":
        time(update)

    # time
    elif query.data == "morning" or query.data == "afternoon" or query.data == "evening":
        course(update)


def main():
    updater = Updater(API_KEY, use_context=True)

    # get dispatcher from updater to register handlers
    dp = updater.dispatcher

    # adding start command handler to dispatcher.
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('youtube', youtube_url))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('echo', echo))
    dp.add_handler(CommandHandler('id', user_id))
    dp.add_handler(CommandHandler('begin', begin))

    dp.add_handler(CallbackQueryHandler(handle_callback_query))

    # Filters out unknown commands
    dp.add_handler(MessageHandler(Filters.command, unknown))
    # Filters out unknown messages.
    dp.add_handler(MessageHandler(Filters.text, unknown_text))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives
    # SIGINT, SIGTERM or SIGABRT. This should be used most of the
    # time, since,start_polling() is non-blocking and will stop
    # the bot
    updater.idle()


if __name__ == '__main__':
    main()
