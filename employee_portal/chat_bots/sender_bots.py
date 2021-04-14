import enum

from chat_bots.models import Sender
from slack_bot.bot import SlackBot
from telegram_bot.bot import TelegramBot


class MessengerType(enum.Enum):
    Telegram = 'Telegram'
    Slack = 'Slack'


class SenderBots:
    new_employee_channel_id = None
    new_employee_chat_bot = None
    access_request_channel_id = None
    access_request_chat_bot = None

    @staticmethod
    def updateBots():
        sender = Sender.objects.first()
        employee_chat_bot = sender.newEmployeeChatBot
        access_chat_bot = sender.accessRequestChatBot
        SenderBots.new_employee_channel_id = sender.newEmployeeChannelId
        SenderBots.access_request_channel_id = sender.accessRequestChannelId
        SenderBots.new_employee_chat_bot = SenderBots.createBot(employee_chat_bot)
        SenderBots.access_request_chat_bot = SenderBots.createBot(access_chat_bot)

    @staticmethod
    def createBot(chat_bot):
        if chat_bot.botType.messenger_type == MessengerType.Telegram.name:
            return TelegramBot(chat_bot.token)

        if chat_bot.botType.messenger_type == MessengerType.Slack.name:
            return SlackBot(chat_bot.token)

    @staticmethod
    def sendNewEmployeeMessage(data):
        message = f"Новый сотрудник {data['full_name']}. Отдел {data['department']}," \
                  f" должность {data['position']}"
        SenderBots.new_employee_chat_bot.post_message(SenderBots.new_employee_channel_id, message)

    @staticmethod
    def sendAccessEmployeeMessage():
        message = f'Запрос от ... на следующие сервисы: ...'
        SenderBots.access_request_chat_bot.post_message(SenderBots.new_employee_channel_id, message)


if Sender.objects.first():
    SenderBots.updateBots()
