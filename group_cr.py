import telebot
import telebot as tb
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
import app
from lecture import Group

_=None
groupIDs=[]

def storeGroupIDs():
    global groupIDs
    list=app.getGroupIDs()
    if list != None or list!=[]:
        for item in list:
            groupIDs.append(item[0])


def langChoosing(bot:tb,message):
    markup=InlineKeyboardMarkup()
    persian=InlineKeyboardButton(("فارسی"),callback_data='persian')
    english=InlineKeyboardButton(("English"),callback_data='english')
    markup.add(persian,english)
    bot.send_message(message.chat.id,"Please Select Your Language First:",reply_markup=markup)

def configureGroup(bot:tb,lang,call):
    group=Group(
    groupID=int(call.message.chat.id),
    name=call.message.chat.title,
    lang=lang
    )
    status=app.addGroup(group)
    if status:
        bot.send_message(group.groupID,"Your Group successfully registered!")





