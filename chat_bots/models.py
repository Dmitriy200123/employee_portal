import datetime

from django.db import models


# Create your models here.

class BotType(models.Model):
    messenger_type = models.CharField(max_length=50)

    def __str__(self):
        return self.messenger_type


class ChatBot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Имя бота')
    botType = models.ForeignKey(BotType, on_delete=models.CASCADE, verbose_name='Тип бота')
    token = models.CharField(max_length=100, verbose_name='Токен')

    def __str__(self):
        return f'{self.botType}: {self.name}'


class Sender(models.Model):
    newEmployeeChatBot = models.ForeignKey(ChatBot, related_name='%(class)s_new_employee_chat_bot',
                                           on_delete=models.CASCADE, verbose_name="Бот для уведомлений о новом сотруднике")
    newEmployeeChannelId = models.CharField(max_length=50, verbose_name="Id канала для уведомлений о новом сотруднике")
    accessRequestChatBot = models.ForeignKey(ChatBot, related_name='%(class)s_access_request_chat_bot',
                                             on_delete=models.CASCADE, verbose_name="Бот для запроса доступа к сервисам")
    accessRequestChannelId = models.CharField(max_length=50, verbose_name="Id канала для запроса доступа к сервисам")
    sendTime = models.TimeField(default=datetime.datetime.now().replace(second=0, microsecond=0), verbose_name="Время отправки")

    def __str__(self):
        return f'{self.newEmployeeChatBot}, {self.accessRequestChatBot}'


class MessageToSend(models.Model):
    channel = models.CharField(max_length=50, verbose_name='Id канала')
    message = models.CharField(max_length=50, verbose_name='Текст сообщения')
    date = models.DateField(default=datetime.date.today, verbose_name='Дата отправки')
    time = models.TimeField(default=datetime.datetime.now().replace(second=0, microsecond=0), verbose_name='Время отправки')
    bot = models.ForeignKey(ChatBot, on_delete=models.CASCADE, verbose_name='Бот')
