from tkinter import Button
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler
from telegram.ext import CallbackQueryHandler, Filters, ContextTypes

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


def echo(update, context):
    update.message.reply_text(update.message.text)


def user_id(update, context):
    update.message.reply_text(update.message.from_user.id)


def button(update: Update, context: CallbackContext) -> None:
    keyboard = [[
        InlineKeyboardButton("1", callback_data='1'),
        InlineKeyboardButton("2", callback_data='2'),
        InlineKeyboardButton("3",callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose a number:", reply_markup=reply_markup)

def buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == '1':
        update.callback_query.message.edit_text("You win!")
    elif query.data == '2':
        update.callback_query.message.edit_text("Boo, wrong number")
    elif query.data == '3':
        update.callback_query.message.edit_text("Oops, you chose wrong")


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
    dp.add_handler(CommandHandler('butt', button))
    dp.add_handler(CallbackQueryHandler(buttons))

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
