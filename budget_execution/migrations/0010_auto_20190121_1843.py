# Generated by Django 2.1.5 on 2019-01-21 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget_execution', '0009_auto_20190110_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empenho',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cd_key', models.TextField(blank=True, null=True)),
                ('an_empenho', models.BigIntegerField(blank=True, null=True)),
                ('cd_categoria', models.BigIntegerField(blank=True, null=True)),
                ('cd_elemento', models.TextField(blank=True, null=True)),
                ('cd_empenho', models.BigIntegerField(blank=True, null=True)),
                ('cd_empresa', models.TextField(blank=True, null=True)),
                ('cd_fonte_de_recurso', models.TextField(blank=True, null=True)),
                ('cd_funcao', models.TextField(blank=True, null=True)),
                ('cd_grupo', models.BigIntegerField(blank=True, null=True)),
                ('cd_item_despesa', models.TextField(blank=True, null=True)),
                ('cd_modalidade', models.BigIntegerField(blank=True, null=True)),
                ('cd_orgao', models.TextField(blank=True, null=True)),
                ('cd_programa', models.TextField(blank=True, null=True)),
                ('cd_projeto_atividade', models.TextField(blank=True, null=True)),
                ('cd_subelemento', models.TextField(blank=True, null=True)),
                ('cd_subfuncao', models.TextField(blank=True, null=True)),
                ('cd_unidade', models.TextField(blank=True, null=True)),
                ('dt_empenho', models.DateTimeField(blank=True, null=True)),
                ('mes_empenho', models.BigIntegerField(blank=True, null=True)),
                ('nm_empresa', models.TextField(blank=True, null=True)),
                ('dc_cpf_cnpj', models.TextField(blank=True, null=True)),
                ('cd_reserva', models.BigIntegerField(blank=True, null=True)),
                ('dc_categoria_economica', models.TextField(blank=True, null=True)),
                ('dc_elemento', models.TextField(blank=True, null=True)),
                ('dc_fonte_de_recurso', models.TextField(blank=True, null=True)),
                ('dc_funcao', models.TextField(blank=True, null=True)),
                ('dc_item_despesa', models.TextField(blank=True, null=True)),
                ('dc_orgao', models.TextField(blank=True, null=True)),
                ('dc_programa', models.TextField(blank=True, null=True)),
                ('dc_projeto_atividade', models.TextField(blank=True, null=True)),
                ('dc_subelemento', models.TextField(blank=True, null=True)),
                ('dc_subfuncao', models.TextField(blank=True, null=True)),
                ('dc_unidade', models.TextField(blank=True, null=True)),
                ('dc_grupo_despesa', models.TextField(blank=True, null=True)),
                ('dc_modalidade', models.TextField(blank=True, null=True)),
                ('dc_razao_social', models.TextField(blank=True, null=True)),
                ('vl_empenho_anulado', models.FloatField(blank=True, null=True)),
                ('vl_empenho_liquido', models.FloatField(blank=True, null=True)),
                ('vl_liquidado', models.FloatField(blank=True, null=True)),
                ('vl_pago', models.FloatField(blank=True, null=True)),
                ('vl_pago_restos', models.BigIntegerField(blank=True, null=True)),
                ('vl_empenhado', models.FloatField(blank=True, null=True)),
                ('dt_data_loaded', models.DateTimeField(auto_now_add=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget_execution.Execucao')),
            ],
            options={
                'db_table': 'empenhos',
            },
        ),
        migrations.CreateModel(
            name='Orcamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cd_key', models.TextField(blank=True, null=True)),
                ('dt_inicial', models.DateTimeField(blank=True, null=True)),
                ('dt_final', models.DateTimeField(blank=True, null=True)),
                ('cd_ano_execucao', models.BigIntegerField(blank=True, null=True)),
                ('cd_exercicio', models.BigIntegerField(blank=True, null=True)),
                ('nm_administracao', models.TextField(blank=True, null=True)),
                ('cd_exercicio_empresa_id', models.BigIntegerField(blank=True, null=True)),
                ('cd_orgao', models.BigIntegerField(blank=True, null=True)),
                ('sg_orgao', models.TextField(blank=True, null=True)),
                ('ds_orgao', models.TextField(blank=True, null=True)),
                ('cd_unidade', models.BigIntegerField(blank=True, null=True)),
                ('ds_unidade', models.TextField(blank=True, null=True)),
                ('cd_funcao', models.BigIntegerField(blank=True, null=True)),
                ('ds_funcao', models.TextField(blank=True, null=True)),
                ('cd_subfuncao', models.BigIntegerField(blank=True, null=True)),
                ('ds_subfuncao', models.TextField(blank=True, null=True)),
                ('cd_programa', models.BigIntegerField(blank=True, null=True)),
                ('ds_programa', models.TextField(blank=True, null=True)),
                ('tp_projeto_atividade', models.TextField(blank=True, null=True)),
                ('tp_papa', models.TextField(blank=True, null=True)),
                ('cd_projeto_atividade', models.BigIntegerField(blank=True, null=True)),
                ('ds_projeto_atividade', models.TextField(blank=True, null=True)),
                ('cd_despesa', models.BigIntegerField(blank=True, null=True)),
                ('ds_despesa', models.TextField(blank=True, null=True)),
                ('ds_categoria_despesa', models.BigIntegerField(blank=True, null=True)),
                ('ds_categoria', models.TextField(blank=True, null=True)),
                ('cd_grupo_despesa', models.BigIntegerField(blank=True, null=True)),
                ('ds_grupo_despesa', models.TextField(blank=True, null=True)),
                ('cd_modalidade', models.BigIntegerField(blank=True, null=True)),
                ('ds_modalidade', models.TextField(blank=True, null=True)),
                ('cd_elemento', models.BigIntegerField(blank=True, null=True)),
                ('cd_fonte', models.BigIntegerField(blank=True, null=True)),
                ('ds_fonte', models.TextField(blank=True, null=True)),
                ('vl_orcado_inicial', models.BigIntegerField(blank=True, null=True)),
                ('vl_orcado_atualizado', models.FloatField(blank=True, null=True)),
                ('vl_congelado', models.FloatField(blank=True, null=True)),
                ('vl_orcado_disponivel', models.FloatField(blank=True, null=True)),
                ('vl_reservado_liquido', models.FloatField(blank=True, null=True)),
                ('vl_empenhado_liquido', models.FloatField(blank=True, null=True)),
                ('vl_empenhado_liquido_atual', models.FloatField(blank=True, null=True)),
                ('vl_liquidado', models.FloatField(blank=True, null=True)),
                ('vl_liquidado_atual', models.FloatField(blank=True, null=True)),
                ('vl_pago', models.FloatField(blank=True, null=True)),
                ('vl_pago_atual', models.FloatField(blank=True, null=True)),
                ('vl_saldo_empenho', models.FloatField(blank=True, null=True)),
                ('vl_saldo_reserva', models.FloatField(blank=True, null=True)),
                ('vl_saldo_dotacao', models.FloatField(blank=True, null=True)),
                ('dt_extracao', models.DateTimeField(blank=True, null=True)),
                ('dt_data_loaded', models.DateTimeField(auto_now_add=True)),
                ('execucao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget_execution.Execucao')),
            ],
            options={
                'db_table': 'orcamento',
            },
        ),
        migrations.AlterField(
            model_name='categoria',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='elemento',
            name='desc',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='fontederecurso',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='gnd',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='modalidade',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='orgao',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='orgao',
            name='initials',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='programa',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='projetoatividade',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='projetoatividade',
            name='type',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='subelemento',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='subfuncao',
            name='desc',
            field=models.TextField(),
        ),
    ]
