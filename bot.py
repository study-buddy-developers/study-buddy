from telegram import ForceReply, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, MessageHandler
from telegram.ext import CallbackQueryHandler, Filters, ContextTypes
from datetime import datetime, timedelta

API_KEY = "5371570532:AAEWry3st7_CFoQo7hJwwehMJvkD0NR-P9Q"

EXPECT_TEXT = range(1)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello there, Welcome to the Bot. Please write /help to see the commands available.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """
    Available Commands:
    /id - Display user id
    /begin - Start Study Buddy Telegram Bot
    """
    )


def unknown_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'. Please use /begin to start again." % update.message.text)


def user_id(update, context):
    update.message.reply_text(update.message.from_user.id)


def begin(update, context):
    first_time(update, context)


def first_time(update, context):
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
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi! Welcome to StudyBuddy Bot! To verify your identity, what is your NUS email? (ending with @u.nus.edu)")

    return


def verification(update, context):
    email = update.message.text
    update.message.reply_text(
        "A verification code has been sent to " + str(email) + " Please check and enter the code here to complete the verification.")

    return


def code(update, context):
    code = update.effective_message.text

    # TODO: get verification code here
    verification_code = "123"

    if code == verification_code:
        update.message.reply_text(
            "Thank you! Your email has been verified!")
        initiate_or_join(update, context)

    else:
        keyboard = [
            [
                InlineKeyboardButton("Resend", callback_data="resend")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            "Sorry, the verification code you have entered is incorrect, please click the resend button for a new code."
            " If you have entered your email incorrectly, please send your email (ending with @u.nus.edu) again.", reply_markup=reply_markup)

    return


def new_code(update, context):
    update.callback_query.message.reply_text(
        "A new code has been sent to your email. Please check and enter the code here to complete the verification.")

    return


def initiate_or_join(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Initiate", callback_data="initiate"),
            InlineKeyboardButton("Join", callback_data="join")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if context.chat_data["state"] == "code":
        update.message.reply_text(
            "Greetings! Would you like to join a study session or initiate one yourself?", reply_markup=reply_markup)
    elif context.chat_data["state"] == "first_time_no":
        update.callback_query.message.reply_text(
            "Greetings! Would you like to join a study session or initiate one yourself?", reply_markup=reply_markup)
    else:
        update.callback_query.message.reply_text(
            "Greetings! Would you like to join a study session or initiate one yourself?", reply_markup=reply_markup)

    return


def gender(update, context):
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


def date(update, context):
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


def time(update, context):
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
    update.callback_query.message.reply_text("What is your course?")

    return


def year(update, context):
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

    update.message.reply_text(
        "What year are you in?", reply_markup=reply_markup)

    return


def location(update, context):
    update.callback_query.message.reply_text("Where would you like to study?")

    return


def pax(update, context):
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


def remark_yes(update, context):
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

    if context.chat_data["state"] == "remark_done":
        update.message.reply_text(
            "Would you like your data to be stored?", reply_markup=reply_markup)
    elif context.chat_data["state"] == "remark_no":
        update.callback_query.message.reply_text(
            "Would you like your data to be stored?", reply_markup=reply_markup)
    else:
        update.callback_query.message.reply_text(
            "Would you like your data to be stored?", reply_markup=reply_markup)

    return


def which_data(update, context):
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
    update.callback_query.message.reply_text(
        "Your study session has been posted successfully! We will update you when someone joined your session")

    return ConversationHandler.END


def handle_callback_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    print(query.data)

    context.chat_data["state"] = query.data

    # first_time
    if query.data == "first_time_yes":
        permission(update, context)
    elif query.data == "first_time_no":
        initiate_or_join(update, context)

    # permission
    elif query.data == "permission_allow":
        email(update, context)

    # resend verification code
    elif query.data == "resend":
        new_code(update, context)

    # initiate_or_join
    elif query.data == "initiate":
        gender(update, context)
    elif query.data == "join":
        update.callback_query.message.reply_text("handle join")

    # gender
    elif query.data == "male" or query.data == "female":
        date(update, context)

    # date
    elif query.data == "date_1" or query.data == "date_2" or query.data == "date_3" or query.data == "date_4" or query.data == "date_5" or query.data == "date_6" or query.data == "date_7":
        time(update, context)

    # time
    elif query.data == "morning" or query.data == "afternoon" or query.data == "evening":
        course(update, context)

    # year
    elif query.data == "year_one" or query.data == "year_two" or query.data == "year_three" or query.data == "year_four" or query.data == "year_five":
        location(update, context)

    # pax
    elif query.data == "pax_two" or query.data == "pax_three" or query.data == "pax_four" or query.data == "pax_five":
        remark(update, context)

    # remark_yes or remark_no
    elif query.data == "remark_yes":
        remark_yes(update, context)
    elif query.data == "remark_no":
        store_data(update, context)

    # store data
    elif query.data == "store_data_yes":
        which_data(update, context)
    elif query.data == "store_data_no":
        end(update, context)

    # which data
    elif query.data == "gender" or query.data == "course" or query.data == "location" or query.data == "pax":
        # TODO: store data
        print("handle store data")
    elif query.data == "done":
        end(update, context)

    return


def handle_text(update, context):
    text = update.effective_message.text

    print(text)

    if "state" in context.chat_data.keys():
        print("state: " + context.chat_data["state"])
        state = context.chat_data["state"]
    else:
        state = ""

    # email
    if state == "permission_allow" and text.endswith("@u.nus.edu"):
        context.chat_data["state"] = "verification"
        verification(update, context)

    # verification
    # TODO: isNumeric()
    elif state == "verification" or state == "resend":
        context.chat_data["state"] = "code"
        code(update, context)

    # redo verification
    elif state == "code" and text.endswith("@u.nus.edu"):
        context.chat_data["state"] = "verification"
        verification(update, context)

    # course
    elif state == "morning" or state == "afternoon" or state == "evening":
        context.chat_data["state"] = "course"
        year(update, context)

    # year
    elif state == "course":
        context.chat_data["state"] = "year"
        year(update, context)

    # pax
    elif state == "year_one" or state == "year_two" or state == "year_three" or state == "year_four" or state == "year_five":
        context.chat_data["state"] = "pax"
        pax(update, context)

    # remarks
    elif state == "remark_yes":
        context.chat_data["state"] = "remark_done"
        store_data(update, context)

    # unknown text
    else:
        context.chat_data["state"] = ""
        unknown_text(update, context)

    return


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Conversation cancelled by user. Send /begin to start again.")

    return ConversationHandler.END


def main():
    updater = Updater(API_KEY, use_context=True)

    # get dispatcher from updater to register handlers
    dp = updater.dispatcher

    # adding start command handler to dispatcher.
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("id", user_id))
    dp.add_handler(CommandHandler("begin", begin))
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
