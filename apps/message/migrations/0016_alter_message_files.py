# Generated by Django 4.2.8 on 2024-02-27 13:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0015_message_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to='files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['doc', 'txt', 'xlsx', 'pdf', 'jpg', 'png'])], verbose_name='Прикреплённые файлы'),
        ),
    ]
