import re
import pandas


class Dados:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def csv_to_dataframe(self):
        ## tentar ler formato padrão e em erro, usar opções mais flexíveis, mas risco de perda de dados
        ## https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html?highlight=read_csv
        err = False
        try:
            return pandas.read_csv(self.arquivo, sep=";"), err
        except:
            err = True
            return pandas.read_csv(self.arquivo, sep=";", encoding="ISO-8859-1", on_bad_lines="skip"), err
