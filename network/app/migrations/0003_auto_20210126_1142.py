# Generated by Django 3.1.5 on 2021-01-26 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210125_1838'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('liked_post', 'user')},
        ),
    ]
