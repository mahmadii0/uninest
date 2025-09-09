import telebot
from telebot.types import Message,InlineKeyboardButton,InlineKeyboardMarkup
import group_cr,class_cr,student_cr,lecture_cr
from shared import dbMig


def register_handlers(bot: telebot):
    @bot.message_handler(commands=['start'])
    def start(message: Message):
        if message.chat.type == "private":
            name = message.from_user.first_name
            bot.send_message(message.chat.id,f'welcome to UniNest {name}!')
        else:
            if int(message.chat.id) in group_cr.groupIDs:
                markup=InlineKeyboardMarkup()
                classes=InlineKeyboardButton(('Manage Classes'),callback_data=f'manageClasses_{message.chat.id}')
                lectures=InlineKeyboardButton(('Manage Lectures'),callback_data=f'manageLectures_{message.chat.id}')
                students=InlineKeyboardButton(('Manage Students'),callback_data=f'manageStudents_{message.chat.id}')
                searchFile=InlineKeyboardButton(('Search File'),callback_data=f'searchFiles_{message.chat.id}')
                markup.add(lectures,classes,students,searchFile)
                bot.send_message(message.chat.id, f'How can i help you?',reply_markup=markup)
            else:
                group_cr.langChoosing(bot, message)


    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        if call.data=='persian':
            group_cr.configureGroup(bot, 'fa', call)
        elif call.data=='english':
            group_cr.configureGroup(bot, 'en', call)
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
            elif operate=='manageStudents':
                student_cr.manageStudents(bot, groupID)
            elif operate=='searchFiles':
                pass
            #lecture
            elif operate=='addLecture':
                lecture_cr.addLecture(bot, groupID)
            elif operate=='getAllLectures':
                lecture_cr.getAllLectures(bot, groupID)
            elif operate=='lecture':
                lecture_cr.getLecture(bot,modelsID,groupID)
            elif operate=='getLecture':
                lecture_cr.getLecture(bot,modelsID,groupID)
            elif operate=='editLecture':
                lecture_cr.editLecture(bot,modelsID,groupID)
            elif operate == 'deleteLecture':
                status=dbMig.addRequest(modelsID,groupID,"delete_lecture")
                if status:
                    markup = InlineKeyboardMarkup()
                    yes = InlineKeyboardButton('yes', callback_data=f"yesAnswr_{modelsID}_{groupID}")
                    no=InlineKeyboardButton('no',callback_data=f"noAnswr_{groupID}")
                    markup.add(yes,no)
                    bot.send_message(groupID, "Are you sure you want to delete the lecture?",reply_markup=markup)
            elif operate == 'yesAnswr':
                request=dbMig.getRequest(modelsID)
                match request[2]:
                    case "delete_lecture":
                        lecture_cr.deleteLecture(bot,modelsID,groupID)
            elif operate == 'noAnswr':
                bot.send_message(groupID,"Delete process was canceled")




