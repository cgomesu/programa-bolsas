
##################################################
# Módulo de teste para métodos de 'ferramentas.py'
##################################################

from .ferramentas import formatador, trocador, alfabeto_mais_um, codificador

## meus inputs
STRING_ESPECIAL = "!T@é#S$t%*"
STRING_INTEIROS = "123456"
STRING_LETRAS = "ABCDEZ"

## inputs dos exemplos no enunciado
ENUNCIADO_SEM_CODIFICADO = ["PERIGO", "FUGA", "PAZ"]
ENUNCIADO_COM_CODIFICADO = ["QHJSFP", "GHVB", "ABQ"]

def test_formatador() -> None:
    assert formatador(STRING_ESPECIAL) == "TEST"

def test_trocador() -> None:
    assert trocador(STRING_INTEIROS, 0, 1) == "213456"
    assert trocador(STRING_INTEIROS, 0, len(STRING_INTEIROS)-1) == "623451"

def test_alfabeto_mais_um() -> None:
    assert alfabeto_mais_um(STRING_LETRAS) == "BCDEFA"

def test_codificador() -> None:
    for i in ENUNCIADO_SEM_CODIFICADO:
        assert codificador(i) == ENUNCIADO_COM_CODIFICADO[ENUNCIADO_SEM_CODIFICADO.index(i)]

