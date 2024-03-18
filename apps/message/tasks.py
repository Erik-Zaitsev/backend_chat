from config.celery import app
from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from config.settings import EMAIL_HOST_USER


@shared_task
def send_message_at_email(request):
    send_mail(
        subject='Приветственное сообщение от Backend Chat',
        message='Поздравляю! Вы успешно зарегистрировались на сайте!',
        from_email=EMAIL_HOST_USER,
        recipient_list=[request.data.get('email'),],
        fail_silently=True,
    )
    print('Сообщение отправлено!')
    print(request.data.get('email'))
    return 'Done'
    