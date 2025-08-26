import telebot
from telebot.types import Message,InlineKeyboardButton,InlineKeyboardMarkup
import group_cr,class_cr,student_cr,lecture_cr
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
                group_cr.langChoosing(bot,message)


    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        if call.data=='persian':
            group_cr.configureGroup(bot,'fa',call)
        elif call.data=='english':
            group_cr.configureGroup(bot,'en',call)
        else:
            operate=None
            groupID=None
            data= call.data.split('_')
            if len(data)==2:
                operate,groupID=data
            if operate=='manageClasses':
                class_cr.manageClasses(bot,groupID)
            elif operate=='manageLectures':
                lecture_cr.manageLectures(bot,groupID)
            elif operate=='manageStudents':
                student_cr.manageStudents(bot,groupID)
            elif operate=='searchFiles':
                pass
            #lecture
            elif operate=='addLecture':
                lecture_cr.addLecture(bot,groupID)
            elif operate=='getLecture':
                lecture_cr.getLecture(bot,groupID)
            elif operate=='getAllLectures':
                lecture_cr.getAllLectures(bot,groupID)


