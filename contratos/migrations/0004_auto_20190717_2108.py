# Generated by Django 2.2.3 on 2019-07-17 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0003_empenhosofcache'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empenhosofcache',
            name='codProcesso',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
