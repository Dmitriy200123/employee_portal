# Generated by Django 3.2 on 2021-05-23 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_information_site', '0021_employeeservices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='is_new_employee',
            field=models.BooleanField(verbose_name='Я новый сотрудник'),
        ),
    ]
