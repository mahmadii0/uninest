import random

def rand(randnums):
    num = random.randint(10 ** 7, 10 ** 8 - 1)
    if num in randnums:
        return rand(randnums)
    else:
        return

def checkAdmin(bot,groupID,userID):
    member = bot.get_chat_member(groupID,userID)
    if member.status in ["administrator", "creator"]:
        return True
    else:
        return False

def deleteMessage(bot,call):
    if call.data =='getAllLectures' or call.data == 'getAllClasses':
        return
    bot.delete_message(call.message.chat.id, call.message.message_id)