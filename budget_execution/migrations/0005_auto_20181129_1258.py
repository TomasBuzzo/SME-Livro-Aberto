# Generated by Django 2.1.3 on 2018-11-29 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget_execution', '0004_auto_20181129_0202'),
    ]

    operations = [
        migrations.CreateModel(
            name='FonteDeRecursoGrupo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='execucao',
            name='fonte_grupo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget_execution.FonteDeRecursoGrupo'),
        ),
    ]
