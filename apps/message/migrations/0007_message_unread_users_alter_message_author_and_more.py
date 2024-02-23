# Generated by Django 4.2.8 on 2024-02-23 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0006_isreadmessage_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='unread_users',
            field=models.ManyToManyField(related_name='unread_users', to=settings.AUTH_USER_MODEL, verbose_name='Непрочитавшие пользователи'),
        ),
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель'),
        ),
        migrations.DeleteModel(
            name='IsReadMessage',
        ),
    ]
