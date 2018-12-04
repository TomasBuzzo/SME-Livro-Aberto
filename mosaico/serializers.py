from functools import lru_cache

from django.db.models import Sum
from rest_framework import serializers

from budget_execution.models import Execucao


class GrupoSerializer(serializers.ModelSerializer):

    grupo_id = serializers.SerializerMethodField()
    grupo_nome = serializers.SerializerMethodField()
    orcado_total = serializers.SerializerMethodField()
    empenhado_total = serializers.SerializerMethodField()
    percentual_empenhado = serializers.SerializerMethodField()

    class Meta:
        model = Execucao
        fields = ('id', 'grupo_id', 'grupo_nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado')

    def get_grupo_id(self, obj):
        return obj.subgrupo.grupo_id

    def get_grupo_nome(self, obj):
        return obj.subgrupo.grupo.desc

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        return Execucao.objects.filter(
            year=obj.year, subgrupo__grupo_id=obj.subgrupo.grupo_id)

    @lru_cache(maxsize=10)
    def get_orcado_total(self, obj):
        execs = self._execucoes(obj)
        ret = execs.aggregate(total=Sum('orcado_atualizado'))
        return ret['total']

    @lru_cache(maxsize=10)
    def get_empenhado_total(self, obj):
        execs = self._execucoes(obj)
        ret = execs.aggregate(total=Sum('empenhado_liquido'))
        return ret['total']

    def get_percentual_empenhado(self, obj):
        orcado = self.get_orcado_total(obj)
        empenhado = self.get_empenhado_total(obj)

        if empenhado:
            return (empenhado * 100) / orcado
        else:
            return 0
