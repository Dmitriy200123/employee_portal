import datetime

from chat_bots.models import ChatBot, Sender, BotType, MessageToSend
from chat_bots.sender_bots import SenderBots
from django import forms


class ChatBotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChatBotForm, self).__init__(*args, **kwargs)
        self.fields['botType'].empty_label = 'Выберите тип бота'

    class Meta:
        model = ChatBot
        fields = ('name', 'botType', 'token')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_field', 'placeholder': 'Введите имя бота'}),
            'botType': forms.Select(choices=BotType.objects.all(),
                                    attrs={'class': 'form_field'}),
            'token': forms.TextInput(attrs={'class': 'form_field', 'placeholder': 'Введите токен бота'})
        }


class SenderForm(forms.ModelForm):
    class Meta:
        model = Sender
        fields = ('newEmployeeChatBot', 'newEmployeeChannelId', 'accessRequestChatBot', 'accessRequestChannelId',
                  'sendTime')
        widgets = {
            'newEmployeeChatBot': forms.Select(choices=ChatBot.objects.all(), attrs={'class': 'можно менять'}),
            'newEmployeeChannelId': forms.TextInput(attrs={'class': 'можно менять'}),
            'accessRequestChatBot': forms.Select(choices=ChatBot.objects.all(), attrs={'class': 'можно менять'}),
            'accessRequestChannelId': forms.TextInput(attrs={'class': 'можно менять'}),
            'sendTime': forms.TimeInput(attrs={'type': 'time', 'step': '60', 'class': 'можно менять'})
        }


class SendMessageForm(forms.ModelForm):
    class Meta:
        model = MessageToSend
        fields = '__all__'
        date = forms.DateField(input_formats=['%d-%m-%Y'])
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'edit'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'step': '60', 'class': 'edit'}),
        }

    def send_message(self):
        data = self.cleaned_data
        bot = SenderBots.createBot(data['bot'])
        time = datetime.datetime.combine(data['date'], data['time'])
        if datetime.datetime.now() > time + datetime.timedelta(minutes=1):
            return {'Result': 'Bad', 'Message': 'Time in past'}
        if datetime.datetime.now() < time:
            bot.post_scheduled_message(date=time, channel_id=data['channel'], message=data['message'])
        else:
            bot.post_message(channel_id=data['channel'], message=data['message'])
        return {'Result': 'Ok', 'Message': 'Ok'}
