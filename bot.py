import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from constants import Token
from handlers import register_handlers
from app import createTables
from group_cr import storeGroupIDs

bot = telebot.TeleBot(Token)
createTables()
storeGroupIDs()
register_handlers(bot)
if __name__ == "__main__":
    bot.infinity_polling()