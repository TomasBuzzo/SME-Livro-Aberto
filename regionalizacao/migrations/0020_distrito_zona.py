# Generated by Django 2.2.7 on 2019-11-27 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regionalizacao', '0019_auto_20191127_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='distrito',
            name='zona',
            field=models.CharField(max_length=6, null=True),
        ),
    ]