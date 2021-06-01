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
    def __init__(self, *args, **kwargs):
        super(SenderForm, self).__init__(*args, **kwargs)
        self.fields['newEmployeeChatBot'].empty_label = 'Выберите бота'
        self.fields['accessRequestChatBot'].empty_label = 'Выберите бота'

    class Meta:
        model = Sender
        fields = ('newEmployeeChatBot', 'newEmployeeChannelId', 'accessRequestChatBot', 'accessRequestChannelId',
                  'sendTime')
        widgets = {
            'newEmployeeChatBot': forms.Select(choices=ChatBot.objects.all(), attrs={'class': 'setting_parameter'}),
            'newEmployeeChannelId': forms.TextInput(attrs={'class': 'setting_parameter', 'placeholder': '@channel'}),
            'accessRequestChatBot': forms.Select(choices=ChatBot.objects.all(), attrs={'class': 'setting_parameter'}),
            'accessRequestChannelId': forms.TextInput(attrs={'class': 'setting_parameter', 'placeholder': '@channel'}),
            'sendTime': forms.TimeInput(attrs={'type': 'time', 'step': '60', 'class': 'setting_parameter'})
        }


class SendMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SendMessageForm, self).__init__(*args, **kwargs)
        self.fields['bot'].empty_label = 'Выберите бота'

    class Meta:
        model = MessageToSend
        fields = '__all__'
        date = forms.DateField(input_formats=['%d-%m-%Y'])
        widgets = {
            'bot': forms.Select(choices=MessageToSend.objects.all(), attrs={'class': 'message_sending_parameter bot'}),
            'channel': forms.TextInput(attrs={'class': 'message_sending_parameter channel', 'placeholder': '@channel'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'message_sending_parameter date'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'step': '60', 'class': 'message_sending_parameter time'}),
            'message': forms.Textarea(attrs={'class': 'message_sending_parameter message', 'placeholder': 'Введите сообщение'})
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
