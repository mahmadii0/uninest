import telebot
from datetime import datetime, timedelta
from shared import dbMig
from shared.constants import Token
from handlers import register_handlers
from shared.dbMig import createTables
from group_cr import storeGroupIDs
import redis,json,threading
from apscheduler.schedulers.background import BackgroundScheduler
from utils import setLanguage


bot = telebot.TeleBot(Token)

def reminderMessage(bot,students,exam):
    _ = setLanguage(groupID=str(exam[2]),classID=True)
    for student in students:
        bot.send_message(student[2], _(f"📅Reminder \n Your {exam[1]} exam is on {exam[3]}"))

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
                    _=setLanguage(str(groupID))
                    bot.send_message(groupID, _("✅Lecture successfully added!"))
                case 'lecture-edited':
                    groupID = data['data']['groupID']
                    _ = setLanguage(str(groupID))
                    bot.send_message(groupID, _("✅Lecture successfully edited!"))
                case 'class-added':
                    groupID= data['data']['groupID']
                    _ = setLanguage(str(groupID))
                    bot.send_message(groupID,_("✅Class successfully added!"))
                case 'class-edited':
                    groupID = data['data']['groupID']
                    _ = setLanguage(str(groupID))
                    bot.send_message(groupID, _("✅Class successfully edited!"))
                case 'student-added':
                    groupID= data['data']['groupID']
                    _ = setLanguage(str(groupID))
                    bot.send_message(groupID,_("✅You successfully added to this class!"))
                case 'student-edited':
                    groupID = data['data']['groupID']
                    _ = setLanguage(str(groupID))
                    bot.send_message(groupID, _("✅your info successfully edited!"))
                case 'exam-added':
                    groupID = data['data']['groupID']
                    _ = setLanguage(str(groupID))
                    bot.send_message(groupID, _("✅Exam successfully added!"))
                case 'exam-edited':
                    groupID = data['data']['groupID']
                    _ = setLanguage(str(groupID))
                    bot.send_message(groupID, _("✅Exam successfully edited!"))
                case 'activeReminder':
                    examID=data['data']['examID']
                    groupID= data['data']['groupID']
                    _ = setLanguage(str(groupID))
                    exam = dbMig.getExam(examID)
                    students=dbMig.getAllStudent(exam[2],groupID)
                    reminderTime = exam[3] - timedelta(days=1)
                    job = scheduler.add_job(reminderMessage, "date", run_date=reminderTime, args=[bot, students, exam])
                    status = dbMig.activeReminder(job.id, exam[0])
                    if status:
                        bot.send_message(groupID, _("✅The Reminder successfully activated"))
                case 'deactiveReminder':
                    examID = data['data']['examID']
                    groupID = data['data']['groupID']
                    _ = setLanguage(str(groupID))
                    exam = dbMig.getExam(examID)
                    scheduler.remove_job(exam[4])
                    status=dbMig.deactiveReminder(examID)
                    if status:
                        bot.send_message(groupID,_("✅The Reminder successfully deactivated"))


threading.Thread(target=listen_for_events, daemon=True).start()
scheduler = BackgroundScheduler()
scheduler.start()

createTables()
storeGroupIDs()
register_handlers(bot)
bot.infinity_polling()
