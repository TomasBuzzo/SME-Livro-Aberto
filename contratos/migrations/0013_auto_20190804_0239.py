# Generated by Django 2.2.3 on 2019-08-04 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0012_auto_20190803_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratoraw',
            name='valaditamentos',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contratoraw',
            name='valanulacao',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contratoraw',
            name='valanuladoempenho',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contratoraw',
            name='valempenhadoliquido',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contratoraw',
            name='valliquidado',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contratoraw',
            name='valpago',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contratoraw',
            name='valprincipal',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contratoraw',
            name='valreajustes',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contratoraw',
            name='valtotalempenhado',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
