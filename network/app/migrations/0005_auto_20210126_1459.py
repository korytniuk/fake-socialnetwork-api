# Generated by Django 3.1.5 on 2021-01-26 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_user_last_request_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='last_request_time',
            new_name='last_request',
        ),
    ]
