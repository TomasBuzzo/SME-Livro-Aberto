# Generated by Django 2.2 on 2019-04-18 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('from_to_handler', '0006_auto_20190214_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deflator',
            name='variation_percent',
        ),
    ]
