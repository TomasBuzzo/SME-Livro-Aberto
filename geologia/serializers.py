from datetime import date
from decimal import Decimal
from django.db.models import Sum
from rest_framework import serializers

from budget_execution.models import Execucao, GndGeologia, Subfuncao
from from_to_handler.models import Deflator
from geologia.exceptions import InvalidChartOptionException


class GndGeologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GndGeologia
        fields = ('desc', 'slug')


class SubfuncaoSerializer(serializers.ModelSerializer):
    selecionado = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.subfuncao_id = kwargs.pop('subfuncao_id', False)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Subfuncao
        fields = ('id', 'desc', 'selecionado')

    def get_selecionado(self, obj):
        param = self.subfuncao_id
        return param and obj.id == int(param)


class GeologiaSerializer:

    def __init__(self, queryset, subfuncao_id=None, *args, **kwargs):
        self.queryset = queryset
        self._subfuncao_id = int(subfuncao_id) if subfuncao_id else subfuncao_id

    @property
    def data(self):
        return {
            'camadas': self.prepare_data(),
            'subfuncao': self.prepare_data(subfuncao_id=self._subfuncao_id),
            'subgrupo': self.prepare_subgrupo_data(),
            'gnds': GndGeologiaSerializer(
                GndGeologia.objects.all().order_by('desc'), many=True).data,
            'subfuncoes': self.prepare_subfuncoes(),
            'dt_updated': Execucao.objects.get_date_updated(),
        }

    # Charts 1 and 2 (camadas and subfuncao)
    def prepare_data(self, subfuncao_id=None):
        qs = self.queryset

        ret = {
            'orcado': [],
            'empenhado': [],
        }

        # filtering for chart 2 (by subfuncao)
        if subfuncao_id:
            qs = qs.filter(subfuncao_id=subfuncao_id)
            ret['subfuncao_id'] = subfuncao_id

        years = qs.order_by('year').values('year').distinct()

        for year_dict in years:
            year = year_dict['year']
            year_qs = qs.filter(year=year)

            ret['orcado'].append(self._get_orcado_data_by_year(year_qs))
            ret['empenhado'].append(self._get_empenhado_data_by_year(year_qs))

        return ret

    def _get_orcado_data_by_year(self, qs):
        year = qs[0].year

        orcado_by_gnd = qs.values('gnd_geologia__desc', 'gnd_geologia__slug') \
            .annotate(orcado=Sum('orcado_atualizado'))
        orcado_total = qs.aggregate(total=Sum('orcado_atualizado'))
        orcado_total = deflate(orcado_total['total'], year)

        orcado_gnds = self._get_orcado_gnds_list(orcado_by_gnd, orcado_total,
                                                 year)

        return {
            "year": year.strftime("%Y"),
            "total": orcado_total,
            "gnds": orcado_gnds,
        }

    def _get_empenhado_data_by_year(self, qs):
        year = qs[0].year

        empenhado_by_gnd = qs \
            .values('gnd_geologia__desc', 'gnd_geologia__slug') \
            .annotate(empenhado=Sum('empenhado_liquido')) \
            .order_by('gnd_geologia__desc')
        empenhado_total = qs.aggregate(total=Sum('empenhado_liquido'))
        empenhado_total = deflate(empenhado_total['total'], year)

        empenhado_gnds = self._get_empenhado_gnds_list(
            empenhado_by_gnd, empenhado_total, year)

        return {
            "year": year.strftime("%Y"),
            "total": empenhado_total,
            "gnds": empenhado_gnds,
        }

    # Chart 3: Subgrupo
    def prepare_subgrupo_data(self):
        qs = self.queryset.filter(year__year__gte=2010,
                                  subgrupo__isnull=False)

        years = qs.order_by('year').values('year').distinct()

        ret = {
            'orcado': [],
            'empenhado': [],
        }
        for year_dict in years:
            year = year_dict['year']
            year_qs = qs.filter(year=year)

            ret['orcado'].append(self.get_subgrupo_year_orcado_data(year_qs))
            ret['empenhado'].append(
                self.get_subgrupo_year_empenhado_data(year_qs))

        return ret

    def get_subgrupo_year_orcado_data(self, qs):
        year = qs[0].year
        subgrupos = qs.order_by('subgrupo__desc').values('subgrupo_id') \
            .distinct()

        ret = {
            'year': year.strftime('%Y'),
            'subgrupos': [],
        }

        for subgrupo in subgrupos:
            qs_subgrupo = qs.filter(subgrupo=subgrupo['subgrupo_id'])
            ret['subgrupos'].append(
                self.get_subgrupo_orcado_data(qs_subgrupo))

        return ret

    def get_subgrupo_year_empenhado_data(self, qs):
        year = qs[0].year
        subgrupos = qs.order_by('subgrupo__desc').values('subgrupo_id') \
            .distinct()

        ret = {
            'year': year.strftime('%Y'),
            'subgrupos': [],
        }

        for subgrupo in subgrupos:
            qs_subgrupo = qs.filter(subgrupo=subgrupo['subgrupo_id'])
            ret['subgrupos'].append(
                self.get_subgrupo_empenhado_data(qs_subgrupo))

        return ret

    def get_subgrupo_orcado_data(self, qs):
        subgrupo = qs[0].subgrupo
        year = qs[0].year

        orcado_by_gnd = qs.values('gnd_geologia__desc', 'gnd_geologia__slug') \
            .annotate(orcado=Sum('orcado_atualizado'))
        orcado_total = qs.aggregate(total=Sum('orcado_atualizado'))
        orcado_total = deflate(orcado_total['total'], year)

        orcado_gnds = self._get_orcado_gnds_list(orcado_by_gnd, orcado_total,
                                                 year)

        return {
            "subgrupo": subgrupo.desc,
            "total": orcado_total,
            "gnds": orcado_gnds,
        }

    def get_subgrupo_empenhado_data(self, qs):
        subgrupo = qs[0].subgrupo
        year = qs[0].year

        empenhado_by_gnd = qs \
            .values('gnd_geologia__desc', 'gnd_geologia__slug') \
            .annotate(empenhado=Sum('empenhado_liquido'))
        empenhado_total = qs.aggregate(total=Sum('empenhado_liquido'))
        empenhado_total = deflate(empenhado_total['total'], year)

        empenhado_gnds = self._get_empenhado_gnds_list(
            empenhado_by_gnd, empenhado_total, year)

        return {
            "subgrupo": subgrupo.desc,
            "total": empenhado_total,
            "gnds": empenhado_gnds,
        }

    def _get_orcado_gnds_list(self, orcado_by_gnd, orcado_total, year):
        ret = []
        for gnd in orcado_by_gnd:
            orcado = deflate(gnd['orcado'], year)
            gnd_dict = {
                "name": gnd['gnd_geologia__desc'],
                "slug": gnd['gnd_geologia__slug'],
                "value": orcado,
                "percent": calculate_percent(
                    orcado, orcado_total)
            }
            ret.append(gnd_dict)

        return ret

    def _get_empenhado_gnds_list(self, empenhado_by_gnd, empenhado_total, year):
        ret = []
        for gnd in empenhado_by_gnd:
            empenhado = deflate(gnd['empenhado'], year)
            gnd_dict = {
                "name": gnd['gnd_geologia__desc'],
                "slug": gnd['gnd_geologia__slug'],
                "value": empenhado,
                "percent": calculate_percent(
                    empenhado, empenhado_total)
            }
            ret.append(gnd_dict)

        return ret

    def _calculate_percent(self, value, total):
        if value is None or not total:
            return 0
        return value / total

    def prepare_subfuncoes(self):
        # We need to get the subfuncoes from the execucoes queryset because
        # there's no way to tell which subfuncoes are from SME and which aren't.
        # Only the Execucao model has a fk to Orgao.
        subfuncoes = [execucao.subfuncao
                      for execucao in self.queryset.distinct('subfuncao')]
        subfuncoes.sort(key=lambda s: s.desc)

        return SubfuncaoSerializer(subfuncoes, subfuncao_id=self._subfuncao_id,
                                   many=True).data


class GeologiaDownloadSerializer:

    def __init__(self, queryset, chart, subfuncao_id=None, *args, **kwargs):
        self.queryset = queryset
        self.chart = chart
        self.subfuncao_id = int(subfuncao_id) if subfuncao_id else subfuncao_id

    @property
    def data(self):
        if self.chart == 'camadas':
            return self.prepare_camadas_chart_data()
        elif self.chart == 'subfuncao':
            return self.prepare_subfuncao_chart_data()
        elif self.chart == 'subgrupo':
            return self.prepare_subgrupo_chart_data()
        else:
            raise InvalidChartOptionException

    def prepare_camadas_chart_data(self):
        qs = self.queryset.order_by('year')

        data_by_gnd = qs.values('gnd_geologia__desc', 'year__year') \
            .annotate(orcado=Sum('orcado_atualizado')) \
            .annotate(empenhado=Sum('empenhado_liquido'))

        orcado_values = qs.values('year__year') \
            .annotate(total=Sum('orcado_atualizado'))
        orcado_total = {v['year__year']: v['total'] for v in orcado_values}

        empenhado_values = qs.values('year__year') \
            .annotate(total=Sum('empenhado_liquido'))
        empenhado_total = {v['year__year']: v['total']
                           for v in empenhado_values}

        return self._get_gnds_list_by_year(data_by_gnd, orcado_total,
                                           empenhado_total)

    def prepare_subfuncao_chart_data(self):
        qs = self.queryset

        if self.subfuncao_id:
            qs = qs.filter(subfuncao_id=self.subfuncao_id)

        subfuncoes = qs.order_by('subfuncao_id').values('subfuncao_id') \
            .distinct()
        ret = []
        for subfuncao in subfuncoes:
            qs_subfuncao = qs.filter(subfuncao=subfuncao['subfuncao_id'])
            ret += self._get_subfuncao_values(qs_subfuncao)

        return ret

    def _get_subfuncao_values(self, queryset):
        qs = queryset.order_by('year')

        data_by_gnd = qs.values('gnd_geologia__desc', 'year__year',
                                'subfuncao__desc') \
            .annotate(orcado=Sum('orcado_atualizado')) \
            .annotate(empenhado=Sum('empenhado_liquido'))

        orcado_values = qs.values('year__year') \
            .annotate(total=Sum('orcado_atualizado'))
        orcado_total = {v['year__year']: v['total'] for v in orcado_values}

        empenhado_values = qs.values('year__year') \
            .annotate(total=Sum('empenhado_liquido'))
        empenhado_total = {v['year__year']: v['total']
                           for v in empenhado_values}

        return self._get_gnds_list_by_year(data_by_gnd, orcado_total,
                                           empenhado_total)

    def _get_gnds_list_by_year(self, data_by_gnd, orcado_total_by_year,
                               empenhado_total_by_year):
        ret = []
        for gnd in data_by_gnd:
            year = gnd['year__year']
            year_date = date(year, 1, 1)

            orcado = deflate(gnd['orcado'], year_date)
            empenhado = deflate(gnd['empenhado'], year_date)

            orcado_total = orcado_total_by_year[year]
            orcado_total = deflate(orcado_total, year_date)

            empenhado_total = empenhado_total_by_year[year]
            empenhado_total = deflate(empenhado_total, year_date)

            gnd_dict = {
                "ano": year,
                "gnd": gnd['gnd_geologia__desc'],
                "orcado": orcado,
                "orcado_total": orcado_total,
                "orcado_percentual": calculate_percent(
                    orcado, orcado_total),
                "empenhado": empenhado,
                "empenhado_total": empenhado_total,
                "empenhado_percentual": calculate_percent(
                    empenhado, empenhado_total),
            }
            if 'subfuncao__desc' in gnd:
                gnd_dict["subfuncao"] = gnd['subfuncao__desc']

            ret.append(gnd_dict)

        return ret

    def prepare_subgrupo_chart_data(self):
        qs = self.queryset.filter(year__year__gte=2010,
                                  subgrupo__isnull=False)

        years = qs.order_by('year').values('year').distinct()
        ret = []
        for year_dict in years:
            year = year_dict['year']
            year_qs = qs.filter(year=year)
            ret += self._get_subgrupo_values(year_qs)

        return ret

    def _get_subgrupo_values(self, queryset):
        qs = queryset.order_by('subgrupo_id')

        data_by_gnd = qs.values('gnd_geologia__desc', 'year__year',
                                'subgrupo_id', 'subgrupo__desc') \
            .annotate(orcado=Sum('orcado_atualizado')) \
            .annotate(empenhado=Sum('empenhado_liquido'))

        orcado_values = qs.values('subgrupo_id') \
            .annotate(total=Sum('orcado_atualizado'))
        orcado_total = {v['subgrupo_id']: v['total'] for v in orcado_values}

        empenhado_values = qs.values('subgrupo_id') \
            .annotate(total=Sum('empenhado_liquido'))
        empenhado_total = {v['subgrupo_id']: v['total']
                           for v in empenhado_values}

        return self._get_gnds_list_by_subgrupo(data_by_gnd, orcado_total,
                                               empenhado_total)

    def _get_gnds_list_by_subgrupo(self, data_by_gnd, orcado_total_by_subgrupo,
                                   empenhado_total_by_subgrupo):
        ret = []
        for gnd in data_by_gnd:
            subgrupo_id = gnd['subgrupo_id']
            year = gnd['year__year']
            year_date = date(year, 1, 1)

            orcado = deflate(gnd['orcado'], year_date)
            empenhado = deflate(gnd['empenhado'], year_date)

            orcado_total = orcado_total_by_subgrupo[subgrupo_id]
            orcado_total = deflate(orcado_total, year_date)

            empenhado_total = empenhado_total_by_subgrupo[subgrupo_id]
            empenhado_total = deflate(empenhado_total, year_date)

            ret.append({
                "ano": year,
                "gnd": gnd['gnd_geologia__desc'],
                "subgrupo": gnd['subgrupo__desc'],
                "orcado": orcado,
                "orcado_total": orcado_total,
                "orcado_percentual": calculate_percent(
                    orcado, orcado_total),
                "empenhado": empenhado,
                "empenhado_total": empenhado_total,
                "empenhado_percentual": calculate_percent(
                    empenhado, empenhado_total),
            })

        return ret


def calculate_percent(value, total):
    if value is None or not total:
        return 0
    return value / total


def deflate(value, year):
    if value:
        try:
            deflator = Deflator.objects.get(year=year)
            value = value / deflator.index_number
            value = value.quantize(Decimal('.01'))
        except Deflator.DoesNotExist:
            pass
    return value
