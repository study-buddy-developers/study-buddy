from tkinter import Button
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.filters import Filters


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


# def buttons(update, context):
#     """Sends a message with three inline buttons attached."""
#     keyboard = [
#         [
#             InlineKeyboardButton("Option 1", callback_data="1"),
#             InlineKeyboardButton("Option 2", callback_data="2"),
#         ],
#         [InlineKeyboardButton("Option 3", callback_data="3")],
#     ]

#     reply_markup = InlineKeyboardMarkup(keyboard)

#     async update.message.reply_text("Please choose:", reply_markup=reply_markup)


# def button(update, context):
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query

#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     await query.answer()

#     await query.edit_message_text(text=f"Selected option: {query.data}")


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

    # dp.add_handler(CommandHandler('buttons', buttons))
    # dp.add_handler(CallbackQueryHandler(button))

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
