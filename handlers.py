import telebot
from telebot.types import Message

def register_handlers(bot: telebot):
    @bot.message_handler(commands=['start'])
    def start(message: Message):
        if message.chat.type == "private":
            userId = message.from_user.id
