# Generated by Django 3.1.7 on 2021-03-24 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_information_site', '0008_auto_20210324_2116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['-department', 'position', 'full_name']},
        ),
    ]
