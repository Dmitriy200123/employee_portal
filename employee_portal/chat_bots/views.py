from chat_bots.forms import ChatBotForm, SenderForm, SendMessageForm
from chat_bots.models import ChatBot, Sender, MessageToSend
from chat_bots.sender_bots import MessengerType, SenderBots
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from employee_information_site.models import Employee
from slack_bot.bot import SlackBot
from telegram.error import InvalidToken
from telegram_bot.bot import TelegramBot


# Create your views here.

class ChatBotsListPage(ListView):
    template_name = 'chat_bots/chat_bots_setting_page.html'
    model = ChatBot

    def get_context_data(self, **kwargs):
        context = super(ChatBotsListPage, self).get_context_data(**kwargs)
        employee = Employee.objects.filter(user=self.request.user.id).first()
        context['current_user'] = employee
        return context


class AddChatBotPage(CreateView):
    template_name = 'chat_bots/add_chat_bot_page.html'
    model = ChatBot
    form_class = ChatBotForm
    success_url = reverse_lazy('chatBots:chatBotsSetting')

    def form_valid(self, form):
        if self.is_valid_token(form.cleaned_data['token'], form.cleaned_data['botType']):
            return super().form_valid(form)

        form.add_error('token', 'Недействительный токен')
        return super().form_invalid(form)

    @staticmethod
    def is_valid_token(token: str, bot_type):
        if bot_type.messenger_type == MessengerType.Telegram.name:
            try:
                bot = TelegramBot(token)
            except InvalidToken:
                return False

        else:
            try:
                bot = SlackBot(token)
            except Exception:
                return False

        return True

    def get_context_data(self, **kwargs):
        context = super(AddChatBotPage, self).get_context_data(**kwargs)
        employee = Employee.objects.filter(user=self.request.user.id).first()
        context['current_user'] = employee
        return context


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
        if AddChatBotPage.is_valid_token(form.cleaned_data['token'], form.cleaned_data['botType']):
            return super().form_valid(form)

        form.add_error('token', 'Недействительный токен')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateChatBotPage, self).get_context_data(**kwargs)
        current_user = Employee.objects.filter(user=self.request.user.id).first()
        context['current_user'] = current_user
        return context


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


class SenderSettingPage(ListView):
    model = Sender
    context_object_name = 'sender'
    template_name = 'chat_bots/sender_setting_page.html'

    def get_queryset(self):
        return super().get_queryset().first()

    def get(self, request, *args, **kwargs):
        if self.model.objects.all():
            return super().get(request, *args, **kwargs)

        return redirect('chatBots:updateSender')

    def get_context_data(self, **kwargs):
        context = super(SenderSettingPage, self).get_context_data(**kwargs)
        current_user = Employee.objects.filter(user=self.request.user.id).first()
        context['current_user'] = current_user
        return context


class UpdateOrCreateSenderPage(UpdateView):
    model = Sender
    form_class = SenderForm
    template_name = 'chat_bots/sender_update_or_create_page.html'
    success_url = reverse_lazy('chatBots:senderSetting')

    def get_object(self, **kwargs):
        return self.model.objects.first()

    def form_valid(self, form):
        SenderBots.updateBots()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateOrCreateSenderPage, self).get_context_data(**kwargs)
        current_user = Employee.objects.filter(user=self.request.user.id).first()
        context['current_user'] = current_user
        return context


class SendMessageView(FormView):
    template_name = 'chat_bots/send_message.html'
    form_class = SendMessageForm
    success_url = reverse_lazy('chatBots:chatBotsSetting')
    model = MessageToSend

    def form_valid(self, form):
        response = form.send_message()
        if response['Result'] == 'OK':
            return super().form_valid(form)
        else:
            form.add_error('date', response['Message'])
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(SendMessageView, self).get_context_data(**kwargs)
        current_user = Employee.objects.filter(user=self.request.user.id).first()
        context['current_user'] = current_user
        return context
