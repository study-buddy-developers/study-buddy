from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import pymongo

from admin import *
from first_time import *
from initiate import *
from join import *
from credentials import *

from datetime import datetime, timedelta

from bson.objectid import ObjectId


def handle_callback_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    print(query.data)

    # first_time
    if query.data == "first_time_yes":
        cursor = db.users.find(
            {"user_id": context.chat_data["id"]})
        if list(cursor) == []:
            db.users.insert_one(
                {"user_id": context.chat_data["id"]})
        permission(update, context)

    elif query.data == "first_time_no":
        cursor = db.users.find(
            {"user_id": context.chat_data["id"]})
        if list(cursor) == []:
            db.users.insert_one(
                {"user_id": context.chat_data["id"]})
        initiate_or_join(update, context)

    # permission
    elif query.data == "permission_allow":
        email(update, context)

    # resend verification code
    elif query.data == "resend":
        new_code(update, context)

    # initiate_or_join
    elif query.data == "initiate":
        # where user_id is the user ID of the initiator
        db.StudySessions.insert_one(
            {"user_id": context.chat_data["id"]})
        gender(update, context)
    elif query.data == "join":
        join_date(update, context)

    # gender
    elif query.data == "male" or query.data == "female":
        context.chat_data["gender"] = query.data

        initiate_date(update, context)

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

    # initiate time
    elif query.data == "morning" or query.data == "afternoon" or query.data == "evening":
        context.chat_data["initiate_time"] = query.data

        course(update, context)

    # course
    elif query.data[0:3] == "CDE":
        context.chat_data["course"] = query.data

        year(update,context)

    # year
    elif query.data == "year_one" or query.data == "year_two" or query.data == "year_three" or query.data == "year_four" or query.data == "year_five":
        context.chat_data["year"] = query.data

        location(update, context)

    # pax
    elif query.data == "pax_two" or query.data == "pax_three" or query.data == "pax_four" or query.data == "pax_five":
        context.chat_data["pax"] = query.data

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
        create_study_session(update, context)

        purge_data(update, context)

        end(update, context)

    # which data
    elif query.data == "gender" or query.data == "course" or query.data == "year" or query.data == "location" or query.data == "pax":
        # handle store data
        filter_con = {"user_id": context.chat_data["id"]}
        new_con = {"$set": {query.data: context.chat_data[query.data]}}
        db.users.update_one(filter_con, new_con)

    elif query.data == "done":
        create_study_session(update, context)

        purge_data(update, context)

        end(update, context)

    # join date
    elif query.data[:9] == "join_date":
        i = int(query.data[-1]) - 1

        curr_date = datetime.now() + timedelta(days=i)
        curr_day = str(curr_date.day)
        curr_month = str(curr_date.month)
        curr_year = str(curr_date.year)
        date = curr_day + "/" + curr_month + "/" + curr_year

        context.chat_data["join_date"] = date

        join_time(update, context)

    # join time
    elif query.data[:5] == "join_":
        context.chat_data["join_time"] = query.data[5:]

        sessions = available_sessions(update, context)

        join_sessions(update, context, sessions)

    # join session
    elif query.data[0:8] == "contact_":
        session_id = query.data[8:]
        cursor = db.sessions.find_one(
            {"_id" : ObjectId(session_id)}
        )
        userid = cursor["user_id_array"][0]
        joiner_id = context.chat_data["id"]
        print(joiner_id)
        if joiner_id not in cursor["user_id_array"]:
            filtercon = {"_id":ObjectId(session_id)}
            newcon = {"$push":{"user_id_array":joiner_id}}
            db.sessions.update_one(filtercon,newcon)
        contact = db.users.find_one({"user_id":userid})["tele_handle"]

        prompt_contact(update, context, contact)

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

    # course DEPRECATED
    elif (state == "course") and text.isalpha():
        context.chat_data["course"] = text

        year(update, context)

    # location
    elif state == "location":
        context.chat_data["location"] = text

        # store telehandle in user db
        filtercon = {"user_id":context.chat_data["id"]}
        newcon = {"$set":{"tele_handle":context.chat_data["tele_handle"]}}
        db.users.update_one(filtercon,newcon)

        pax(update, context)

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
        "Conversation cancelled by user. Send /begin to start again.")

    return ConversationHandler.END
