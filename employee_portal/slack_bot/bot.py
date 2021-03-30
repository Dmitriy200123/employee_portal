import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from slack import WebClient, AsyncWebClient


class ChatBot:

    def __init__(self):
        self.client = WebClient('xoxb-1918468674416-1907327567825-W1FsgXG3X0rxJLYnB203FRYU')
        self.AsyncClient = AsyncWebClient('xoxb-1918468674416-1907327567825-W1FsgXG3X0rxJLYnB203FRYU')
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.scheduler.pause()

    def post_message(self, message='Hello world', channel_id='#random'):
        if (len(self.scheduler.get_jobs()) == 0):
            self.scheduler.pause()
        return self.client.chat_postMessage(channel=channel_id, text=message)

    async def post_message_async(self, message: str, channel_id: str):
        response = await self.AsyncClient.chat_postMessage(channel=channel_id, text=message)
        return response

    def post_scheduled_message(self, date, message='Hello world', channel_id='#random', ):
        '''
        Adding message to scheduler query
        :param date: date in format "2021-03-27 15:38:50"
        '''
        if (len(self.scheduler.get_jobs()) == 0):
            self.scheduler.resume()
        self.scheduler.add_job(self.post_message, 'date', run_date=date, args=[message, channel_id])

    # def schedule_message(self, message: str, channel_id: str, date):
    #     return self.client.chat_scheduleMessage(channel=channel_id, post_at=date, text=message)
    #
    # async def schedule_message_async(self, date):
    #     response = await self.AsyncClient.chat_scheduleMessage(channel='#random', text='async shcdeule', post_at=date)
    #     return response
