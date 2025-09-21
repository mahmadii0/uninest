from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
from shared.models import Student
from shared import dbMig

randnums=[]

def addStudent(bot,stdID,stdName,stdUsername,classID,groupID):
    student=Student(
        name=stdName,
        userName=stdUsername
    )
    student.StudentID=stdID
    status = dbMig.addStudent(student,groupID)
    if status:
        status=dbMig.addStudentToClass(student.StudentID,classID,groupID)
        if status:
            bot.send_message(groupID,'🤖Now, you added to this class ')

def getAllStudent(bot,classID,groupID):
    list = dbMig.getAllStudent(classID,groupID)
    if list == None:
        bot.send_message("🚫Your request for getting all students, failed")
    wholeMessage = ""
    markup = InlineKeyboardMarkup()
    for item in list:
        message = ("Student name: ")+f"{item[0]}"+("\n Username: ")+f"{item[1]}"+"\n-----------------"
        wholeMessage = wholeMessage + message
        btn = InlineKeyboardButton(f'{item[1]}', callback_data=f"student_{item[0]}_{groupID}")
        markup.add(btn)
    back=InlineKeyboardButton(('Back'),callback_data=f'class_{classID}_{groupID}')
    markup.add(back)
    bot.send_message(groupID,wholeMessage + ("\n🔹The number of students: ")+f"{len(list)}", reply_markup=markup)

def getStudent(bot,studentID,groupID):
    student = dbMig.getStudent(studentID, groupID)
    if student == None:
        bot.send_message(groupID, ("🚫Your request for getting student, failed"))
    message = ("Student name: ")+f"{student[1]}"+("\n Username: ")+f"{student[2]}"
    markup = InlineKeyboardMarkup()
    edit = InlineKeyboardButton(('Edit'), callback_data=f"editStudent_{student[0]}_{groupID}")
    delete = InlineKeyboardButton(('Delete'), callback_data=f"deleteStudent_{student[0]}_{groupID}")
    markup.add(edit, delete)
    bot.send_message(groupID, message, reply_markup=markup)

def deleteStudent(bot,studentID,classID,groupID):
    status = dbMig.deleteStudent(studentID,classID,groupID)
    if status:
        status = dbMig.delRequest(studentID)
        if status:
            bot.send_message(groupID, ("✅The student successfully deleted"))