from django import forms

from sending.models import ClientService, Blasts
from users.forms import FormMixin


class ClientServiceForm(FormMixin, forms.ModelForm):
    class Meta:
        model = ClientService
        fields = ('email', 'surname_name_patronymic', 'comment', 'company')


class BlastsForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Blasts
        fields = ('title', 'email', 'company', 'frequency')
