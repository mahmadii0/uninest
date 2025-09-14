from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
from utils import rand
from shared import dbMig

randnums=[]

def manageClasses(bot,groupID):
    markup=InlineKeyboardMarkup()
    add=InlineKeyboardButton(('Add Class'),callback_data=f'addClass_{groupID}')
    getAll=InlineKeyboardButton(('Get All Classes'),callback_data=f'getAllClasses_{groupID}')
    markup.add(add,getAll)
    bot.send_message(groupID,'Select a one of buttons to do that',reply_markup=markup)

def addClass(bot,groupID):
    _num = rand(randnums)
    status = dbMig.addRequest(_num, groupID, "add_class")
    if status != True:
        bot.send_message(groupID, 'Error while adding request')
    bot.send_message(groupID,
                     'Yeah! Now you can add the class from this url:' + '\n' + f'http://127.0.0.1:8000/add-class/{_num}')

def getAllClass(bot,groupID):
    list = dbMig.getAllClass(groupID)
    if list == None:
        bot.send_message("Your request for getting all classes, failed")
    wholeMessage = ""
    markup = InlineKeyboardMarkup()
    for item in list:
        lec=dbMig.getLecture(item[2],groupID)
        message = f"""
        class name: {item[1]}
        lecture: {lec[1]}
        -----------------
        """
        wholeMessage = wholeMessage + message
        btn = InlineKeyboardButton(f'{item[1]}', callback_data=f"class_{item[0]}_{groupID}")
        markup.add(btn)

    bot.send_message(groupID, wholeMessage + f"\nnumber of classes: {len(list)}", reply_markup=markup)

def getClass(bot,classID,groupID):
    clss = dbMig.getClass(classID, groupID)
    if clss == None:
        bot.send_message(groupID, "Your request for getting class, failed")
    lec = dbMig.getLecture(clss[2], groupID)
    message = f"""
    class name: {clss[1]}
    lecture: {lec[1]}"""
    markup = InlineKeyboardMarkup()
    edit = InlineKeyboardButton('edit', callback_data=f"editClass_{clss[0]}_{groupID}")
    delete = InlineKeyboardButton('delete', callback_data=f"deleteClass_{clss[0]}_{groupID}")
    exams= InlineKeyboardButton('exams',callback_data=f"getExams_{clss[0]}_{groupID}")
    addExam=InlineKeyboardButton('add exam',callback_data=f"addExam_{clss[0]}_{groupID}")
    addStd=InlineKeyboardButton(('add me as student'),callback_data=f'addStudent_{clss[0]}_{groupID}')
    deleteStd=InlineKeyboardButton('delete me from class',callback_data=f'deleteStudent_{clss[0]}_{groupID}')
    getAll=InlineKeyboardButton(('Get All Students'),callback_data=f'getAllStudents_{clss[0]}_{groupID}')
    markup.add(edit,delete,exams,addStd,deleteStd,getAll)
    bot.send_message(groupID, message, reply_markup=markup)

def editClass(bot,classID,groupID):
    status = dbMig.addRequest(classID, groupID, "edit_class")
    if status != True:
        bot.send_message(groupID, 'Error while adding request')
    bot.send_message(groupID,
                     'Yeah! Now you can edit the class from this url:' + '\n' + f'http://127.0.0.1:8000/edit-class/{classID}')

def deleteClass(bot,classID,groupID):
    status = dbMig.deleteClass(classID, groupID)
    if status:
        status = dbMig.delRequest(classID)
        if status:
            bot.send_message(groupID, "The class successfully deleted")