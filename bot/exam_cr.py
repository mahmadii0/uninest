from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
from shared import dbMig

def addExam(bot,classID,groupID):
    status = dbMig.addRequest(classID, groupID, "add_exam")
    if status != True:
        bot.send_message(groupID, 'Error while adding request')
    bot.send_message(groupID,
                     'Yeah! Now you can add the exam from this url:' + '\n' + f'http://127.0.0.1:8000/add-exam/{classID}')

def editExam(bot,examID,groupID):
    status = dbMig.addRequest(examID, groupID, "edit_exam")
    if status != True:
        bot.send_message(groupID, 'Error while adding request')
    bot.send_message(groupID,
                     'Yeah! Now you can edit the exam from this url:' + '\n' + f'http://127.0.0.1:8000/edit-exam/{examID}')

def getExams(bot,classID,groupID):
    list = dbMig.getExams(classID)
    if list == None:
        bot.send_message("Your request for getting exams, failed")
    wholeMessage = ""
    markup = InlineKeyboardMarkup()
    for item in list:
        message = f"""
        title: {item[1]}
        date: {item[3]}
        -----------------
        """
        wholeMessage = wholeMessage + message
        btn = InlineKeyboardButton(f'{item[1]}', callback_data=f"exam_{item[0]}_{groupID}")
        markup.add(btn)
    bot.send_message(groupID, wholeMessage + f"\nnumber of exams: {len(list)}", reply_markup=markup)

def getExam(bot,examID,groupID):
    exam = dbMig.getExam(examID)
    if exam == None:
        bot.send_message(groupID, "Your request for getting exam, failed")
    message = f"""
    title: {exam[1]}
    date: {exam[3]}"""
    markup = InlineKeyboardMarkup()
    edit = InlineKeyboardButton('edit', callback_data=f'editExam_{exam[0]}_{groupID}')
    delete = InlineKeyboardButton('delete', callback_data=f"deleteExam_{exam[0]}_{groupID}")
    markup.add(delete,edit)
    bot.send_message(groupID, message, reply_markup=markup)

def deleteExam(bot,examID,groupID):
    status=dbMig.deleteExam(examID)
    if status:
        status = dbMig.delRequest(examID)
        if status:
            bot.send_message(groupID, "The student successfully deleted")