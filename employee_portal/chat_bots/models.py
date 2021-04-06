import uuid

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
        return self.name
