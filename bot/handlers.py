import telebot
from telebot.types import Message,InlineKeyboardButton,InlineKeyboardMarkup
import group_cr,class_cr,student_cr,lecture_cr
import exam_cr
import file_cr
from shared import dbMig, constants
from utils import deleteMessage,checkAdmin

def accessDenied(bot,groupID):
    bot.send_message(groupID, "🚫Just the owner or admin of the group can to that!")

def register_handlers(bot: telebot):
    @bot.message_handler(commands=['start'])
    def start(message: Message):
        if message.chat.type == "private":
            name = message.from_user.first_name
            bot.send_message(message.chat.id,(f'welcome to UniNest')+f' {name}!')
        else:
            if int(message.chat.id) in group_cr.groupIDs:
                markup=InlineKeyboardMarkup()
                classes=InlineKeyboardButton(('Manage Classes'),callback_data=f'manageClasses_{message.chat.id}')
                lectures=InlineKeyboardButton(('Manage Lectures'),callback_data=f'manageLectures_{message.chat.id}')
                markup.add(lectures,classes)
                bot.send_message(message.chat.id, (f'🤖How can i help you?'),reply_markup=markup)
            else:
                group_cr.langChoosing(bot, message)

    @bot.message_handler(content_types=['photo', 'document', 'audio', 'video', 'voice'])
    def handle_file(message):
        if not message.caption:
            bot.send_message(message.chat.id,('''🔹Please send file with caption that include a specific name
            Like: Booklet of chapter one'''))
            return
        rqust=dbMig.getRequest(str(message.chat.id))
        if type(rqust) != tuple:
            bot.send_message(message.chat.id,("""🚫You haven't request for adding file!
            Go to your class management and create a request for add file"""))
            return
        if rqust[2]=='add_file':
            status=file_cr.getFile(bot,message.caption,rqust[1],bool=True)
            if status:
                _=dbMig.delRequest(str(message.chat.id))
                bot.send_message(message.chat.id,("🚫You already have a file with this name! change it and send again"))
                return
            forwarded = bot.forward_message(constants.channelID,from_chat_id=message.chat.id,message_id=message.message_id)
            _=dbMig.delRequest(str(message.chat.id))
            file_cr.addFile(bot,message.caption,forwarded.message_id,rqust[1],message.chat.id)

    @bot.message_handler(func=lambda msg: msg.text and msg.text.startswith("search_"))
    def handle_search(message):
        fileName = message.text.split("search_", 1)[1].strip()
        file_cr.search(bot,fileName,message.chat.id)

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        deleteMessage(bot,call)
        status = checkAdmin(bot, call.message.chat.id, call.from_user.id)
        if call.data=='persian':
            if status:
                group_cr.configureGroup(bot, 'fa', call)
            else:
                accessDenied(bot,call.message.chat.id)
        elif call.data=='english':
            if status:
                group_cr.configureGroup(bot, 'en', call)
            else:
                accessDenied(bot, call.message.chat.id)
        else:
            operate=None
            groupID=None
            modelsID=None
            data= call.data.split('_')
            if len(data)==2:
                operate,groupID=data
            elif len(data)==3:
                operate,modelsID,groupID=data
            if operate=='manageClasses':
                class_cr.manageClasses(bot, groupID)
            elif operate=='manageLectures':
                lecture_cr.manageLectures(bot, groupID)

            #lecture
            elif operate=='addLecture':
                if status:
                    lecture_cr.addLecture(bot, groupID)
                else:
                    accessDenied(bot, call.message.chat.id)
            elif operate=='getAllLectures':
                lecture_cr.getAllLectures(bot, groupID)
            elif operate=='lecture':
                lecture_cr.getLecture(bot,modelsID,groupID)
            elif operate=='getLecture':
                lecture_cr.getLecture(bot,modelsID,groupID)
            elif operate=='editLecture':
                if status:
                    lecture_cr.editLecture(bot,modelsID,groupID)
                else:
                    accessDenied(bot, call.message.chat.id)
            elif operate == 'deleteLecture':
                if status:
                    status=dbMig.addRequest(modelsID,groupID,"delete_lecture")
                    if status:
                        markup = InlineKeyboardMarkup()
                        yes = InlineKeyboardButton(('Yes'), callback_data=f"yesAnswr_{modelsID}_{groupID}")
                        no=InlineKeyboardButton(('No'),callback_data=f"noAnswr_{modelsID}_{groupID}")
                        markup.add(yes,no)
                        bot.send_message(groupID, ("🔸Are you sure you want to delete the lecture?"),reply_markup=markup)
                else:
                    accessDenied(bot, call.message.chat.id)

            #Classes
            elif operate=='addClass':
                if status:
                    class_cr.addClass(bot, groupID)
                else:
                    accessDenied(bot, call.message.chat.id)
            elif operate=='getAllClasses':
                class_cr.getAllClass(bot, groupID)
            elif operate=='class':
                class_cr.getClass(bot,modelsID,groupID)
            elif operate=='editClass':
                if status:
                    class_cr.editClass(bot,modelsID,groupID)
                else:
                    accessDenied(bot, call.message.chat.id)
            elif operate == 'deleteClass':
                if status:
                    status=dbMig.addRequest(modelsID,groupID,"delete_class")
                    if status:
                        markup = InlineKeyboardMarkup()
                        yes = InlineKeyboardButton(('Yes'), callback_data=f"yesAnswr_{modelsID}_{groupID}")
                        no=InlineKeyboardButton(('No'),callback_data=f"noAnswr_{modelsID}_{groupID}")
                        markup.add(yes,no)
                        bot.send_message(groupID, ("🔸Are you sure you want to delete the class?"),reply_markup=markup)
                else:
                    accessDenied(bot, call.message.chat.id)

            #Students
            elif operate=='addStudent':
                stdID=call.from_user.id
                if call.from_user.first_name == None and call.from_user.last_name==None:
                    stdName='No name'
                elif call.from_user.first_name == None and call.from_user.last_name!=None:
                    stdName=call.from_user.last_name
                elif call.from_user.first_name != None and call.from_user.last_name==None:
                    stdName = call.from_user.first_name
                elif call.from_user.first_name != None and call.from_user.last_name!=None:
                    stdName=(call.from_user.first_name)+" "+(call.from_user.last_name)
                stdUsername=call.from_user.username
                student_cr.addStudent(bot,stdID,stdName,stdUsername,modelsID,groupID)
            elif operate=='getAllStudents':
                student_cr.getAllStudent(bot,modelsID,groupID)
            elif operate=='student':
                student_cr.getStudent(bot,modelsID,groupID)
            elif operate == 'deleteStudent':
                student=dbMig.getStudent(call.from_user.id,modelsID,groupID)
                if student==None:
                    bot.send_message(groupID,('You already not in this class!'))
                    return
                status=dbMig.addRequest(modelsID,groupID,"delete_student")
                if status:
                    markup = InlineKeyboardMarkup()
                    yes = InlineKeyboardButton(('Yes'), callback_data=f"yesAnswr_{modelsID}_{groupID}")
                    no=InlineKeyboardButton(('No'),callback_data=f"noAnswr_{modelsID}_{groupID}")
                    markup.add(yes,no)
                    bot.send_message(groupID,("🔸Are you sure you want to delete the student?"),reply_markup=markup)

            #Exam
            elif operate == 'addExam':
                if status:
                    exam_cr.addExam(bot,modelsID,groupID)
                else:
                    accessDenied(bot, call.message.chat.id)
            elif operate == 'editExam':
                if status:
                    exam_cr.editExam(bot,modelsID,groupID)
                else:
                    accessDenied(bot, call.message.chat.id)
            elif operate == 'getExams':
                exam_cr.getAllExams(bot,modelsID,groupID)
            elif operate == 'exam':
                exam_cr.getExam(bot,modelsID,groupID)
            elif operate == 'deleteExam':
                if status:
                    status=dbMig.addRequest(modelsID,groupID,"delete_exam")
                    if status:
                        markup = InlineKeyboardMarkup()
                        yes = InlineKeyboardButton(('Yes'), callback_data=f"yesAnswr_{modelsID}_{groupID}")
                        no=InlineKeyboardButton(('No'),callback_data=f"noAnswr_{modelsID}_{groupID}")
                        markup.add(yes,no)
                        bot.send_message(groupID, ("🔸Are you sure you want to delete the exam?"),reply_markup=markup)
                else:
                    accessDenied(bot, call.message.chat.id)

            #File
            elif operate == 'addFile':
                if status:
                    status=dbMig.addRequest(groupID,modelsID,'add_file')
                    if status:
                        markup=InlineKeyboardMarkup()
                        cancel=InlineKeyboardButton(('Cancel adding file'),callback_data=f'cancel_{groupID}')
                        markup.add(cancel)
                        bot.send_message(groupID,('🔹Please send your file with a specific name in its caption'),reply_markup=markup)
                else:
                    accessDenied(bot, call.message.chat.id)
            elif operate == 'getAllFiles':
                file_cr.getAllFiles(bot,modelsID,groupID)
            elif operate == 'getFile':
                file_cr.getFile(bot,modelsID,groupID)
            elif operate == 'deleteFile':
                if status:
                    status=dbMig.addRequest(modelsID,groupID,"delete_file")
                    if status:
                        markup = InlineKeyboardMarkup()
                        yes = InlineKeyboardButton(('Yes'), callback_data=f"yesAnswr_{modelsID}_{groupID}")
                        no=InlineKeyboardButton(('No'),callback_data=f"noAnswr_{modelsID}_{groupID}")
                        markup.add(yes,no)
                        bot.send_message(groupID, ("🔸Are you sure you want to delete the file?"),reply_markup=markup)
                else:
                    accessDenied(bot, call.message.chat.id)

            elif operate == 'yesAnswr':
                request=dbMig.getRequest(modelsID)
                if type(request)==tuple:
                    match request[2]:
                        case "delete_lecture":
                            lecture_cr.deleteLecture(bot,modelsID,groupID)
                            _=dbMig.delRequest(modelsID)
                        case "delete_class":
                            class_cr.deleteClass(bot,modelsID,groupID)
                            _ = dbMig.delRequest(modelsID)
                        case "delete_student":
                            student_cr.deleteStudent(bot,call.from_user.id,modelsID,groupID)
                            _ = dbMig.delRequest(modelsID)
                        case "delete_exam":
                            exam_cr.deleteExam(bot,modelsID,groupID)
                        case "delete_file":
                            file_cr.deleteFile(bot,modelsID,groupID)
            elif operate == 'noAnswr':
                status=dbMig.delRequest(modelsID)
                if status:
                    bot.send_message(groupID,"Delete process was canceled")
            elif operate == 'cancel':
                status=dbMig.delRequest(groupID)
                if status:
                    bot.send_message(groupID,'Adding file process was canceled')




