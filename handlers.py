import telebot
from telebot.types import Message,InlineKeyboardButton,InlineKeyboardMarkup
import group_cr
def register_handlers(bot: telebot):
    @bot.message_handler(commands=['start'])
    def start(message: Message):
        if message.chat.type == "private":
            name = message.from_user.first_name
            bot.send_message(message.chat.id,f'welcome to UniNest {name}!')
        else:
            if int(message.chat.id) in group_cr.groupIDs:
                markup=InlineKeyboardMarkup
                classes=InlineKeyboardButton(callback_data='manage_classes')
                lectures=InlineKeyboardButton(callback_data='manage_lecture')
                students=InlineKeyboardButton(callback_data='manage_students')
                bot.send_message(message.chat.id, f'What can i help you?')
            else:
                group_cr.langChoosing(bot,message)


    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        if call.data=='persian':
            group_cr.configureGroup(bot,'fa',call)
        elif call.data=='english':
            group_cr.configureGroup(bot,'en',call)
