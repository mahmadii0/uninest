import random
import gettext

from shared import dbMig

_=None

groupLangs={}

def setLanguage(groupID:str,classID=False):
    lang=None
    if groupID not in groupLangs:
        if classID:
            lang = dbMig.getGroupLang(classID=int(classID))
            if lang == None:
                lang = 'en'
        else:
            lang = dbMig.getGroupLang(groupID=int(groupID))
            if lang == None:
                lang='en'
        groupLangs[groupID]=lang
    else:
        lang=groupLangs[groupID]
    translation = gettext.translation("messages", localedir="locales", languages=[lang])
    translation.install()
    return translation.gettext

def rand(randnums):
    num = random.randint(10 ** 7, 10 ** 8 - 1)
    if num in randnums:
        return rand(randnums)
    else:
        return num

def checkAdmin(bot,groupID,userID):
    member = bot.get_chat_member(groupID,userID)
    if member.status in ["administrator", "creator"]:
        return True
    else:
        return False

def deleteMessage(bot,call):
    if call.data =='getAllLectures' or call.data == 'getAllClasses':
        return
    if 'like' in call.data or 'dislike' in call.data:
        return
    bot.delete_message(call.message.chat.id, call.message.message_id)