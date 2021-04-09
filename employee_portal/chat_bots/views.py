from chat_bots.forms import ChatBotForm
from chat_bots.models import ChatBot
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


# Create your views here.

class ChatBotsListPage(ListView):
    template_name = 'chat_bots/chat_bots_setting_page.html'
    model = ChatBot


class AddChatBotPage(CreateView):
    template_name = 'chat_bots/add_chat_bot_page.html'
    model = ChatBot
    form_class = ChatBotForm
    success_url = reverse_lazy('chatBots:chatBotsSetting')

    def form_valid(self, form):
        if self.is_valid_token(form.cleaned_data['token']):
            return super().form_valid(form)

        form.add_error('token', 'Недействительный токен')
        return super().form_invalid(form)

    @staticmethod
    def is_valid_token(token: str):
        # ToDO: Make token validation
        return True


class UpdateChatBotPage(UpdateView):
    template_name = 'chat_bots/add_chat_bot_page.html'
    model = ChatBot
    form_class = ChatBotForm
    context_object_name = 'chatBot'
    success_url = reverse_lazy('chatBots:chatBotsSetting')
    argument = 'id'

    def get_object(self, **kwargs):
        parameters = self.request.GET
        id_value = parameters[self.argument] if self.argument in parameters and parameters[
            self.argument].isdigit() else None
        return get_object_or_404(self.model, id=id_value)

    def form_valid(self, form):
        if AddChatBotPage.is_valid_token(form.cleaned_data['token']):
            return super().form_valid(form)

        form.add_error('token', 'Недействительный токен')
        return super().form_invalid(form)


class DeleteChatBotPage(DeleteView):
    model = ChatBot
    context_object_name = 'chatBot'
    success_url = reverse_lazy('chatBots:chatBotsSetting')
    argument = 'id'

    def get_object(self, **kwargs):
        parameters = self.request.POST
        id_value = parameters[self.argument] if self.argument in parameters and parameters[
            self.argument].isdigit() else None
        return get_object_or_404(self.model, id=id_value)
