from chat_bots.models import ChatBot, MessageToSend
from django import forms
from telegram_bot.bot import TelegramBot
from slack_bot.bot import SlackBot
from django.db import models
import datetime

telegramBot = TelegramBot('1736332153:AAFb6_GN9SqZMSFa0aLqUAU6IM32nLaCZr8')
slackBot = SlackBot('xoxb-1918468674416-1907327567825-W1FsgXG3X0rxJLYnB203FRYU')


class ChatBotForm(forms.ModelForm):
    class Meta:
        model = ChatBot
        fields = ('name', 'botType', 'token')


class SendMessageForm(forms.ModelForm):
    class Meta:
        model = MessageToSend
        fields = '__all__'
        date = forms.DateField(input_formats=['%d-%m-%Y'])
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'step': '60'}),
        }

    def send_message(self):
        data = self.cleaned_data
        type = str(data['botType'])
        time = datetime.datetime.combine(data['date'], data['time'])
        bot = telegramBot
        if type == 'Slack':
            bot = slackBot
        if datetime.datetime.now() > time + datetime.timedelta(minutes=1):
            return {'Result': 'Bad', 'Message': 'Time in past'}
        if datetime.datetime.now() < time:
            bot.post_scheduled_message(date=time, channel_id=data['channel'], message=data['message'])
        else:
            bot.post_message(channel_id=data['channel'], message=data['message'])
        return {'Result': 'Ok', 'Message': 'Ok'}
