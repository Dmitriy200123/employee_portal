# Generated by Django 3.2 on 2021-04-22 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_bots', '0014_messagetosend'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MessageToSend',
        ),
    ]
