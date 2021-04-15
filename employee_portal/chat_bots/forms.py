from chat_bots.models import ChatBot, Sender, BotType
from django import forms


class ChatBotForm(forms.ModelForm):
    class Meta:
        model = ChatBot
        fields = ('name', 'botType', 'token')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'test'}),
            'botType': forms.Select(choices=BotType.objects.all(), attrs={'class': 'test'}),
            'token': forms.TextInput(attrs={'class': 'test'})
        }


class SenderForm(forms.ModelForm):
    class Meta:
        model = Sender
        fields = ('newEmployeeChatBot', 'newEmployeeChannelId', 'accessRequestChatBot', 'accessRequestChannelId',
                  'sendTime')
