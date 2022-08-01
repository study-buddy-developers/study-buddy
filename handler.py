from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from datetime import datetime, timedelta
from bson.objectid import ObjectId


from admin import *
from first_time import *
from initiate import *
from join import *
from credentials import *


def handle_callback_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    print(query.data)

    # first_time
    if query.data == "acknowledge":
        email(update, context)

    # resend verification code
    elif query.data == "resend":
        new_code(update, context)

    # initiate_or_join
    elif query.data == "initiate":
        initiate_date(update, context)
    elif query.data == "join":
        for i in range(7):
            curr_date = datetime.now() + timedelta(days=i)
            curr_day = str(curr_date.day)
            curr_month = str(curr_date.month)
            curr_year = str(curr_date.year)

            date = curr_day + "/" + curr_month + "/" + curr_year

            if valid_date(update, context, date):
                join_date(update, context)
                return

        no_sessions(update, context)

    # initiate date
    elif query.data == "date_1" or query.data == "date_2" or query.data == "date_3" or query.data == "date_4" or query.data == "date_5" or query.data == "date_6" or query.data == "date_7":
        i = int(query.data[-1]) - 1

        curr_date = datetime.now() + timedelta(days=i)
        curr_day = str(curr_date.day)
        curr_month = str(curr_date.month)
        curr_year = str(curr_date.year)
        date = curr_day + "/" + curr_month + "/" + curr_year

        context.chat_data["initiate_date"] = date

        initiate_time(update, context)

    # update_data_done
    elif query.data == "update_done":
        if context.chat_data["state"] == "update_data":
            end(update, context)
        else:
            next_data(update, context)

    # update_data
    elif query.data[:7] == "update_":
        data = query.data[7:]
        context.chat_data["stored_data"].remove(data)

        edit_update_data(update, context)

    # year
    elif query.data[:5] == "year_":
        context.chat_data["year"] = query.data

        next_data(update, context)

    # course
    elif query.data[0:3] == "CDE":
        context.chat_data["course"] = query.data

        next_data(update, context)

    # gender
    elif query.data == "male" or query.data == "female" or query.data == "gender_null":
        context.chat_data["gender"] = query.data

        next_data(update, context)

    # pax
    elif query.data == "pax_2" or query.data == "pax_3" or query.data == "pax_4" or query.data == "pax_5":
        context.chat_data["pax"] = query.data

        next_data(update, context)

    # remark_yes or remark_no
    elif query.data == "remark_yes":
        context.chat_data["remarks"] = ""

        add_remark(update, context)
    elif query.data == "remark_no":
        context.chat_data["remarks"] = ""

        store_data(update, context)

    # store data
    elif query.data == "store_data_yes":
        which_data(update, context)
    elif query.data == "store_data_no":
        end(update, context)

    # which data
    elif query.data == "gender" or query.data == "course" or query.data == "year" or query.data == "location" or query.data == "pax" or query.data == "remarks":
        # handle store data
        filter_con = {"user_id": context.chat_data["user_id"]}
        new_con = {"$set": {query.data: context.chat_data[query.data]}}
        db.users.update_one(filter_con, new_con)

        context.chat_data["stored_data"].remove(query.data)

        edit_which_data(update, context)

    elif query.data == "store_done":
        end(update, context)

    # join date
    elif query.data[:9] == "join_date":
        i = int(query.data[-1])

        curr_date = datetime.now() + timedelta(days=i)
        curr_day = str(curr_date.day)
        curr_month = str(curr_date.month)
        curr_year = str(curr_date.year)
        date = curr_day + "/" + curr_month + "/" + curr_year

        context.chat_data["join_date"] = date

        join_sessions(update, context)

    # join session
    elif query.data[:13] == "join_session_":
        session_id = query.data[13:]

        cursor = db.sessions.find_one(
            {"_id": ObjectId(session_id)}
        )

        userid = cursor["user_id_array"][0]
        joiner_id = context.chat_data["user_id"]

        if joiner_id not in cursor["user_id_array"]:
            filtercon = {"_id": ObjectId(session_id)}
            newcon = {"$push": {"user_id_array": joiner_id}}
            db.sessions.update_one(filtercon, newcon)

        context.chat_data["initiator_telegram_handle"] = db.users.find_one(
            {"user_id": userid})["tele_handle"]

        context.bot.send_message(chat_id=userid, text="Hi! @" +
                                 context.chat_data["tele_handle"] + " has joined your study session!")
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

    # initiate time
    elif state == "time":
        if len(text) > 4:
            invalid_initiate_time(
                update, context, "Text more than 4 digits")
        elif len(text) < 4:
            invalid_initiate_time(
                update, context, "Text less than 4 digits")
        elif [text[i].isdigit() for i in range(4)] != [True, True, True, True]:
            invalid_initiate_time(
                update, context, "Text contains non-digits")
        elif not valid_time(update, context, text):
            invalid_initiate_time(
                update, context, "Inititate time before current time")
        else:
            context.chat_data["initiate_time"] = text

            if len(check_data(update, context)) == 0:
                next_data(update, context)
            else:
                update_data(update, context)

    # location
    elif state == "location":
        context.chat_data["location"] = text

        # store telehandle in user db
        filtercon = {"user_id": context.chat_data["user_id"]}
        newcon = {"$set": {"tele_handle": context.chat_data["tele_handle"]}}
        db.users.update_one(filtercon, newcon)

        next_data(update, context)

    # remark
    elif state == "add_remark":
        context.chat_data["remarks"] = text

        store_data(update, context)

    # unknown text
    else:
        unknown_text(update, context)

    return


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Conversation cancelled by user. Send /start to start again.")

    return ConversationHandler.END
