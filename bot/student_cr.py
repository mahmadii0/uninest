from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup

from shared.models import Student
from utils import rand
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
            bot.send_message(groupID,
                     'Now, you added to this class ')

def getAllStudent(bot,classID,groupID):
    list = dbMig.getAllStudent(classID,groupID)
    if list == None:
        bot.send_message("Your request for getting all students, failed")
    wholeMessage = ""
    markup = InlineKeyboardMarkup()
    for item in list:
        message = f"""
        student name: {item[0]}
        username: {item[1]}
        -----------------
        """
        wholeMessage = wholeMessage + message
        btn = InlineKeyboardButton(f'{item[1]}', callback_data=f"student_{item[0]}_{groupID}")
        markup.add(btn)

    bot.send_message(groupID,wholeMessage + f"\nnumber of students: {len(list)}", reply_markup=markup)

def getStudent(bot,studentID,groupID):
    student = dbMig.getStudent(studentID, groupID)
    if student == None:
        bot.send_message(groupID, "Your request for getting student, failed")
    message = f"""
    student name: {student[1]}
    username: {student[2]}"""
    markup = InlineKeyboardMarkup()
    edit = InlineKeyboardButton('edit', callback_data=f"editStudent_{student[0]}_{groupID}")
    delete = InlineKeyboardButton('delete', callback_data=f"deleteStudent_{student[0]}_{groupID}")
    markup.add(edit, delete)
    bot.send_message(groupID, message, reply_markup=markup)

# def editStudent(bot,studentID,groupID):
#     status = dbMig.addRequest(studentID, groupID, "edit_student")
#     if status != True:
#         bot.send_message(groupID, 'Error while adding request')
#     bot.send_message(groupID,
#                      'Yeah! Now you can edit the student from this url:' + '\n' + f'http://127.0.0.1:8000/edit-student/{studentID}')

def deleteStudent(bot,studentID,classID,groupID):
    status = dbMig.deleteStudent(studentID,classID,groupID)
    if status:
        status = dbMig.delRequest(studentID)
        if status:
            bot.send_message(groupID, "The student successfully deleted")