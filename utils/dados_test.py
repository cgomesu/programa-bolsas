
############################################
# Módulo de teste para métodos de 'dados.py'
############################################

from .dados import Dados
import pandas


dados_erro_header = {
    "BOLSISTA": ['a', 'b', 'c'],
    "BOLSISTA": ['a', 'b', 'c'],
    "NM_ENTIDADE_ENSINO": ['a', 'b', 'c'],
    "ME_REFERENCIA": [1, 2, 3],
    "REFERENCIA": [1, 2, 3],
    "DIRETORIA": ['a', 'b', 'c'],
    "SG_SISTEMA_ORIGEM": ['a', 'b', 'c'],
    "CD_MODALIDADE_SGB": [1, 2, 3],
    "MODALIDADE_PAGAMENTO": ['a', 'b', 'c'],
    "MOEDA": ['a', 'b', 'c'],
    "VL_BOLSISTA_PAGAMENTO": [1, 2, 3],
}

dados_erro_input = {
    "NM_BOLSISTA": ['a', 2, 'c'],
    "CPF_BOLSISTA": ['a', 'b', 'c'],
    "NM_ENTIDADE_ENSINO": ['a', 'b', 'c'],
    "ME_REFERENCIA": ['a', 2, 3],
    "AN_REFERENCIA": [1, 2, 3],
    "SG_DIRETORIA": ['a', 'b', 'c'],
    "SG_SISTEMA_ORIGEM": ['a', 'b', 'c'],
    "CD_MODALIDADE_SGB": [1, 2, 3],
    "DS_MODALIDADE_PAGAMENTO": ['a', 'b', 'c'],
    "CD_MOEDA": ['a', 'b', 'c'],
    "VL_BOLSISTA_PAGAMENTO": [1, 2, 3],
}

dados_faltando_coluna = {
    "CPF_BOLSISTA": ['a', 'b', 'c'],
    "NM_ENTIDADE_ENSINO": ['a', 'b', 'c'],
    "ME_REFERENCIA": [1, 2, 3],
    "AN_REFERENCIA": [1, 2, 3],
    "SG_DIRETORIA": ['a', 'b', 'c'],
    "SG_SISTEMA_ORIGEM": ['a', 'b', 'c'],
    "CD_MODALIDADE_SGB": [1, 2, 3],
    "DS_MODALIDADE_PAGAMENTO": ['a', 'b', 'c'],
    "CD_MOEDA": ['a', 'b', 'c'],
    "VL_BOLSISTA_PAGAMENTO": [1, 2, 3],
}

dados_missing = {
    "NM_BOLSISTA": ['a', 'b', 'c'],
    "CPF_BOLSISTA": ['a', 'b', 'c'],
    "NM_ENTIDADE_ENSINO": ['a', 'b', 'c'],
    "ME_REFERENCIA": [1, None, None],
    "AN_REFERENCIA": [1, 2, 3],
    "SG_DIRETORIA": ['a', 'b', 'c'],
    "SG_SISTEMA_ORIGEM": ['a', 'b', 'c'],
    "CD_MODALIDADE_SGB": [1, 2, 3],
    "DS_MODALIDADE_PAGAMENTO": ['a', 'b', 'c'],
    "CD_MOEDA": [None, None, None],
    "VL_BOLSISTA_PAGAMENTO": [1, 2, 3],
}

dados = {
    "NM_BOLSISTA": ['a', 'b', 'c'],
    "CPF_BOLSISTA": ['a', 'b', 'c'],
    "NM_ENTIDADE_ENSINO": ['a', 'b', 'c'],
    "ME_REFERENCIA": [1, 2, 3],
    "AN_REFERENCIA": [1, 2, 3],
    "SG_DIRETORIA": ['a', 'b', 'c'],
    "SG_SISTEMA_ORIGEM": ['a', 'b', 'c'],
    "CD_MODALIDADE_SGB": [1, 2, 3],
    "DS_MODALIDADE_PAGAMENTO": ['a', 'b', 'c'],
    "CD_MOEDA": ['a', 'b', 'c'],
    "VL_BOLSISTA_PAGAMENTO": [1, 2, 3],
}

DF_VAZIO = pandas.DataFrame()
DF_ERRO_HEADER = pandas.DataFrame(dados_erro_header)
DF_ERRO_INPUT = pandas.DataFrame(dados_erro_input)
DF_FALTANDO_COLUNA = pandas.DataFrame(dados_faltando_coluna)
DF_MISSING = pandas.DataFrame(dados_missing)
DF = pandas.DataFrame(dados)


def test_validador_df() -> None:
    assert Dados(None).validador_df(DF_VAZIO) == False
    assert Dados(None).validador_df(DF_ERRO_HEADER) == False
    assert Dados(None).validador_df(DF_ERRO_INPUT) == False
    assert Dados(None).validador_df(DF_FALTANDO_COLUNA) == False
    assert Dados(None).validador_df(DF) == True

def test_soma_missin_por_col() -> None:
    for i, j in Dados(None).soma_missing_por_col(DF_MISSING):
        if i == "ME_REFERENCIA" or i == "CD_MOEDA":
            assert j > 0
