# Generated by Django 2.1.3 on 2018-11-28 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('from_to_handler', '0012_auto_20181128_1848'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dotacaofromto',
            old_name='group_description',
            new_name='group_desc',
        ),
        migrations.RenameField(
            model_name='dotacaofromto',
            old_name='subgroup_description',
            new_name='subgroup_desc',
        ),
        migrations.RenameField(
            model_name='gndfromto',
            old_name='elemento_description',
            new_name='elemento_desc',
        ),
        migrations.RenameField(
            model_name='gndfromto',
            old_name='gnd_description',
            new_name='gnd_desc',
        ),
        migrations.RenameField(
            model_name='gndfromto',
            old_name='new_gnd_description',
            new_name='new_gnd_desc',
        ),
        migrations.RenameField(
            model_name='subelementofromto',
            old_name='description',
            new_name='desc',
        ),
    ]
