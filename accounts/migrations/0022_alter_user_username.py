# Generated by Django 3.2.7 on 2021-09-17 12:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_user_devices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=12, unique=True, validators=[django.core.validators.MinLengthValidator(6)]),
        ),
    ]
