from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
from utils import rand,setLanguage
from shared import dbMig

randnums=[]

def manageClasses(bot,groupID):
    _=setLanguage(str(groupID))
    markup=InlineKeyboardMarkup()
    add=InlineKeyboardButton(_('Add Class'),callback_data=f'addClass_{groupID}')
    getAll=InlineKeyboardButton(_('Get All Classes'),callback_data=f'getAllClasses_{groupID}')
    markup.add(add,getAll)
    bot.send_message(groupID,_('🤖Select a one of buttons to do that'),reply_markup=markup)

def addClass(bot,groupID):
    _ = setLanguage(str(groupID))
    _num = rand(randnums)
    status = dbMig.addRequest(_num, groupID, "add_class")
    if status != True:
        bot.send_message(groupID, _('🚫Error while adding request'))
    bot.send_message(groupID,_('🔹Yeah! Now you can add the class from this url:') + '\n' + f'http://127.0.0.1:8000/add-class/{_num}')

def getAllClass(bot,groupID):
    _ = setLanguage(str(groupID))
    list = dbMig.getAllClass(groupID)
    if list == None:
        bot.send_message(groupID,_("🚫Your request for getting all classes, failed"))
    wholeMessage = ""
    markup = InlineKeyboardMarkup()
    for item in list:
        lec=dbMig.getLecture(item[2],groupID)
        message = _("Class name: ")+f"{item[1]}"+_("\n Lecture: ")+f"{lec[1]}"+"\n-----------------\n"
        wholeMessage = wholeMessage + message
        btn = InlineKeyboardButton(f'{item[1]}', callback_data=f"class_{item[0]}_{groupID}")
        markup.add(btn)
    back=InlineKeyboardButton(_('↩️Back'),callback_data=f'manageClasses_{groupID}')
    markup.add(back)
    bot.send_message(groupID, wholeMessage + _("\n🔹The number of classes: ")+f"{len(list)}", reply_markup=markup)

def getClass(bot,classID,groupID):
    _ = setLanguage(str(groupID))
    clss = dbMig.getClass(classID, groupID)
    if clss == None:
        bot.send_message(groupID, _("🚫Your request for getting class, failed"))
    lec = dbMig.getLecture(clss[2], groupID)
    message = _("Class name: ")+f"{clss[1]}"+ _("\n Lecture: ")+f"{lec[1]}"
    markup = InlineKeyboardMarkup()
    edit = InlineKeyboardButton(_('Edit'), callback_data=f"editClass_{clss[0]}_{groupID}")
    delete = InlineKeyboardButton(_('Delete'), callback_data=f"deleteClass_{clss[0]}_{groupID}")
    exams= InlineKeyboardButton(_('📋Exams'),callback_data=f"getExams_{clss[0]}_{groupID}")
    addExam=InlineKeyboardButton(_('📋Add Exam'),callback_data=f"addExam_{clss[0]}_{groupID}")
    addFile=InlineKeyboardButton(_('💾Add File To Class'),callback_data=f"addFile_{clss[0]}_{groupID}")
    getFiles=InlineKeyboardButton(_('💾Get All Files'),callback_data=f"getAllFiles_{clss[0]}_{groupID}")
    addStd=InlineKeyboardButton(_('🧑‍🎓Add Me As Student'),callback_data=f'addStudent_{clss[0]}_{groupID}')
    deleteStd=InlineKeyboardButton(_('🧑‍🎓Delete Me From Class'),callback_data=f'deleteStudent_{clss[0]}_{groupID}')
    getAll=InlineKeyboardButton(_('🧑‍🎓Get All Students'),callback_data=f'getAllStudents_{clss[0]}_{groupID}')
    back=InlineKeyboardButton(_('↩️Back'),callback_data=f'getAllClasses_{groupID}')
    markup.add(edit,delete,exams,addExam,addFile,getFiles,addStd,deleteStd,getAll,back)
    bot.send_message(groupID, message, reply_markup=markup)

def editClass(bot,classID,groupID):
    _ = setLanguage(str(groupID))
    status = dbMig.addRequest(classID, groupID, "edit_class")
    if status != True:
        bot.send_message(groupID, _('🚫Error while adding request'))
    bot.send_message(groupID,_('🔹Yeah! Now you can edit the class from this url:') + '\n' + f'http://127.0.0.1:8000/edit-class/{classID}')

def deleteClass(bot,classID,groupID):
    _ = setLanguage(str(groupID))
    dbMig.deleteClassStds(classID,groupID)
    dbMig.deleteClassExams(classID)
    dbMig.deleteClassFiles(classID)
    status = dbMig.deleteClass(classID,groupID)
    if status:
        status = dbMig.delRequest(classID)
        if status:
            bot.send_message(groupID,_("✅The class successfully deleted"))