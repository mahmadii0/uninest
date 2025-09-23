from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
from shared import dbMig
from datetime import datetime, timedelta
from webApp.utils.utils import publishEvent

def addExam(bot,classID,groupID):
    status = dbMig.addRequest(classID, groupID, "add_exam")
    if status != True:
        bot.send_message(groupID, ('🚫Error while adding request'))
    bot.send_message(groupID,('🔹Yeah! Now you can add the exam from this url:') + '\n' + f'http://127.0.0.1:8000/add-exam/{classID}')

def editExam(bot,examID,groupID):
    status = dbMig.addRequest(examID, groupID, "edit_exam")
    if status != True:
        bot.send_message(groupID, ('🚫Error while adding request'))
    bot.send_message(groupID,('🔹Yeah! Now you can edit the exam from this url:') + '\n' + f'http://127.0.0.1:8000/edit-exam/{examID}')

def activeReminder(examID,groupID):
    publishEvent("activeReminder", {'examID':examID,'groupID':groupID})


def deactiveReminder(examID,groupID):
    publishEvent("deactiveReminder", {'examID': examID, 'groupID': groupID})

def getAllExams(bot,classID,groupID):
    list = dbMig.getExams(classID)
    if list == None:
        bot.send_message(("🚫Your request for getting exams, failed"))
    wholeMessage = ""
    markup = InlineKeyboardMarkup()
    for item in list:
        message = (f"Title: ")+f"{item[1]}"+("\n Date: ")+f"{item[3]}"+"\n-----------------\n"
        wholeMessage = wholeMessage + message
        btn = InlineKeyboardButton(f'{item[1]}', callback_data=f"exam_{item[0]}_{groupID}")
        markup.add(btn)
    back=InlineKeyboardButton(('↩️Back'),callback_data=f'class_{classID}_{groupID}')
    markup.add(back)
    bot.send_message(groupID, wholeMessage + ("\n🔹The number of exams: ")+f"{len(list)}", reply_markup=markup)

def getExam(bot,examID,groupID):
    exam = dbMig.getExam(examID)
    if exam == None:
        bot.send_message(groupID, ("Your request for getting exam, failed"))
    message = ("Title: ")+f"{exam[1]}"+("\n Date: ")+f"{exam[3]}"
    markup = InlineKeyboardMarkup()
    edit = InlineKeyboardButton(('Edit'), callback_data=f'editExam_{exam[0]}_{groupID}')
    if exam[4]!='0':
        reminder=InlineKeyboardButton(('🔴DeActive Reminder'),callback_data=f"deactive_{exam[0]}_{groupID}")
    else:
        reminder=InlineKeyboardButton(('🟢Active Reminder'),callback_data=f"active_{exam[0]}_{groupID}")
    delete = InlineKeyboardButton(('Delete'), callback_data=f"deleteExam_{exam[0]}_{groupID}")
    markup.add(edit,reminder)
    markup.add(delete)
    bot.send_message(groupID, message, reply_markup=markup)

def deleteExam(bot,examID,groupID):
    status=dbMig.deleteExam(examID)
    if status:
        status = dbMig.delRequest(examID)
        if status:
            bot.send_message(groupID, ("✅The student successfully deleted"))