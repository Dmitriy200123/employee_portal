from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from . import views

app_name = 'chatBots'
urlpatterns = [
    path('setting/', staff_member_required(views.ChatBotsListPage.as_view()), name='chatBotsSetting'),
    path('add_chatbot/', staff_member_required(views.AddChatBotPage.as_view()), name='addChatBots'),
    path('update_chatbot/', staff_member_required(views.UpdateChatBotPage.as_view()), name='updateChatBot'),
    path('delete_chatbot/', staff_member_required(views.DeleteChatBotPage.as_view()), name='deleteChatBot'),
]
