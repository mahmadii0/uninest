from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
from shared.models import Student
from shared import dbMig
from utils import setLanguage

randnums=[]

def addStudent(bot,stdID,stdName,stdUsername,classID,groupID):
    _ = setLanguage(str(groupID))
    student=Student(
        name=stdName,
        userName=stdUsername
    )
    student.StudentID=stdID
    status = dbMig.addStudent(student,groupID)
    if status:
        status=dbMig.addStudentToClass(student.StudentID,classID,groupID)
        if status:
            bot.send_message(groupID,_('🤖Now, you added to this class '))

def getAllStudent(bot,classID,groupID):
    _ = setLanguage(str(groupID))
    list = dbMig.getAllStudent(classID,groupID)
    if list == None:
        bot.send_message(groupID,_("🚫Your request for getting all students, failed"))
    wholeMessage = ""
    markup = InlineKeyboardMarkup()
    for item in list:
        message = _("Student name: ")+f"{item[0]}"+_("\n Username: ")+f"{item[1]}"+"\n-----------------\n"
        wholeMessage = wholeMessage + message
        btn = InlineKeyboardButton(f'{item[1]}', callback_data=f"student_{item[0]}_{groupID}")
        markup.add(btn)
    back=InlineKeyboardButton(_('Back'),callback_data=f'class_{classID}_{groupID}')
    markup.add(back)
    bot.send_message(groupID,wholeMessage + _("\n🔹The number of students: ")+f"{len(list)}", reply_markup=markup)

def getStudent(bot,studentID,groupID):
    _ = setLanguage(str(groupID))
    student = dbMig.getStudent(studentID, groupID)
    if student == None:
        bot.send_message(groupID, _("🚫Your request for getting student, failed"))
    message = _("Student name: ")+f"{student[1]}"+_("\n Username: ")+f"{student[2]}"
    markup = InlineKeyboardMarkup()
    edit = InlineKeyboardButton(_('Edit'), callback_data=f"editStudent_{student[0]}_{groupID}")
    delete = InlineKeyboardButton(_('Delete'), callback_data=f"deleteStudent_{student[0]}_{groupID}")
    markup.add(edit, delete)
    bot.send_message(groupID, message, reply_markup=markup)

def deleteStudent(bot,studentID,classID,groupID):
    _ = setLanguage(str(groupID))
    status = dbMig.deleteStudent(studentID,classID,groupID)
    if status:
        status = dbMig.delRequest(studentID)
        if status:
            bot.send_message(groupID, _("✅The student successfully deleted"))