from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler


class ChatBot():
    def __init__(self):
        self.bot = Bot('1736332153:AAFb6_GN9SqZMSFa0aLqUAU6IM32nLaCZr8')
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.scheduler.pause()

    def post_message(self, chat_id=388535300, message='Hello world!'):
        if (len(self.scheduler.get_jobs()) == 0):
            self.scheduler.pause()
        return self.bot.send_message(chat_id=chat_id, text=message)

    def post_scheduled_message(self, date, chat_id=388535300, message='Hello world'):
        '''
        Adding message to scheduler query
        :param date: date in format "2021-03-27 15:38:50"
        '''
        if (len(self.scheduler.get_jobs()) == 0):
            self.scheduler.resume()
        self.scheduler.add_job(self.post_message, 'date', run_date=date, args=[chat_id, message])
