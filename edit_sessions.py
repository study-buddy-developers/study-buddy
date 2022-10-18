from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from pymongo import *
from credentials import *
from bson.objectid import ObjectId


def display_sessions(update,context,edit_or_view_or_delete): #view or edit or delete
    context.chat_data["state"] = "display_editable_sessions"
    cursor = db.users.find_one({"user_id": context.chat_data["user_id"]})
    sessions_list = []
    updated_list = []
    for sess in cursor["sessions_initiated"]: 
        found_session = db.sessions.find_one({"_id":sess})
        if found_session:
            updated_list.append(sess)
            session_details = found_session["time"] + " , " + found_session["date"] + " @ " + found_session["location"]

            if edit_or_view_or_delete == "edit":
                sessions_list.append(InlineKeyboardButton(session_details, callback_data="edit_session" + str(sess)))
            elif edit_or_view_or_delete == "view":
                sessions_list.append(InlineKeyboardButton(session_details, callback_data="Iamnotsupposedtodoanything"))
            elif edit_or_view_or_delete == "delete":
                sessions_list.append(InlineKeyboardButton(session_details, callback_data="delete_session" + str(sess)))
    
    # update sessions list in user collection if there exists outdated sessions
    filter_con = {"user_id": context.chat_data["user_id"]}
    new_con = {"$set": {"sessions_initiated": updated_list}}
    db.users.update_one(filter_con, new_con)

    if sessions_list == []:
        initiate_button = InlineKeyboardButton("Initiate a study session :)", callback_data= "initiate")
        keyboard = [
        initiate_button
        ]  
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("You have not initiated any study sessions :( ", reply_markup = reply_markup)
    else:
        keyboard = [
        sessions_list
        ]    
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text(#update.callback_query.data[0:4] == edit/delete
            "Please select the session that you wish to " + edit_or_view_or_delete,reply_markup=reply_markup)
    return

def display_session_details(update,context, sessid_str):
        context.chat_data["state"] = "display_editable_session_details"
        sess_id =ObjectId(sessid_str)
        cursor = db.sessions.find_one({"_id":sess_id})
        session_details_list = []
        for key in cursor: 
            if key == "year":
                button = key + " : " + cursor.get(key)[0:4] + " "+ cursor.get(key)[5:]
            elif key == "pax":
                button = key + " : " + cursor.get(key)[0:3] + " "+ cursor.get(key)[-1]        
            elif key =="course":
                button = key + " : " + cursor.get(key)[4:] 
            elif key == "user_id_array" or key == "_id":
                continue
            else:
                button = key + " : " + cursor.get(key)
            session_details_list.append([InlineKeyboardButton(button,callback_data ="edit_"+ key + "_of_session")] )
        reply_markup = InlineKeyboardMarkup(session_details_list)
        update.callback_query.message.reply_text(
            "this part is still under construction" ,reply_markup=reply_markup) #"Please select the details of your session that you wish to edit"
        return