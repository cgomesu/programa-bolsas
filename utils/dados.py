import pandas
import pandera

## esquema de validação da df via pandera
SCHEMA_DICT = {
    "NM_BOLSISTA": pandera.Column(str),
    "CPF_BOLSISTA": pandera.Column(str),
    "NM_ENTIDADE_ENSINO": pandera.Column(str),
    "ME_REFERENCIA": pandera.Column(int),
    "AN_REFERENCIA": pandera.Column(int),
    "SG_DIRETORIA": pandera.Column(str),
    "SG_SISTEMA_ORIGEM": pandera.Column(str),
    "CD_MODALIDADE_SGB": pandera.Column(int),
    "DS_MODALIDADE_PAGAMENTO": pandera.Column(str),
    "CD_MOEDA": pandera.Column(str),
    "VL_BOLSISTA_PAGAMENTO": pandera.Column(int),
}


class Dados:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def csv_to_dataframe(self):
        ## tentar ler formato padrão e em erro, usar opções mais flexíveis, mas risco de perda de dados
        ## https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html?highlight=read_csv
        try:
            return pandas.read_csv(self.arquivo, sep=",|;", encoding="ISO-8859-1", engine="python")
        except:
            return pandas.read_csv(self.arquivo, sep=",|;", encoding="ISO-8859-1", engine="python", on_bad_lines="skip")

    @staticmethod
    def validate_df(df, log_failures):
        schema = pandera.DataFrameSchema(SCHEMA_DICT)
        try:
            schema(df, lazy=True), object()
            return True
        except pandera.errors.SchemaErrors as err:
            with open(log_failures, 'w') as f:
                f.write("{}".format(err))
            return False
