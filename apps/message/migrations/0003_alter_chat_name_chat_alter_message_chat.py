# Generated by Django 4.2.8 on 2024-02-12 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_alter_chat_options_alter_message_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='name_chat',
            field=models.CharField(max_length=100, verbose_name='Название чата'),
        ),
        migrations.AlterField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='message.chat', verbose_name='Чат'),
        ),
    ]