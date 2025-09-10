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
    list = dbMig.getAllLecture(groupID)
    if list == None:
        bot.send_message("Your request for getting all lectures, failed")
    wholeMessage = ""
    markup = InlineKeyboardMarkup()
    for item in list:
        message = f"""
        lecture name: {item[1]}
        phone: {item[2]}
        rate: {item[3]}
        -----------------
        """
        wholeMessage = wholeMessage + message
        btn = InlineKeyboardButton(f'{item[1]}', callback_data=f"lecture_{item[0]}_{groupID}")
        markup.add(btn)

    bot.send_message(groupID, wholeMessage + f"\nnumber of lectures: {len(list)}", reply_markup=markup)

def getClass(bot,classID,groupID):
    lec = dbMig.getLecture(lecID, groupID)
    if lec == None:
        bot.send_message(groupID, "Your request for getting lecture, failed")
    message = f"""
    lecture name: {lec[1]}
    phone: {lec[2]}
    rate: {lec[3]}"""
    markup = InlineKeyboardMarkup()
    edit = InlineKeyboardButton('edit', callback_data=f"editLecture_{lec[0]}_{groupID}")
    delete = InlineKeyboardButton('delete', callback_data=f"deleteLecture_{lec[0]}_{groupID}")
    markup.add(edit, delete)
    bot.send_message(groupID, message, reply_markup=markup)

def editClass(bot,classID,groupID):
    status = dbMig.addRequest(lecID, groupID, "edit_lecture")
    if status != True:
        bot.send_message(groupID, 'Error while adding request')
    bot.send_message(groupID,
                     'Yeah! Now you can edit the lecture from this url:' + '\n' + f'http://127.0.0.1:8000/edit-lecture/{lecID}')

def deleteClass():
    pass