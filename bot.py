from telegram.ext.updater import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler, ConversationHandler

from credentials import API_KEY
from handler import *
from admin import *


EXPECT_TEXT = range(1)


def main():
    api_key = API_KEY
    updater = Updater(api_key, use_context=True)

    # get dispatcher from updater to register handlers
    dp = updater.dispatcher

    # adding start command handler to dispatcher.
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("cancel", cancel))

    dp.add_handler(CallbackQueryHandler(handle_callback_query))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, handle_text)],
        states={
            EXPECT_TEXT: [MessageHandler(Filters.text, handle_text)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    dp.add_handler(conv_handler)

    # Filters out unknown commands
    dp.add_handler(MessageHandler(Filters.command, unknown_command))
    # Filters out unknown messages.
    dp.add_handler(MessageHandler(Filters.text, unknown_text))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives
    # SIGINT, SIGTERM or SIGABRT. This should be used most of the
    # time, since,start_polling() is non-blocking and will stop
    # the bot
    updater.idle()

    return 0


if __name__ == '__main__':
    main()
