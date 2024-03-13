from .celery import app
from time import sleep
from django.core.mail import send_mail


@app.task
def send_message_at_email():
    # sleep(10)
    send_mail('Соо')
    print('Сообщение отправлено!')