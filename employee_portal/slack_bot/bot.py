from slack import WebClient, AsyncWebClient
import asyncio


class ChatBot:

    def __init__(self):
        self.client = WebClient('xoxb-1918468674416-1907327567825-W1FsgXG3X0rxJLYnB203FRYU')
        self.AsyncClient = AsyncWebClient('xoxb-1918468674416-1907327567825-W1FsgXG3X0rxJLYnB203FRYU')

    def post_message(self, message: str, channel_id: str):
        return self.client.chat_postMessage(channel=channel_id, text=message)

    def schedule_message(self, message: str, channel_id: str, date):
        return self.client.chat_scheduleMessage(channel=channel_id, post_at=date, text=message)

    async def post_message_async(self):
        response = await self.AsyncClient.chat_postMessage(channel='#random', text="Hello world!")
        return response

    async def schedule_message_async(self, date):
        response = await self.AsyncClient.chat_scheduleMessage(channel='#random', text='async shcdeule', post_at=date)
        return response

# loop = asyncio.get_event_loop()
# loop.run_until_complete(post())
# loop.run_until_complete(asyncio.sleep(1))
# loop.close()
