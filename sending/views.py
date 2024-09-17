from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from sending.forms import ClientServiceForm, BlastsForm, MessageForm, ManagerBlastsForm
from sending.management.commands.start_mailing import start_sending
from sending.models import ClientService, Blasts, Message, DeliveryAttempt


def index(request):
    """Решение для малого объема данных 3 случайных блога"""
    random_blog = Blog.objects.filter(is_published=True).order_by('?')[:3]
    clients_items = Blasts.objects.all()
    client_service = ClientService.objects.all()
    context = {'blog': random_blog}
    context['number_of_mailings'] = clients_items.count()
    context['status'] = Blasts.objects.filter(status='запущенный').count()
    context['client_service'] = client_service.count()

    return render(request, 'sending/home.html', context)


"""Контролеры работы с клиентами сервера"""


class ClientServiceListView(ListView):
    model = ClientService

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager').exists():
            clients_items = ClientService.objects.all()
        elif self.request.user.company:
            clients_items = ClientService.objects.filter(company=self.request.user)
        context_data['clients'] = clients_items
        context_data['title'] = 'Клиенты сервера'
        return context_data


class ClientServiceCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = ClientService
    form_class = ClientServiceForm
    permission_required = 'sending.add_clients'
    success_url = reverse_lazy('sending:clients')
    extra_context = {
        'button_name': 'Добавить',
        'title': 'Создание клиента сервера'
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.company = self.request.user
        return form


class ClientServiceUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = ClientService
    form_class = ClientServiceForm
    success_url = reverse_lazy('sending:clients')
    permission_required = 'sending.change_clients'
    extra_context = {
        'button_name': 'Изменить',
        'title': 'Изменение данных клиента сервера'
    }


class ClientServiceDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = ClientService
    success_url = reverse_lazy('sending:clients')
    permission_required = 'sending.delete_clients'
    extra_context = {
        'title': 'Удаление Клиента'
    }


"""Контролеры рассылок"""


class BlastsListView(ListView):
    model = Blasts

    def get_context_data(self, *args, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager').exists():
            clients_items = Blasts.objects.all()
            client_service = ClientService.objects.all()
        elif self.request.user.company:
            clients_items = Blasts.objects.filter(company=self.request.user)
            client_service = ClientService.objects.filter(company=self.request.user)
        contex_data['blasts'] = clients_items
        contex_data['title'] = 'Рассылки'
        contex_data['number_of_mailings'] = clients_items.count()
        contex_data['status'] = Blasts.objects.filter(status='запущенный').count()
        contex_data['client_service'] = client_service.count()
        return contex_data


class BlastsCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Blasts
    form_class = BlastsForm
    permission_required = 'sending.add_blasts'
    success_url = reverse_lazy('sending:blasts')
    extra_context = {
        'button_name': 'Создать',
        'title': 'Создание рассылки'
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.company = self.request.user
        return form

    for blast in Blasts.objects.all():
        start_sending(blast)


class BlastsUpdateView(LoginRequiredMixin, UpdateView):
    model = Blasts

    def get_form(self, form_class=None):

        if self.request.user.groups.filter(name='manager').exists():
            form_class = ManagerBlastsForm
            return form_class
        else:
            form_class = BlastsForm
            return form_class

    success_url = reverse_lazy('sending:blasts')
    extra_context = {
        'button_name': 'Подтвердить изменение',
        'title': 'Редактирование рассылки'
    }


class BlastsDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Blasts
    success_url = reverse_lazy('sending:blasts')
    permission_required = 'sending.delete_blasts'
    extra_context = {
        'title': 'Удаление рассылки'
    }


"""Контролеры сообщений"""


class MessageListView(ListView):
    model = Message

    def get_context_data(self, *args, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = 'Сообщение'
        if self.request.user.is_superuser:
            clients_items = Message.objects.all()
            contex_data['message'] = clients_items
            return contex_data
        elif self.request.user.company:
            clients_items = Message.objects.filter(user=self.request.user)
            contex_data['message'] = clients_items
            return contex_data


class MessageCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    permission_required = 'sending.add_message'
    success_url = reverse_lazy('sending:message')
    extra_context = {
        'button_name': 'Создать',
        'title': 'Создать сообщение'
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.user = self.request.user
        return form


class MessageUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = 'sending.change_message'
    success_url = reverse_lazy('sending:message')
    extra_context = {
        'button_name': 'Изменить',
        'title': 'Изменение сообщения'
    }


class MessageDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Message
    permission_required = 'sending.delete_message'
    success_url = reverse_lazy('sending:message')
    extra_context = {
        'title': 'Удаление сообщение'
    }


class DeliveryAttemptListView(ListView):
    model = DeliveryAttempt

    def get_context_data(self, *args, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        clients_items = DeliveryAttempt.objects.all()
        contex_data['DeliveryAttempt'] = clients_items
        contex_data['title'] = 'Отчет о рассылках'
        return contex_data
