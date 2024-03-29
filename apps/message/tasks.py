from config.celery import app
from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from config.settings import EMAIL_HOST_USER


@app.task
def send_message_at_email(email):
    print('Сообщение отправлено!')

    send_mail(
        subject='Приветственное сообщение от Backend Chat2',
        message='Поздравляю! Вы успешно зарегистрировались на сайте!',
        from_email=EMAIL_HOST_USER,
        recipient_list=[email,],
        fail_silently=True,
    )

    print(email)
    return 'Done'
    