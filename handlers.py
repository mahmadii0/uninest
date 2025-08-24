import telebot
from telebot.types import Message

def register_handlers(bot: telebot):
    @bot.message_handler(commands=['start'])
    def start(message: Message):
        if message.chat.type == "private":
            name = message.from_user.first_name
            bot.send_message(message.chat.id,f'welcome to UniNest {name}!')
