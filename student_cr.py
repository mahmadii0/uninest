import telebot as tb
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
import app
from lecture import Group

def manageStudents(bot,groupID):
    markup=InlineKeyboardMarkup()
    add=InlineKeyboardButton(('Add Student'),callback_data=f'addStudent_{groupID}')
    get=InlineKeyboardButton(('Get Student'),callback_data=f'getStudent_{groupID}')
    getAll=InlineKeyboardButton(('Get All Students'),callback_data=f'getAllStudents_{groupID}')
    markup.add(add,get,getAll)
    bot.send_message(groupID,'Select a one of buttons to do that',reply_markup=markup)