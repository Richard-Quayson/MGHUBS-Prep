# Generated by Django 5.0.2 on 2024-02-24 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='time',
            field=models.TimeField(default='00:00'),
            preserve_default=False,
        ),
    ]