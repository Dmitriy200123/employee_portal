# Generated by Django 3.1.7 on 2021-03-12 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_information_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.ImageField(upload_to='employee_photos'),
        ),
    ]
