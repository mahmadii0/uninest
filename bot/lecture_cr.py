import random

from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
import dbMig

waiting= {}
randnums=[]
def manageLectures(bot,groupID):
    markup=InlineKeyboardMarkup()
    add=InlineKeyboardButton(('Add Lecture'),callback_data=f'addLecture_{groupID}')
    get=InlineKeyboardButton(('Get Lecture'),callback_data=f'getLecture_{groupID}')
    getAll=InlineKeyboardButton(('Get All Lectures'),callback_data=f'getAllLectures_{groupID}')
    markup.add(add,get,getAll)
    bot.send_message(groupID,'Select a one of buttons to do that',reply_markup=markup)

def addLecture(bot,groupID):
    def rand():
        num = random.randint(10 ** 7, 10 ** 8 - 1)
        if num in randnums:
            return rand()
        else:
            return num
    _num=rand()
    status= dbMig.addRequest(_num, groupID)
    if status!=True:
        bot.send_message(groupID,'Error while adding request')
    bot.send_message(groupID,'Yeah! Now you can add your lecture from this url:'+'\n'+f'http://127.0.0.1:8000/add-lecture/{_num}')

