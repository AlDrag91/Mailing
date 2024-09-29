from celery import shared_task

from django.core.mail import send_mail

from sending.models import Blasts, DeliveryAttempt

from django.utils import timezone

"""Отправка рассылки при создании"""


def start_sending(blasts):
    # now = timezone.now

    if blasts.start_datetime <= timezone.now() <= blasts.end_datetime:
        send_emails(blasts)
    elif blasts.start_datetime > timezone.now():
        schedule_sending(blasts)


"""Планировщик рассылок"""


@shared_task
def scheduled_send(mail_id):
    blasts = Blasts.objects.get(id=mail_id)
    send_emails(blasts)


def schedule_sending(blasts):
    scheduled_send.apply_async((blasts.id,), eta=blasts.start_datetime)


"""Функция отправки"""


def send_emails(blasts):
    attempt = DeliveryAttempt.objects.create(title=blasts)

    for email in blasts.email.all():
        try:
            response = send_mail("Рассылка с ресурса Mailing",
                                 f"Рассылка {blasts.title}",
                                 "Mailing",
                                 [email],
                                 fail_silently=False)
            if response.status_code == 200:
                attempt.attempt_status = 'успешно отправлено'
            else:
                raise Exception("Ошибка на стороне сервиса")  # Пример обработки ошибки

        except Exception as e:
            attempt.attempt_status = 'ошибка'
            attempt.error_message = str(e)
            break  # Первая ошибка завершает отправку

    attempt.save()
