import requests

from regionalizacao.constants import EOL_API_URL
from regionalizacao.dao.models_dao import DreDao, EscolaDao, TipoEscolaDao


def update_dre_table():
    dre_dao = DreDao()
    url = f'{EOL_API_URL}diretorias/'

    response = requests.get(url)
    results = response['results']

    created_count = 0
    updated_count = 0
    for dre_dict in results:
        _, created = dre_dao.update_or_create(
            code=dre_dict['dre'],
            name=dre_dict['diretoria'],
        )
        if created:
            created_count += 1
        else:
            updated_count += 1

    return created_count, updated_count


def update_tipo_escola_table():
    tipo_dao = TipoEscolaDao()
    url = f'{EOL_API_URL}tipo_escola/'

    response = requests.get(url)
    results = response['results']

    created_count = 0
    for tipo_dict in results:
        _, created = tipo_dao.get_or_create(
            code=tipo_dict['tipoesc'],
        )
        if created:
            created_count += 1

    return created_count


def update_escola_table():
    escola_dao = EscolaDao()
    url = f'{EOL_API_URL}livroaberto_escolas/'

    response = requests.get(url)
    results = response['results']

    created_count = 0
    for escola_dict in results:
        _, created = escola_dao.get_or_create(
            dre=escola_dict["dre"],
            codesc=escola_dict["codesc"],
            tipoesc=escola_dict["tipoesc"],
            nomesc=escola_dict["nomesc"],
            diretoria=escola_dict["diretoria"],
            endereco=escola_dict["endereco"],
            numero=escola_dict["numero"],
            bairro=escola_dict["bairro"],
            cep=escola_dict["cep"],
            situacao=escola_dict["situacao"],
            coddist=escola_dict["coddist"],
            distrito=escola_dict["distrito"],
            rede=escola_dict["rede"],
            latitude=escola_dict["latitude"],
            longitude=escola_dict["longitude"],
            total_vagas=escola_dict["total_vagas"],
        )
        if created:
            created_count += 1

    return created_count
