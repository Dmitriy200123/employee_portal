from apscheduler.schedulers.background import BackgroundScheduler
from slack import WebClient, AsyncWebClient


class SlackBot:

    def __init__(self, token):
        self.client = WebClient(token)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.scheduler.pause()
        self.client.auth_test()

    def post_message(self, message, channel_id):
        if len(self.scheduler.get_jobs()) == 0:
            self.scheduler.pause()
        return self.client.chat_postMessage(channel=channel_id, text=message)

    def post_scheduled_message(self, date, message, channel_id):
        '''
        Adding message to scheduler query
        :param date: date in format "2021-03-27 15:38:50"
        '''
        if len(self.scheduler.get_jobs()) == 0:
            self.scheduler.resume()
        self.scheduler.add_job(self.post_message, 'date', run_date=date, args=[message, channel_id])
