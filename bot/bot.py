import telebot
from constants import Token
from handlers import register_handlers
from dbMig import createTables
from group_cr import storeGroupIDs
import redis,json,threading

bot = telebot.TeleBot(Token)

r = redis.Redis(host="localhost", port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe("uninest")

def listen_for_events():
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            if data['event'] == 'lecture-added':
                groupID = data['data']['groupID']
                bot.send_message(groupID, "Lecture successfully added!")

threading.Thread(target=listen_for_events, daemon=True).start()

createTables()
storeGroupIDs()
register_handlers(bot)
bot.infinity_polling()
