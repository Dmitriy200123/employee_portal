# Generated by Django 3.2 on 2021-04-24 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_information_site', '0020_delete_employeeservices'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='employee_information_site.employee')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='employee_information_site.service')),
            ],
        ),
    ]
