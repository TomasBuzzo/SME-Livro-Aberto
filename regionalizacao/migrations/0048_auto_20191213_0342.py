# Generated by Django 2.2.7 on 2019-12-13 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regionalizacao', '0047_auto_20191206_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distrito',
            name='zona',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
