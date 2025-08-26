import telebot as tb
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
import app
from lecture import Group

def manageLectures(bot,groupID):
    markup=InlineKeyboardMarkup()
    add=InlineKeyboardButton(('Add Lecture'),callback_data=f'addLecture_{groupID}')
    get=InlineKeyboardButton(('Get Lecture'),callback_data=f'getLecture_{groupID}')
    getAll=InlineKeyboardButton(('Get All Lectures'),callback_data=f'getAllLectures_{groupID}')
    markup.add(add,get,getAll)
    bot.send_message(groupID,'Select a one of buttons to do that',reply_markup=markup)

def addLecture(bot,groupID):
    pass
