import telebot
from shared.constants import Token
from handlers import register_handlers
from shared.dbMig import createTables
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
            match data['event']:
                case 'lecture-added':
                    groupID = data['data']['groupID']
                    bot.send_message(groupID, "Lecture successfully added!")
                case 'lecture-edited':
                    groupID = data['data']['groupID']
                    bot.send_message(groupID, "Lecture successfully edited!")
                case 'class-added':
                    groupID= data['data']['groupID']
                    bot.send_message(groupID,"Class successfully added!")
                case 'class-edited':
                    groupID = data['data']['groupID']
                    bot.send_message(groupID, "Class successfully edited!")
                case 'student-added':
                    groupID= data['data']['groupID']
                    bot.send_message(groupID,"You successfully added to this class!")
                case 'student-edited':
                    groupID = data['data']['groupID']
                    bot.send_message(groupID, "your info successfully edited!")

threading.Thread(target=listen_for_events, daemon=True).start()

createTables()
storeGroupIDs()
register_handlers(bot)
bot.infinity_polling()
