#!/usr/bin/env python3

################################################################
# Programa desenvolvido para processo de seleção
#
# Autor:  Carlos Gomes (cgomesu)
# Versão: 26/03/2022
#
# Repositório:
# - https://github.com/cgomesu/programa-bolsas
#
# Documentação relacionada:
# - curses: https://docs.python.org/3/library/curses.html
# - pandas: https://pandas.pydata.org/docs/
# - pandera: https://pandera.readthedocs.io/en/stable/index.html
################################################################

import curses
from curses.textpad import Textbox
from time import sleep
import utils
import re

## Constantes passiveis de personalização
MENU = [
    "Consultar bolsa zero / Ano",
    "Codificar nomes",
    "Consultar média anual",
    "Ranking valores de bolsa",
    "Sair"
]
## diretório de trabalho dos dados e nome do arquivo com dados
DIR_TRABALHO = "data/"
ARQUIVO_CSV = "br-capes-bolsistas-uab.csv"
## linha inicial do menu
LINHA_INICIAL = 0
## número máximo de caracteres no input de texto
TEXTBOX_CARACTERES_MAX = 60
## ranking das maiores e menores bolsas
RANKING_BOLSAS = 3
## validação de dados
LOG_DIR = "logs/"
LOG_FAILURE_CASES = "failure_cases.log"

def imprimir_menu_centro(janela, linha_selecionada):
    janela.clear()
    janela_altura, janela_largura = janela.getmaxyx()
    for indice, linha in enumerate(MENU):
        ## achar meio das dimensoes maximas da janela (floor) e imprimir linhas
        x = janela_largura//2 - len(linha)//2
        y = janela_altura//2 - len(MENU)//2 + indice
        ## para seleção, usar visual diferente
        if indice == linha_selecionada:
            janela.attron(curses.color_pair(1))
            janela.addstr(y, x, linha)
            janela.attroff(curses.color_pair(1))
        else:
            janela.addstr(y, x, linha)
    janela.refresh()

def imprimir_lista_centro(janela, lista=[]):
    ## modificado de imprimir_menu_centro()
    ## passa uma lista de strings para serem apresentados no centro
    janela.clear()
    janela_altura, janela_largura = janela.getmaxyx()
    for indice, linha in enumerate(lista):
        x = janela_largura//2 - len(linha)//2
        y = janela_altura//2 - len(lista)//2 + indice
        janela.addstr(y, x, linha)
    janela.refresh()

def imprimir_string_centro(janela, string):
    janela.clear()
    janela_altura, janela_largura = janela.getmaxyx()
    janela.addstr(janela_altura//2, janela_largura//2 - len(string)//2, string)
    janela.refresh()

def input_textbox_string_centro(janela, string):
    ## imprime janela e cria campo de texto para retornar input de texto do usuário
    string_final = string + " (Pressione 'Enter' ou 'Ctrl+g' para confirmar.)"
    janela.clear()
    janela_altura, janela_largura = janela.getmaxyx()
    ## ajustar para tamanho da string final
    x = janela_largura//2
    y = janela_altura//2
    janela.addstr(y-2, x-(len(string_final)//2), string_final)
    ## nova janela para user input abaixo do título e no centro; tamanho proporcional ao título
    editwin = curses.newwin(1, TEXTBOX_CARACTERES_MAX, y, x-(len(string_final)//2))
    janela.refresh()
    box = Textbox(editwin)
    box.edit()
    nome_digitado = box.gather()
    janela.refresh()
    return nome_digitado

def opcao_consulta_bolsa_ano(janela, dados):
    ano_digitado = ""
    while type(ano_digitado) is not int:
        try:
            ano_digitado = int(input_textbox_string_centro(janela, "Digite o ANO (YYYY) abaixo:"))
        except:
            imprimir_string_centro(janela, string="Digite um ANO válido.")
            sleep(1)
    ## filtrar df de acordo com ano
    dados_ano = dados[(dados["AN_REFERENCIA"] == ano_digitado) & (dados["ME_REFERENCIA"] == 1)]
    ## lidar com df vazio
    if dados_ano.empty:
        imprimir_string_centro(janela, string="Ano {} não encontrado.".format(ano_digitado))
    else:
        imprimir_lista_centro(janela, lista=["Informações do bolsista zero do ano {}".format(ano_digitado),
            "Nome: '{}'".format(dados_ano.iloc[0]["NM_BOLSISTA"]),
            "CPF: '{}'".format(dados_ano.iloc[0]["CPF_BOLSISTA"]),
            "Entidade de ensino: '{}'".format(dados_ano.iloc[0]["NM_ENTIDADE_ENSINO"]),
            "Valor da bolsa (em {}): '{}'".format(dados_ano.iloc[0]["CD_MOEDA"],dados_ano.iloc[0]["VL_BOLSISTA_PAGAMENTO"]),])

def opcao_procura_codifica_nome(janela, dados):
    nome_digitado = input_textbox_string_centro(janela, "Digite o NOME abaixo:")
    nome_digitado = ' '.join(utils.formatador(n) for n in nome_digitado.split())
    ## verificar se existe em qualquer lugar da coluna
    if dados["NM_BOLSISTA"].str.contains(nome_digitado).any():
        dados_com_nome = dados[dados["NM_BOLSISTA"].str.contains(nome_digitado)]
        ## loop casos com nome para perguntar ao usuario
        for i in range(len(dados_com_nome[["NM_BOLSISTA"]])):
            if re.match("^.*"+nome_digitado+".*$", dados_com_nome.iloc[i-1]["NM_BOLSISTA"]):
                imprimir_lista_centro(janela, lista=["Nome encontrado:",
                    "'{}'".format(dados_com_nome.iloc[i-1]["NM_BOLSISTA"]), "",
                    "Pressione 'ENTER' para CONFIRMAR",
                    "ou pressione outra telca para ir ao próximo.",])
                if janela.getch() == 10:
                    ## usar utilitario para codificar nome via join (com espaco) + list comprehension
                    nome_codificado = ' '.join(utils.codificador(n) for n in dados_com_nome.iloc[i-1]["NM_BOLSISTA"].split())
                    imprimir_lista_centro(janela, lista=["Informações do bolsista",
                        "Nome (codificado): '{}'".format(nome_codificado),
                        "Ano: '{}'".format(dados_com_nome.iloc[i-1]["AN_REFERENCIA"]),
                        "Entidade de ensino: '{}'".format(dados_com_nome.iloc[i-1]["NM_ENTIDADE_ENSINO"]),
                        "Valor da bolsa (em {}): '{}'".format(dados_com_nome.iloc[i-1]["CD_MOEDA"],dados_com_nome.iloc[i-1]["VL_BOLSISTA_PAGAMENTO"]),])
                    break
    else:
        imprimir_string_centro(janela, string="Não encontrado bolsista '{}'".format(nome_digitado))

def opcao_consulta_media_anual(janela, dados):
    ano_digitado = ""
    ## esperar até que usuário digite um inteiro
    while type(ano_digitado) is not int:
        try:
            ano_digitado = int(input_textbox_string_centro(janela, "Digite o ANO (YYYY) abaixo:"))
        except:
            imprimir_string_centro(janela, string="Digite um ANO válido.")
            sleep(2)
    ## filtrar df de acordo com ano
    dados_ano = dados[(dados["AN_REFERENCIA"] == ano_digitado)]
    ## lidar com df vazio
    if dados_ano.empty:
        imprimir_string_centro(janela, string="Ano {} não encontrado.".format(ano_digitado))
    else:
        imprimir_lista_centro(janela, lista=["Média do valor das bolas do Ano {}".format(ano_digitado),
            "média = '{:.2f}'".format(dados_ano["VL_BOLSISTA_PAGAMENTO"].mean())])

def opcao_ranking_bolsas(janela, dados, ranking=RANKING_BOLSAS):
    ## use nlargest e nsmallest para achar ranking bolsas
    dados_tres_maiores_bolsas = dados.nlargest(ranking, "VL_BOLSISTA_PAGAMENTO")
    dados_tres_menores_bolsas = dados.nsmallest(ranking, "VL_BOLSISTA_PAGAMENTO")
    for i in range(ranking):
        imprimir_lista_centro(janela, lista=["Os {} alunos com bolsa mais ALTA:".format(ranking),
            "{}. '{}' ({} {})".format(i+1,
                dados_tres_maiores_bolsas.iloc[i]["NM_BOLSISTA"],
                dados_tres_maiores_bolsas.iloc[i]["CD_MOEDA"],
                dados_tres_maiores_bolsas.iloc[i]["VL_BOLSISTA_PAGAMENTO"]),
            "", "Pressione qualquer tecla para ir ao próximo..."])
        janela.getch()
    for i in range(ranking):
        imprimir_lista_centro(janela, lista=["Os {} alunos com bolsa mais BAIXA:".format(ranking),
            "{}. '{}' ({} {})".format(i+1,
                dados_tres_menores_bolsas.iloc[i]["NM_BOLSISTA"],
                dados_tres_menores_bolsas.iloc[i]["CD_MOEDA"],
                dados_tres_menores_bolsas.iloc[i]["VL_BOLSISTA_PAGAMENTO"]),
            "", "Pressione qualquer tecla para ir ao próximo..."])
        if i < ranking-1:
            janela.getch()

def inicializar_dados(janela):
    ## inicializar objeto de dados e criar um df salvo na memoria para manipulação
    imprimir_lista_centro(janela, lista=["Lendo o arquivo CSV:","'{}'".format(ARQUIVO_CSV)])
    dados = utils.Dados(DIR_TRABALHO+ARQUIVO_CSV).csv_to_dataframe()
    sleep(1)
    if dados.empty:
        imprimir_lista_centro(janela, lista=["Erro crítico! Nenhum dado foi lido.",
            "Verifique o arquivo CSV e tente novamente.", "",
            "Pressione qualquer tecla para terminar o programa."])
        janela.getch()
        exit()
    ## validar dataframe importado para memória
    imprimir_string_centro(janela, string="Validando estrutura dos dados...")
    sleep(1)
    if not utils.Dados.validador_df(dados, log_failures=LOG_DIR+LOG_FAILURE_CASES):
        imprimir_lista_centro(janela, lista=["Erro crítico! O dataframe não passou a validação.",
            "Um log dos erros e casos será gravado em '{}'".format(LOG_DIR+LOG_FAILURE_CASES), "",
            "Corrigir os problemas no arquivo CSV e tentar novamente.",
            "Pressione qualquer tecla para terminar o programa."])
        janela.getch()
        exit()
    imprimir_string_centro(janela, string="Dados validados com sucesso!")
    sleep(3)
    ## verficar células em branco
    imprimir_string_centro(janela, string="Verificando valores em branco...")
    sleep(1)
    for coluna, soma in utils.Dados.soma_missing_por_col(dados):
        imprimir_lista_centro(janela, lista=["Achei um total de '{}' valores em branco na coluna '{}'".format(soma, coluna),
            "", "Pressione qualquer tecla para continuar..."])
        janela.getch()
    imprimir_string_centro(janela, string="Fim da verificação de valores em branco.")
    sleep(3)
    return dados

def main(janela):
    ## inicializar configuração básica do curses
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    linha_atual = LINHA_INICIAL

    dados = inicializar_dados(janela)

    ## menu principal
    imprimir_menu_centro(janela, linha_atual)
    ## loop para menu principal e seleção de opções
    while True:
        tecla = janela.getch()
        if tecla == curses.KEY_UP and linha_atual > 0:
            linha_atual -= 1
        elif tecla == curses.KEY_DOWN and linha_atual < len(MENU)-1:
            linha_atual += 1
        ## KEY_ENTER parece não confiável; 10 parece mais fidedigno
        elif tecla == 10:
            ## lidar com opção selecionada no menu (MENU[linha_atual])
            ## opção #1: consulta bolsa zero / ano
            if linha_atual == 0:
                opcao_consulta_bolsa_ano(janela, dados)
            ## opção #2: procura e codifica nome digitado por usuário
            elif linha_atual == 1:
                opcao_procura_codifica_nome(janela, dados)
            ## opção #3: consulta média anual
            elif linha_atual == 2:
                opcao_consulta_media_anual(janela, dados)
            ## opção #4: ranking tres maiores e menores bolsas
            elif linha_atual == 3:
                opcao_ranking_bolsas(janela, dados)
            ## última opção: sair
            elif linha_atual == len(MENU)-1:
                break
            janela.getch()
        imprimir_menu_centro(janela, linha_atual)

if __name__ == "__main__":
    curses.wrapper(main)
