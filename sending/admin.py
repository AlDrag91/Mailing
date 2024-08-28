from django.contrib import admin

from sending.models import ClientService, Blasts, Message, DeliveryAttempt


# Register your models here.
@admin.register(ClientService)
class ClientServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'surname_name_patronymic', 'comment', 'company')


@admin.register(Blasts)
class BlastsAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'frequency', 'status', 'company', 'email', 'title')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')


@admin.register(DeliveryAttempt)
class DeliveryAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt_datetime', 'attempt_status', 'mail_server_response', 'email', 'title')
