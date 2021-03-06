import os

import pytest

from datetime import date
from itertools import cycle
from unittest import TestCase

from django.core.files import File
from model_mommy import mommy

from regionalizacao.models import (
    Distrito, DistritoZonaFromTo, Escola, EtapaTipoEscolaFromTo, PtrfFromTo,
    TipoEscola, UnidadeRecursosFromTo, Recurso, Grupo, Subgrupo, Budget,
    EscolaInfo, PtrfFromToSpreadsheet, UnidadeRecursosFromToSpreadsheet,
    UpdateHistory)
from regionalizacao.services import (
    apply_distrito_zona_fromto,
    apply_etapa_tipo_escola_fromto,
    apply_ptrf_fromto,
    apply_unidade_recursos_fromto,
    populate_escola_info_budget_data,
    extract_ptrf_and_recursos_spreadsheets,
    get_years_to_be_updated,
    get_dt_updated,
)


@pytest.mark.django_db
class PtrfAndRecursosSpreadsheetTestCase():

    @pytest.fixture()
    def ptrf_file_fixture(self, db):
        filepath = os.path.join(
            os.path.dirname(__file__),
            'data/test_PtrfFromToSpreadsheet.xlsx')
        with open(filepath, 'rb') as f:
            yield f

        for ssheet_obj in PtrfFromToSpreadsheet.objects.all():
            ssheet_obj.spreadsheet.delete()

    @pytest.fixture()
    def recursos_file_fixture(self, db):
        filepath = os.path.join(
            os.path.dirname(__file__),
            'data/test_UnidadeRecursosFromToSpreadsheet.xlsx')
        with open(filepath, 'rb') as f:
            yield f

        for ssheet_obj in UnidadeRecursosFromToSpreadsheet.objects.all():
            ssheet_obj.spreadsheet.delete()


@pytest.mark.django_db
class TestGetYearsToBeUpdated(PtrfAndRecursosSpreadsheetTestCase):

    def test_return_years_to_be_updated(self, ptrf_file_fixture,
                                        recursos_file_fixture):
        current_year = date.today().year
        mommy.make(
            PtrfFromToSpreadsheet, spreadsheet=File(ptrf_file_fixture),
            year=2017, _quantity=2)
        mommy.make(
            PtrfFromToSpreadsheet, spreadsheet=File(ptrf_file_fixture),
            year=2018)
        mommy.make(
            UnidadeRecursosFromToSpreadsheet,
            spreadsheet=File(recursos_file_fixture),
            year=2018)
        mommy.make(
            UnidadeRecursosFromToSpreadsheet,
            spreadsheet=File(recursos_file_fixture),
            year=current_year)

        years = get_years_to_be_updated()
        assert [2017, 2018, current_year] == years


@pytest.mark.django_db
class TestExtractPtrfAndRecursosSpreadsheet(PtrfAndRecursosSpreadsheetTestCase):

    def test_extract_spreadsheets(self, ptrf_file_fixture,
                                  recursos_file_fixture):
        ptrf_sheet = mommy.make(PtrfFromToSpreadsheet,
                                spreadsheet=File(ptrf_file_fixture))
        recursos_sheet = mommy.make(UnidadeRecursosFromToSpreadsheet,
                                    spreadsheet=File(recursos_file_fixture))
        assert not ptrf_sheet.extracted
        assert not recursos_sheet.extracted

        extract_ptrf_and_recursos_spreadsheets()

        ptrf_sheet.refresh_from_db()
        recursos_sheet.refresh_from_db()
        assert ptrf_sheet.extracted
        assert recursos_sheet.extracted


@pytest.mark.django_db
class TestApplyDistritoZonaFromTo(TestCase):

    def test_apply_distrito_zona_fromto(self):
        mommy.make(Distrito, coddist=cycle([1, 2]), zona=None, _quantity=2)
        mommy.make(Distrito, coddist=3, zona=None)

        mommy.make(DistritoZonaFromTo, coddist=cycle([1, 2]), zona="Norte",
                   _quantity=2)
        mommy.make(DistritoZonaFromTo, coddist=3, zona="Sul")

        apply_distrito_zona_fromto()

        distritos = Distrito.objects.all().order_by('coddist')
        assert distritos[0].zona == "Norte"
        assert distritos[1].zona == "Norte"
        assert distritos[2].zona == "Sul"


@pytest.mark.django_db
class TestApplyEtapaTipoEscolaFromTo(TestCase):

    def test_apply_etapa_tipo_escola_fromto(self):
        mommy.make(TipoEscola, code='CEMEI', desc=None, etapa=None)
        mommy.make(TipoEscola, code='EMEF', desc=None, etapa=None)

        mommy.make(EtapaTipoEscolaFromTo, tipoesc='CEMEI', desctipoesc='desc 1',
                   etapa='Infantil')
        mommy.make(EtapaTipoEscolaFromTo, tipoesc='EMEF', desctipoesc="desc 2",
                   etapa='Fundamental')

        apply_etapa_tipo_escola_fromto()

        tipos = TipoEscola.objects.all().order_by('code')
        assert tipos[0].desc == "desc 1"
        assert tipos[0].etapa == "Infantil"
        assert tipos[1].desc == "desc 2"
        assert tipos[1].etapa == "Fundamental"


@pytest.mark.django_db
class TestApplyPtrfFromTo(TestCase):

    def test_apply_ptrf_fromto(self):
        escola1 = mommy.make(Escola, codesc='01')
        escola2 = mommy.make(Escola, codesc='02')
        mommy.make(Budget, escola=escola1, year=2019, ptrf=None)
        mommy.make(Budget, escola=escola2, year=2019, ptrf=None)
        mommy.make(Budget, escola=escola1, year=2020, ptrf=None)

        ft1 = mommy.make(PtrfFromTo, codesc='01', year=2019, vlrepasse=50)
        ft2 = mommy.make(PtrfFromTo, codesc='02', year=2019, vlrepasse=60)

        apply_ptrf_fromto()

        budgets = Budget.objects.all().order_by('year', 'escola__codesc')
        assert budgets[0].ptrf == ft1.vlrepasse
        assert budgets[1].ptrf == ft2.vlrepasse
        assert budgets[2].ptrf is None


@pytest.mark.django_db
class TestApplyUnidadeRecursosFromTo(TestCase):

    def test_apply_creates_new_budget_instance(self):
        escola = mommy.make(Escola, codesc='01')
        year = date.today().year
        other_budget = mommy.make(Budget, escola=escola, year=year-1)

        mommy.make(
            UnidadeRecursosFromTo, codesc='01', year=year,
            grupo='Material escolar', subgrupo='Kit fundamental',
            valor=15, label='Unidades')
        mommy.make(
            UnidadeRecursosFromTo, codesc='01', year=year,
            grupo='Material escolar', subgrupo='Kit fundamental',
            valor=50.23, label='R$')

        apply_unidade_recursos_fromto()

        assert 2 == Budget.objects.count()
        assert 1 == Recurso.objects.count()
        assert 1 == Subgrupo.objects.count()
        assert 1 == Grupo.objects.count()

        budget = Budget.objects.all().order_by('-year').first()
        assert budget.escola == escola
        assert budget.year == year
        other_budget.refresh_from_db()
        assert other_budget.escola == escola
        assert other_budget.year == year - 1
        assert other_budget.recursos.count() == 0

        recurso = Recurso.objects.first()
        assert budget == recurso.budget
        assert 'Kit fundamental' == recurso.subgrupo.name
        assert 'Material escolar' == recurso.subgrupo.grupo.name
        assert 15 == recurso.amount
        assert 'Unidades' == recurso.label
        assert 50.23 == recurso.cost

    def test_apply_updates_existing_budget_instance(self):
        escola = mommy.make(Escola, codesc='01')
        year = date.today().year
        budget = mommy.make(Budget, escola=escola, year=year)
        other_budget = mommy.make(Budget, escola=escola, year=year-1)

        mommy.make(
            UnidadeRecursosFromTo, codesc='01', year=year,
            grupo='Material escolar', subgrupo='Kit fundamental',
            valor=15, label='Unidades')
        mommy.make(
            UnidadeRecursosFromTo, codesc='01', year=year,
            grupo='Material escolar', subgrupo='Kit fundamental',
            valor=50.23, label='R$')

        apply_unidade_recursos_fromto()

        assert 2 == Budget.objects.count()
        assert 1 == Recurso.objects.count()
        assert 1 == Subgrupo.objects.count()
        assert 1 == Grupo.objects.count()

        budget.refresh_from_db()
        assert budget.escola == escola
        assert budget.year == year
        other_budget.refresh_from_db()
        assert other_budget.escola == escola
        assert other_budget.year == year - 1
        assert other_budget.recursos.count() == 0

        recurso = Recurso.objects.first()
        assert budget == recurso.budget
        assert 'Kit fundamental' == recurso.subgrupo.name
        assert 'Material escolar' == recurso.subgrupo.grupo.name
        assert 15 == recurso.amount
        assert 'Unidades' == recurso.label
        assert 50.23 == recurso.cost


@pytest.mark.django_db
class TestPopulateEscolaInfoBudgetData(TestCase):

    # TODO: test when subgrupo is null
    def test_populate_escola_info(self):
        year = date.today().year

        escola = mommy.make(Escola, codesc='01')
        info = mommy.make(EscolaInfo, escola=escola, nomesc="Escolesc",
                          year=year)

        budget = mommy.make(Budget, escola=escola, year=year, ptrf=10)

        grupo1 = mommy.make(Grupo, name='Repasses')
        subgrupo1 = mommy.make(Subgrupo, grupo=grupo1, name='IPTU')
        subgrupo2 = mommy.make(Subgrupo, grupo=grupo1, name='Locação')
        mommy.make(Recurso, budget=budget, subgrupo=subgrupo1, cost=100)
        mommy.make(Recurso, budget=budget, subgrupo=subgrupo2, cost=200)

        grupo2 = mommy.make(Grupo, name='Material escolar')
        subgrupo2 = mommy.make(Subgrupo, grupo=grupo2, name='Kit fundamental')
        subgrupo3 = mommy.make(Subgrupo, grupo=grupo2, name='Livros')
        mommy.make(Recurso, budget=budget, subgrupo=subgrupo2, cost=1000,
                   amount=1500, label='kits')
        mommy.make(Recurso, budget=budget, subgrupo=subgrupo3, cost=2000,
                   amount=120, label='livros')

        grupo3 = mommy.make(Grupo, name='Outros')
        subgrupo3 = mommy.make(Subgrupo, grupo=grupo3, name='')
        mommy.make(Recurso, budget=budget, subgrupo=subgrupo3, cost=1)

        populate_escola_info_budget_data()

        info.refresh_from_db()
        assert info.budget_total == 3311

        expected = {
            'ptrf': 10,
            'grupos': [
                {
                    "name": "Material escolar",
                    "total": 3000,
                    'subgrupos': [
                        {
                            'name': 'Livros',
                            'cost': 2000,
                            'amount': 120,
                            'label': 'livros',
                        },
                        {
                            'name': 'Kit fundamental',
                            'cost': 1000,
                            'amount': 1500,
                            'label': 'kits',
                        },
                    ],
                },
                {
                    "name": "Repasses",
                    "total": 300,
                    'subgrupos': [
                        {
                            'name': 'Locação',
                            'cost': 200,
                            'amount': None,
                            'label': None,
                        },
                        {
                            'name': 'IPTU',
                            'cost': 100,
                            'amount': None,
                            'label': None,
                        },
                    ],
                },
                {
                    "name": "Outros",
                    "total": 1,
                    'subgrupos': [],
                },
            ],
        }

        assert expected == info.recursos


@pytest.mark.django_db
class TestGetDtUpdate:

    def test_returns_newest_register_in_update_history_table(self):
        mommy.make(UpdateHistory)
        assert date.today() == get_dt_updated()

    def test_return_last_added_sheet_creation_date_when_history_is_empty(self):
        assert 0 == UpdateHistory.objects.count()

        sheet1 = mommy.make(PtrfFromToSpreadsheet, extracted=True)
        sheet1.created_at = date(2019, 12, 1)
        sheet1.save()

        sheet2 = mommy.make(PtrfFromToSpreadsheet, extracted=True)
        sheet2.created_at = date(2017, 1, 1)
        sheet2.save()

        sheet3 = mommy.make(UnidadeRecursosFromToSpreadsheet,
                            extracted=True)
        sheet3.created_at = date(2018, 1, 17)
        sheet3.save()

        assert date(2019, 12, 1) == get_dt_updated()
