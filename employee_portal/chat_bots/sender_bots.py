import enum

from chat_bots.models import Sender
from slack_bot.bot import SlackBot
from telegram_bot.bot import TelegramBot


class ChatBotType(enum.Enum):
    NewEmployeeBot = 1
    AccessRequestBot = 2


class MessengerType(enum.Enum):
    Telegram = 'Telegram'
    Slack = 'Slack'


def createAccessRequestBot(chat_bot):
    if chat_bot.botType.messenger_type == MessengerType.Telegram.name:
        return TelegramBot(chat_bot.token)

    if chat_bot.botType.messenger_type == MessengerType.Slack.name:
        return SlackBot(chat_bot.token)


def createNewEmployeeBot(chat_bot):
    if chat_bot.botType.messenger_type == MessengerType.Telegram.name:
        return TelegramBot(chat_bot.token)

    if chat_bot.botType.messenger_type == MessengerType.Slack.name:
        return SlackBot(chat_bot.token)


class SenderBots:
    sender = Sender.objects.first()
    new_employee_channel_id = sender.newEmployeeChannelId
    new_employee_chat_bot = createNewEmployeeBot(sender.newEmployeeChatBot)
    access_request_channel_id = sender.accessRequestChannelId
    access_request_chat_bot = createAccessRequestBot(sender.accessRequestChatBot)

    @staticmethod
    def sendNewEmployeeMessage(data):
        message = f"Новый сотрудник {data['full_name']}. Отдел {data['department']}," \
                  f" должность {data['position']}"
        SenderBots.new_employee_chat_bot.post_message(SenderBots.new_employee_channel_id, message)

    @staticmethod
    def sendAccessEmployeeMessage():
        message = f'Запрос от ... на следующие сервисы: ...'
        SenderBots.access_request_chat_bot.post_message(SenderBots.new_employee_channel_id, message)

    '''def updateBots(self):
        sender = Sender.objects.first()
        employee_chat_bot = sender.newEmployeeChatBot
        access_chat_bot = sender.accessRequestChatBot
        self.createBot(employee_chat_bot, sender.newEmployeeChannelId, ChatBotType.NewEmployeeBot)
        self.createBot(access_chat_bot, sender.accessRequestChannelId, ChatBotType.AccessRequestBot)

    def createBot(self, chat_bot, channel_id, chat_bot_type):
        if chat_bot_type == ChatBotType.NewEmployeeBot:
            self.createNewEmployeeBot(chat_bot, channel_id)

        if chat_bot_type == ChatBotType.AccessRequestBot:
            self.createAccessRequestBot(chat_bot, channel_id)'''
