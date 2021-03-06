# Generated by Django 2.2.3 on 2019-08-02 15:43

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0007_contratocategoriafromto'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContratoCategoriaFromToSpreadsheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spreadsheet', models.FileField(upload_to='contratos/contratos_categoria_spreadsheets', verbose_name='Planilha')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('extracted', models.BooleanField(default=False, editable=False)),
                ('added_fromtos', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=28), editable=False, null=True, size=None)),
                ('not_added_fromtos', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=28), editable=False, null=True, size=None)),
            ],
            options={
                'verbose_name': 'Planilha De-Para: Contratos Categorias',
                'verbose_name_plural': 'Planilha De-Para: Contratos Categorias',
            },
        ),
    ]
