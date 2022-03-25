import re
import pandas


## dicionário regex para validação dos dados
regex_dicionario = {
    'nome': re.compile(
        r"",
        re.IGNORECASE
    ),
    'cpf': re.compile(
        r"",
        re.IGNORECASE
    ),
    'ano': re.compile(
        r"",
        re.IGNORECASE
    ),
    'valor_bolsa': re.compile(
        r"",
        re.IGNORECASE
    )
}

class Dados:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def csv_to_dataframe(self):
        ## ler arquivo com opções não padrão
        ## TODO: ver o que fazer com casos de colon vs. semi-colon e erros de estrutura:
        ## https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html?highlight=read_csv
        return pandas.read_csv(self.arquivo, sep=';', encoding='ISO-8859-1', on_bad_lines='skip')

    def interpretador(self):
        pass
    