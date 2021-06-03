# Generated by Django 3.2 on 2021-05-23 06:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_bots', '0020_alter_messagetosend_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagetosend',
            name='bot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat_bots.chatbot', verbose_name='Бот'),
        ),
        migrations.AlterField(
            model_name='messagetosend',
            name='channel',
            field=models.CharField(max_length=50, verbose_name='Id канала'),
        ),
        migrations.AlterField(
            model_name='messagetosend',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата отправки'),
        ),
        migrations.AlterField(
            model_name='messagetosend',
            name='message',
            field=models.CharField(max_length=50, verbose_name='Текст сообщения'),
        ),
        migrations.AlterField(
            model_name='messagetosend',
            name='time',
            field=models.TimeField(default=datetime.datetime(2021, 5, 23, 11, 4), verbose_name='Время отправки'),
        ),
        migrations.AlterField(
            model_name='sender',
            name='accessRequestChannelId',
            field=models.CharField(max_length=50, verbose_name='Id канала для запроса доступа к сервисам'),
        ),
        migrations.AlterField(
            model_name='sender',
            name='accessRequestChatBot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_access_request_chat_bot', to='chat_bots.chatbot', verbose_name='Бот для запроса доступа к сервисам'),
        ),
        migrations.AlterField(
            model_name='sender',
            name='newEmployeeChannelId',
            field=models.CharField(max_length=50, verbose_name='Id канала для уведомлений о новом сотруднике'),
        ),
        migrations.AlterField(
            model_name='sender',
            name='newEmployeeChatBot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_new_employee_chat_bot', to='chat_bots.chatbot', verbose_name='Бот для уведомлений о новом сотруднике'),
        ),
        migrations.AlterField(
            model_name='sender',
            name='sendTime',
            field=models.TimeField(default=datetime.datetime(2021, 5, 23, 11, 4), verbose_name='Время отправки'),
        ),
    ]