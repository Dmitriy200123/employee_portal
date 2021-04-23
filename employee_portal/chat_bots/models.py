from django.db import models
import datetime


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
                                           on_delete=models.CASCADE, verbose_name="Бот нового сотрудника")
    newEmployeeChannelId = models.IntegerField(verbose_name="Id канала о новом сотруднике")
    accessRequestChatBot = models.ForeignKey(ChatBot, related_name='%(class)s_access_request_chat_bot',
                                             on_delete=models.CASCADE, verbose_name="Бот доступа к сервисам")
    accessRequestChannelId = models.IntegerField(verbose_name="Id канала о запросе доступа")
    sendTime = models.TimeField(verbose_name="Время отправки")

    def __str__(self):
        return f'{self.newEmployeeChatBot}, {self.accessRequestChatBot}'


class MessageToSend(models.Model):
    channel = models.CharField(max_length=50)
    message = models.CharField(max_length=50)
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(default=datetime.datetime.now().replace(second=0, microsecond=0))
    botType = models.ForeignKey(BotType, on_delete=models.CASCADE)
