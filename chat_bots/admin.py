from chat_bots.models import ChatBot, BotType, Sender, MessageToSend
from django.contrib import admin

# Register your models here.

admin.site.register(BotType)
admin.site.register(ChatBot)
admin.site.register(Sender)
admin.site.register(MessageToSend)