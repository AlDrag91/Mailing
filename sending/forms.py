from django import forms

from sending.models import ClientService, Blasts, Message
from users.forms import FormMixin


class ClientServiceForm(FormMixin, forms.ModelForm):
    class Meta:
        model = ClientService
        fields = ('email', 'surname_name_patronymic', 'comment')


class BlastsForm(FormMixin, forms.ModelForm):
    email = forms.ModelMultipleChoiceField(queryset=ClientService.objects.all(), widget=forms.CheckboxSelectMultiple,
                                           label='выберите получателя')

    class Meta:
        model = Blasts
        fields = ('title', 'email', 'frequency', 'start_datetime', 'end_datetime', 'status')


class ManagerBlastsForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Blasts
        fields = ('status',)


class MessageForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'body')
