from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from admin import *
from first_time import *
from initiate import *
from join import *


def handle_callback_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    print(query.data)

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
        join_date(update, context)

    # gender
    elif query.data == "male" or query.data == "female":
        initiate_date(update, context)

    # initiate date
    elif query.data == "date_1" or query.data == "date_2" or query.data == "date_3" or query.data == "date_4" or query.data == "date_5" or query.data == "date_6" or query.data == "date_7":
        initiate_time(update, context)

    # initiate time
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
        add_remark(update, context)
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

    # join date
    elif query.data[:9] == "join_date":
        join_time(update, context)

    # join time
    elif query.data == "join_morning":
        available(update, context, 'Morning')
    elif query.data == "join_afternoon":
        available(update, context, 'Afternoon')
    elif query.data == "join_evening":
        available(update, context, 'Evening')

    # join session
    elif query.data == "contact":
        prompt_contact(update, context)

    return


def handle_text(update, context):
    text = update.effective_message.text

    print(text)

    # if "state" in context.chat_data.keys():
    #     print("state: " + context.chat_data["state"])
    state = context.chat_data["state"]
    # else:
    #     state = ""

    # email
    if (state == "email" or state == "wrong_code"):
        verification(update, context)

    # verification code
    elif (state == "verification" or state == "new_code"):
        code(update, context)

    # course
    elif (state == "course") and text.isalpha():
        year(update, context)

    # location
    elif state == "location":
        pax(update, context)

    # remark
    elif state == "add_remark":
        store_data(update, context)

    # unknown text
    else:
        unknown_text(update, context)

    return

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Conversation cancelled by user. Send /begin to start again.")

    return ConversationHandler.END
