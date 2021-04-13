from chat_bots.models import ChatBot, Sender
from django import forms


class ChatBotForm(forms.ModelForm):
    class Meta:
        model = ChatBot
        fields = ('name', 'botType', 'token')


class SenderForm(forms.ModelForm):
    class Meta:
        model = Sender
        fields = ('newEmployeeChatBot', 'newEmployeeChannelId', 'accessRequestChatBot', 'accessRequestChannelId',
                  'sendTime')
