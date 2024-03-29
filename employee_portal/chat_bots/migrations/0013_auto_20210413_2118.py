# Generated by Django 3.2 on 2021-04-13 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_bots', '0012_alter_sender_channelid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sender',
            name='channelId',
        ),
        migrations.AddField(
            model_name='sender',
            name='accessRequestChannelId',
            field=models.IntegerField(default=0, verbose_name='Id канала о запросе доступа'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sender',
            name='newEmployeeChannelId',
            field=models.IntegerField(default=0, verbose_name='Id канала о новом сотруднике'),
            preserve_default=False,
        ),
    ]
