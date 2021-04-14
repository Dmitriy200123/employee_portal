# Generated by Django 3.2 on 2021-04-13 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_bots', '0010_merge_0008_alter_bottype_id_0009_auto_20210413_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='sender',
            name='channelId',
            field=models.IntegerField(default=0, verbose_name='Id канала'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sender',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]