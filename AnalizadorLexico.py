"""
UNIVERSIDAD DEL VALLE DE GUATEMALA
LENGUAJES DE PROGRAMACION
SARA NOHEMI ZAVALA GUTIERREZ
"""

from Caracteres import *
seccion = ''
caracteres, keywords, tokens, tokens_2, producciones = [], [], [], [], []
final_linea = True


def get_data():
    return tokens, keywords, caracteres, producciones, tokens_2


def analizar_archivo(archivo):
    archivo = list(map(lambda x: x.replace('\n', ''), archivo))
    archivo = list(filter(lambda x: x != '', archivo))
    for linea in archivo:
        procesar(linea, linea.replace(' ', ''))


def procesar(linea, letras):
    global seccion, final_linea
    if linea == '':
        pass
    if linea[:9] == 'COMPILER ':
        pass
    elif linea[:4] == 'END ':
        0
    elif linea[:10] == 'CHARACTERS':
        seccion = 'CHARACTERS'
    elif linea[:9] == 'KEYWORDS':
        seccion = 'KEYWORDS'
    elif linea[:8] == 'TOKENS':
        seccion = 'TOKENS'
    elif linea[:12] == 'PRODUCTIONS':
        seccion = 'PRODUCTIONS'
    else:
        if seccion != 'PRODUCTIONS':
            if letras[-1] != '.' and letras[-1] != '=' and letras[-1] != '+':
                print('Error')
                quit(0)
        if not final_linea:
            letras = 'a=' + letras

        palabras = letras.split('=', 1)

        if seccion == 'CHARACTERS':
            set_caracteres(palabras, letras)

        if seccion == 'KEYWORDS':
            set_keywords(palabras, letras)

        if seccion == 'TOKENS':
            set_tokens(palabras, letras)

        if seccion == 'PRODUCTIONS':
            set_productions(palabras, letras)

        if letras[-1] != '.':
            final_linea = False


def set_caracteres(palabras, letras):
    global final_linea

    id = palabras[0]
    valor = []
    texto = palabras[1].split('+')
    if letras[-1] == '.':
        texto[-1] = texto[-1][:-1]
    texto = [x for x in texto if x]

    if letras[-1] == '.' or letras[-1] == '+':
        posicion = 0

        while posicion < len(texto):
            if texto[posicion][0] == '"':
                alfabeto = list(texto[posicion].replace('"', ''))
                for caracter in alfabeto:
                    valor.append(caracter)

            elif texto[posicion][:4] == 'CHR(':
                ascii = texto[posicion][4:][:-1]
                valor.append(chr(int(ascii)))
            else:
                en_caracteres = False

                for car in caracteres:
                    if car.id == texto[posicion]:
                        for j in car.alphabet:
                            valor.append(j)
                            en_caracteres = True
                        break
                if not en_caracteres:
                    print("Caracter indefinido")
                    quit(0)
            posicion += 1

    if final_linea:
        caracteres.append(Caracteres(id, valor))
    else:
        for v in valor:
            caracteres[-1].alphabet.append(v)
        final_linea = True


def set_keywords(palabras, letras):
    global final_linea

    id = palabras[0]
    valor = []
    if letras[-1] == '.':
        valor = palabras[1]
    if final_linea:
        keywords.append(Keywords(id, valor))
    else:
        keywords[-1].value = valor
        final_linea = True


def set_tokens(palabras, letras):
    global final_linea
    id = palabras[0]
    valor = palabras[1]
    position = 2
    existe = False

    while position < len(palabras):
        if palabras[position] == 'EXCEPT':
            existe = True
            break
        valor += ' ' + palabras[position]
        position += 1
    if not existe and letras[-1] == '.':
        valor = valor[:-1]

    if valor.find('EXCEPT') != -1:
        valor = valor[:valor.find('EXCEPT')]
    if final_linea:
        tokens.append(Token(id, valor))
    else:
        tokens[-1].value += valor
        final_linea = True


def set_productions(palabras, letras):
    global final_linea
    identificador = palabras[0]
    parametros = []

    if identificador.find('<') != -1:
        inicio_parametro = identificador.split('<')
        fin_parametro = inicio_parametro[1].find('>')

        if fin_parametro != -1:
            parametros = inicio_parametro[1][:fin_parametro]
            id = inicio_parametro[0]
    else:
        id = identificador

    contador = palabras[1].count('"') / 2
    expresion = palabras[1]
    index = 0

    while contador > 0:
        inicio = expresion.find('"')
        if inicio != -1:
            fin = expresion[inicio + 1:].find('"')

            if fin != -1:
                token_nuevo = expresion[inicio + 1: inicio + 1 + fin]
                existe = False
                for token in tokens_2:
                    if token_nuevo == token.id:
                        existe = True
                if not existe:
                    tokens_2.append(Token(token_nuevo, token_nuevo))
            index = inicio + fin + 1
            expresion = expresion[index + 1:]
            contador -= 1
    if letras[-1] == '.':
        value = palabras[1][:-1].replace('\t', '')
    else:
        value = palabras[1].replace('\t', '')

    if final_linea:
        producciones.append(Production(id, parametros, value))
    else:
        producciones[-1].value += value
        final_linea = True
