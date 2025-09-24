import telebot as tb
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
from shared import dbMig
from shared.models import Group
from utils import setLanguage
_=None
groupIDs=[]

def storeGroupIDs():
    global groupIDs
    list= dbMig.getGroupIDs()
    if list != None or list!=[]:
        for item in list:
            groupIDs.append(item[0])


def langChoosing(bot:tb,message):
    markup=InlineKeyboardMarkup()
    persian=InlineKeyboardButton("فارسی",callback_data='persian')
    english=InlineKeyboardButton("English",callback_data='english')
    markup.add(persian,english)
    bot.send_message(message.chat.id,"🔹Please Select Your Language First:",reply_markup=markup)

def configureGroup(bot:tb,lang,call):
    group=Group(
    groupID=int(call.message.chat.id),
    name=call.message.chat.title,
    lang=lang
    )
    status= dbMig.addGroup(group)
    if status:
        _=setLanguage(str(call.message.chat.id))
        markup = InlineKeyboardMarkup()
        classes = InlineKeyboardButton(_('Manage Classes'), callback_data='manage_classes')
        lectures = InlineKeyboardButton(_('Manage Lectures'), callback_data='manage_lectures')
        markup.add(classes, lectures)
        bot.send_message(group.groupID,_("🤖Your Group successfully registered!"), reply_markup=markup)





