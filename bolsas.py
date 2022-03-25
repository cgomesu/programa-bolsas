#!/usr/bin/python3

#########################################################
# Programa para processo de seleção PUCRS/Dell IT Academy
#
# Autor:  Carlos Gomes (cgomesu)                          
# Versão: 24/03/2022                                      
#
# Documentação relacionada:
# - curses: https://docs.python.org/3/library/curses.html
# - pandas: https://pandas.pydata.org/docs/
# 
#########################################################

import curses
from curses.textpad import Textbox
from time import sleep
import utils

MENU = [
    "Consultar bolsa zero / Ano",
    "Codificar nome",
    "Consultar média anual",
    "Ranking valores de bolsa",
    "Sair"
]

DIR_TRABALHO = "/home/cgomes/desktop universal/CARLOS/UNDERGRAD/INTERNSHIPS/DELL-IT-ACADEMY/etapa_2/data/"
ARQUIVO_CSV = "br-capes-bolsistas-uab.csv"

TEXTBOX_NUMERO_CARACTERES = 60

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
    string_final = string + " (Pressione 'Ctrl + g' para enviar)"
    janela.clear()
    janela_altura, janela_largura = janela.getmaxyx()
    ## ajustar para tamanho da string final
    x = janela_largura//2 ##- len(string_final)//2
    y = janela_altura//2
    janela.addstr(y-2, x-(len(string_final)//2), string_final)
    ## nova janela para user input abaixo do título e no centro; tamanho proporcional ao título
    editwin = curses.newwin(1, TEXTBOX_NUMERO_CARACTERES, y, x-(len(string_final)//2))
    janela.refresh()
    box = Textbox(editwin)
    box.edit()
    nome_digitado = box.gather()
    janela.refresh()
    return nome_digitado

def main(janela):
    ## inicializar configuração básica do curses
    curses.curs_set(False)  ##cursor
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)  ##par da cor de seleção padrão
    linha_atual = 0  ##linha selecionada

    ## inicializar objeto de dados e criar um df salvo na memoria para manipulação
    imprimir_lista_centro(janela, lista=["Aguarde enquanto estou lendo o seguinte arquivo de dados:", "'{}'".format(ARQUIVO_CSV)])
    dados = utils.Dados(DIR_TRABALHO+ARQUIVO_CSV).csv_to_dataframe()
    sleep(2)

    ## menu principal
    imprimir_menu_centro(janela, linha_atual)
    ## loop para menu principal e seleção de opções
    while True:
        tecla = janela.getch()
        if tecla == curses.KEY_UP and linha_atual > 0:
            linha_atual -= 1
        elif tecla == curses.KEY_DOWN and linha_atual < len(MENU)-1:
            linha_atual += 1
        ## KEY_ENTER parece não confiável; 10 parece funcionar para 'Enter/Return'
        elif tecla == 10:
            ## lidar com opção selecionada (MENU[linha_atual])
            imprimir_string_centro(janela, string="Opção selecionada: '{}'".format(MENU[linha_atual]))
            sleep(2)
            ## opção #1
            if linha_atual == 0:
                pass
            ## opção #2:codifica nome digitado por usuário
            elif linha_atual == 1:
                nome_digitado = input_textbox_string_centro(janela, "Digite o NOME abaixo:")
                nome_codificado = ' '.join(utils.codificador(s) for s in nome_digitado.split())
                imprimir_lista_centro(janela, lista=["Nome codificado:", "'{}'".format(nome_codificado)])
            ## opção #3
            elif linha_atual == 2:
                pass
            ## opção #4
            elif linha_atual == 3:
                pass
            ## última opção: sair
            elif linha_atual == len(MENU)-1:
                break
            janela.getch()
        imprimir_menu_centro(janela, linha_atual)

if __name__ == '__main__':
    curses.wrapper(main)
