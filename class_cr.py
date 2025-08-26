import telebot as tb
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
import app
from lecture import Group

def manageClasses(bot,groupID):
    markup=InlineKeyboardMarkup()
    add=InlineKeyboardButton(('Add Class'),callback_data=f'addClass_{groupID}')
    get=InlineKeyboardButton(('Get Class'),callback_data=f'getClass_{groupID}')
    getAll=InlineKeyboardButton(('Get All Classes'),callback_data=f'getAllClasses_{groupID}')
    markup.add(add,get,getAll)
    bot.send_message(groupID,'Select a one of buttons to do that',reply_markup=markup)

