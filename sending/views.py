from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from sending.forms import ClientServiceForm, BlastsForm
from sending.models import ClientService, Blasts


# Create your views here.
def index(requst):
    return render(requst, 'sending/home.html')


"""Контролеры работы с клиентами сервера"""


class ClientServiceListView(ListView):
    model = ClientService

    def get_context_data(self, *args, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        clients_items = ClientService.objects.all()
        contex_data['clients'] = clients_items
        contex_data['title'] = 'Клиенты сервера'
        return contex_data


class ClientServiceCreateView(LoginRequiredMixin, CreateView):
    model = ClientService
    form_class = ClientServiceForm
    success_url = reverse_lazy('sending:clients')
    extra_context = {
        'button_name': 'Добавить',
        'title': 'Создание клиента сервера'
    }


class ClientServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = ClientService
    form_class = ClientServiceForm
    success_url = reverse_lazy('sending:clients')
    extra_context = {
        'button_name': 'Изменить',
        'title': 'Изменение данных клиента сервера'
    }


class ClientServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = ClientService
    success_url = reverse_lazy('sending:clients')
    extra_context = {
        'title': 'Удаление Клиента'
    }


"""Контролеры рассылок"""


class BlastsListView(ListView):
    model = Blasts

    def get_context_data(self, *args, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        clients_items = Blasts.objects.all()
        contex_data['blasts'] = clients_items
        contex_data['title'] = 'Рассылки'
        return contex_data


class BlastsCreateView(LoginRequiredMixin, CreateView):
    model = Blasts
    form_class = BlastsForm
    success_url = reverse_lazy('sending:blasts')
    extra_context = {
        'button_name': 'Создать',
        'title': 'Создание рассылки'
    }


class BlastsDeleteView(LoginRequiredMixin, DeleteView):
    model = Blasts
    success_url = reverse_lazy('sending:blasts')
    extra_context = {
        'title': 'Удаление рассылки'
    }
