from django.shortcuts import render

# Create your views here.
import string

from random import random
import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView
from config import settings
from users.forms import UserRegisterForm, UserProfileForm, UserForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = '/users/success/'

    def form_valid(self, form):
        # Сохраняем форму перед отправкой письма
        user = form.save(commit=False)
        user.is_active = False  # Пользователь будет неактивным до подтверждения почты
        user.save()

        subject = 'Подтвердите ваш адрес электронной почты'
        message = 'Для завершения регистрации перейдите по ссылке: {0}/verify-email/?email={1}'.format(
            self.request.build_absolute_uri('/'), user.email)
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return super(RegisterView, self).form_valid(form)


class VerifyEmailView(View):

    def get(self, request):
        # Получаем из запроса параметр email (или другую информацию для идентификации пользователя)
        email = request.GET.get('email')
        # Находим пользователя в базе данных по полученному параметру
        user = User.objects.filter(email=email).first()
        user.is_active = True
        user.save()
        return HttpResponse('Email успешно подтвержден. Ваш аккаунт теперь активен.')


def generate_new_password(request):
    # Переход на страницу восстановления пароля
    context = {
        'title': 'Восстановление пароля'
    }
    return render(request, 'users/password_recovery.html', context)


def generate_random_password():
    # Генерация пароля
    length = 12
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


def password_recovery(request):
    # Контроллер изменение пароля и отправки его на почту
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = generate_random_password()
            user.password = make_password(new_password)
            user.save()

            send_mail(
                'Восстановление пароля в Mailing',
                f'Ваш новый пароль: {new_password}',
                'mailing.com',
                [email],
                fail_silently=False,
            )
            return HttpResponse(
                'Сброс пароля прошел успешно. Проверьте свою электронную почту на наличие нового пароля.')
        except User.DoesNotExist:
            return HttpResponse(
                'Указанная почта не зарегистрированная.')


class ProfileView(LoginRequiredMixin, UpdateView):
    # Профиль пользователя
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        clients_items = User.objects.all()
        context_data['users'] = clients_items
        context_data['title'] = 'Пользователи ресурса'
        return context_data


class UserCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = User
    permission_required = 'users.change_user'
    success_url = reverse_lazy('users:users')
    form_class = UserForm

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['title'] = 'Пользователи ресурса'
    #     return context_data
