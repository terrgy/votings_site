# Generated by Django 3.1.5 on 2021-01-29 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0007_auto_20210129_1651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersettings',
            name='image',
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.image'),
        ),
    ]