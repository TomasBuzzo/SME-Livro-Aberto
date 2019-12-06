# Generated by Django 2.2.7 on 2019-11-30 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regionalizacao', '0028_delete_recurso'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.FloatField()),
                ('label', models.CharField(blank=True, max_length=150, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recursos', to='regionalizacao.Escola')),
                ('subgrupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regionalizacao.Subgrupo')),
            ],
        ),
    ]