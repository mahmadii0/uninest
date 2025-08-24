import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from constants import Token
from handlers import register_handlers

bot = telebot.TeleBot(Token)
register_handlers(bot)
if __name__ == "__main__":
    bot.infinity_polling()