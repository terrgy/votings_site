# Generated by Django 3.1.5 on 2021-01-30 11:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0011_auto_20210130_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
