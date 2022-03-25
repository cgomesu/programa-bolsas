from unidecode import unidecode


def formatador(string):
    ## remove acentos
    string = unidecode(unidecode(string))
    ## remove caracteres especiais e retorna string em MAIUSCULO
    return ''.join(s for s in string if s.isalnum()).upper()

def trocador(string, i, j):
    ## troca caractere do índice i por j da string
    ## transforma string em lista para manipulação dos caracteres
    string = list(string)
    string[i], string[j] = string[j], string[i]
    return ''.join(string)

def alfabeto_mais_um(string):
    ## substituir letra do alfabeto pela próxima
    string_plus = ""
    for caractere in string:
        if caractere.isalpha():
            if caractere == "Z":
                string_plus = string_plus + "A"
            else:
                string_plus = string_plus + chr(ord(caractere)+1)
        else:
            string_plus = string_plus + caractere
    return string_plus

def codificador(string):
    string = formatador(string)
    if len(string) > 1:
        ## i inicia em 0
        for i in range(int(len(string)/2)):
            string = trocador(string, i, len(string)-1-i)
        ## troca ultimos caracteres se string maior do que três
        if len(string) > 3:
            string = trocador(string, 0, len(string)-1)
    return alfabeto_mais_um(string)
