# Generated by Django 2.2 on 2019-05-31 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget_execution', '0022_remove_orcamento_dt_data_loaded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empenho',
            name='dt_data_loaded',
        ),
        migrations.AddField(
            model_name='empenho',
            name='empenho_raw',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget_execution.EmpenhoRaw'),
        ),
    ]
