from telegram import ForceReply, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, MessageHandler
from telegram.ext import CallbackQueryHandler, Filters, ContextTypes
from datetime import datetime, timedelta

API_KEY = "5371570532:AAEWry3st7_CFoQo7hJwwehMJvkD0NR-P9Q"

verification_code = "123"

EXPECT_TEXT = range(1)


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


def unknown_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'. Please use /begin to start again." % update.message.text)


def echo(update, context):
    update.message.reply_text(update.message.text)


def user_id(update, context):
    update.message.reply_text(update.message.from_user.id)


def begin(update, context):
    first_time(update, context)


def first_time(update, context):
    keyboard = [[
        InlineKeyboardButton("Yes", callback_data="first_time_yes"),
        InlineKeyboardButton("No", callback_data="first_time_no")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Hi! Welcome to Study Buddy Telegram Bot! Is this your first time using this bot?", reply_markup=reply_markup)
    return


def permission(update, context):
    keyboard = [[
        InlineKeyboardButton("Allow", callback_data="permission_allow")]]
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
        "A verification code has been sent to " + str(email) + " please check and enter the code here to complete the verification.")

    return


def code(update, context):
    code = update.effective_message.text
    if code == '123':
        keyboard = [[
            InlineKeyboardButton("Initiate", callback_data="initiate"),
            InlineKeyboardButton("Join", callback_data="join")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            "Thank you! Your email has been verified. Would you like to join a study session or initiate one yourself?", reply_markup=reply_markup)

        return
    else:
        keyboard = [[
            InlineKeyboardButton("Resend", callback_data="resend")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            "Sorry, the verification code you have entered is incorrect, please click the resend button for a new code."
            " If you have entered your email incorrectly, please send your email (ending with @u.nus.edu) again.", reply_markup=reply_markup)
        return


def new_code(update, context):
    update.callback_query.message.reply_text(
        "A new code has been sent to your email. Please check and enter the code here to complete the verification.")
    return EXPECT_CODE


def initiate_or_join(update, context):
    keyboard = [[
        InlineKeyboardButton("Initiate", callback_data="initiate"),
        InlineKeyboardButton("Join", callback_data="join")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Greetings! Would you like to join a study session or initiate one yourself?", reply_markup=reply_markup)
    return


def gender(update, context):
    keyboard = [[
        InlineKeyboardButton("Male", callback_data="male"),
        InlineKeyboardButton("Female", callback_data="female"),
        InlineKeyboardButton("Prefer not to say", callback_data="gender_null")
    ]]
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
            curr_day + "/" + curr_month + "/" + curr_year, callback_data=str(i)))

        col += 1
        col %= 3

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Please select your desired date for your study session", reply_markup=reply_markup)
    return


def time(update, context):
    keyboard = [[
        InlineKeyboardButton("Morning <1200", callback_data="morning")],
        [InlineKeyboardButton("Afternoon 1200<=x<=1800",
                              callback_data="afternoon")],
        [InlineKeyboardButton("Evening >1800", callback_data="evening")
         ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "What time would you like to have your study session", reply_markup=reply_markup)
    return


def course(update, context):
    update.callback_query.message.reply_text(
        "What is your course?")
    return


def year(update, context):
    course = update.effective_message.text

    print(course)

    update.message.reply_text("What year are you in?")
    return EXPECT_YEAR


def location(update, context):
    year = update.effective_message.text

    print(year)

    update.message.reply_text("Where would you like to study?")
    return EXPECT_LOCATION


def people(update, context):
    location = update.effective_message.text

    print(location)

    keyboard = [[
        InlineKeyboardButton("2", callback_data="two")],
        [InlineKeyboardButton("3", callback_data="three")],
        [InlineKeyboardButton("4", callback_data="four")],
        [InlineKeyboardButton("5", callback_data="five")
         ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "How many people would you like in your study session?", reply_markup=reply_markup)
    return


def remark(update, context):
    keyboard = [[
        InlineKeyboardButton("Yes", callback_data="remark_yes")],
        [InlineKeyboardButton("No (1st time user)",
                              callback_data="remark_no_first")],
        [InlineKeyboardButton("No", callback_data="remark_no")
         ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Any additional remarks?", reply_markup=reply_markup)
    return


def remark_yes(update, context):
    update.callback_query.message.reply_text(
        "What remark would you like to add?")
    return EXPECT_REMARK


def store_data(update, context):
    keyboard = [[
        InlineKeyboardButton("Yes", callback_data="store_data_yes"),
        InlineKeyboardButton("No", callback_data="store_data_no")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Would you like your data to be stored?", reply_markup=reply_markup)
    return


def which_data(update, context):  # btw i think we should have a 'store all' option
    keyboard = [[
        InlineKeyboardButton("Gender", callback_data="gender"),
        InlineKeyboardButton("Course", callback_data="course"),
        InlineKeyboardButton("Year", callback_data="year")],
        [InlineKeyboardButton("Location", callback_data="location"),
         InlineKeyboardButton("Pax", callback_data="pax"),
         InlineKeyboardButton("Done", callback_data="done")
         ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(
        "Which data would you like to store?", reply_markup=reply_markup)
    return


def end(update, context):
    update.callback_query.message.reply_text(
        "Your study session has been posted successfully! We will update you when someone joined your session")

    return


def handle_callback_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    print(query.data)

    state = query.data
    print("state: ")
    print(state)

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
    elif query.data == "1" or query.data == "2" or query.data == "3" or query.data == "4" or query.data == "5" or query.data == "6" or query.data == "7":
        time(update, context)

    # time
    elif query.data == "morning" or query.data == "afternoon" or query.data == "evening":
        course(update, context)

    # number of people
    elif query.data == "two" or query.data == "three" or query.data == "four" or query.data == "five":
        remark(update, context)

    # remark
    elif query.data == "remark_yes":
        remark_yes(update, context)
    elif query.data == "remark_no_first":
        update.callback_query.message.reply_text("idk what to do")
    elif query.data == "remark_no":
        store_data(update, context)

    # store data
    elif query.data == "store_data_yes":
        which_data(update, context)
    elif query.data == "store_data_no":
        end(update, context)

    return


def handle_text(update, context):
    text = update.effective_message.text

    print(text)

    # email
    if text.endswith("u.nus.edu"):
        ConversationHandler.END
        verification(update, context)

    # verification
    elif text == verification_code:
        ConversationHandler.END
        code(update, context)

    # unknown text
    else:
        unknown_text(update, context)

    return


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Conversation cancelled by user. Bye. Send /begin to start again")
    return ConversationHandler.END


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
    dp.add_handler(CommandHandler('cancel', cancel))

    dp.add_handler(CallbackQueryHandler(handle_callback_query))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, handle_text)],
        states={
            EXPECT_TEXT: [MessageHandler(Filters.text, handle_text)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
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


if __name__ == '__main__':
    main()
