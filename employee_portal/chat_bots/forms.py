from chat_bots.models import ChatBot
from django import forms


class ChatBotForm(forms.ModelForm):
    class Meta:
        model = ChatBot
        fields = ('name', 'botType', 'token')
