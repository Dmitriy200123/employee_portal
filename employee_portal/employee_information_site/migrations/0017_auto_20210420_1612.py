# Generated by Django 3.2 on 2021-04-20 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_information_site', '0016_auto_20210420_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='photo',
            field=models.ImageField(default='skb_lab.jpg', upload_to='employee_photos', verbose_name='Фотография'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.ImageField(default='skb_lab.jpg', upload_to='employee_photos', verbose_name='Фотография'),
        ),
    ]
