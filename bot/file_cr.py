import time

from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
from shared import constants
from shared.models import File
from utils import rand
from shared import dbMig

def getFile(bot,fileName,classID,bool=False):
    if bool:
        file=dbMig.getFile(fileName,classID)
        if type(file)==tuple:
            return True
        else:
            return False
    else:
        groupID=classID
        address=fileName
        markup=InlineKeyboardMarkup()
        delete=InlineKeyboardButton('delete',callback_data=f'deleteFile_{address}_{groupID}')
        markup.add(delete)
        bot.forward_message(groupID,from_chat_id=constants.channelID,message_id=address)
        bot.send_message(groupID, 'for deleting this file,Click the button below:', reply_markup=markup)

def getAllFiles(bot,classID,groupID):
    list=dbMig.getAllFiles(classID)
    if list==None:
        bot.send_message("Your request for getting all files, failed")
    markup=InlineKeyboardMarkup()
    for item in list:
        btn=InlineKeyboardButton(item[0],callback_data=f'getFile_{item[1]}_{groupID}')
        markup.add(btn)
    bot.send_message(groupID,'For access to a specify file, click on its button:',reply_markup=markup)


def addFile(bot,fileName,fileAddress,classID,groupID):
    file=File(
        fileName=fileName,
        address=fileAddress,
        classID=classID
    )
    status=dbMig.addFile(file)
    if status:
        bot.send_message(groupID,'The file successfully added to class files')

def deleteFile(bot,address,groupID):
    status = dbMig.deleteFile(address)
    if status:
        status = dbMig.delRequest(address)
        if status:
            bot.send_message(groupID, "The file successfully deleted")