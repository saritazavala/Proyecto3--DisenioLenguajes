"""
UNIVERSIDAD DEL VALLE DE GUATEMALA
LENGUAJES DE PROGRAMACION
SARA NOHEMI ZAVALA GUTIERREZ
"""

from PySimpleAutomata import automata_IO
import os
import json
from AFN import AFN
from CambioAFN import Subconjuntos
from PSintaxis import PSintaxis

class Producir_utils:
    def __init__(self, tokens, keywords, characters, token2, producciones):
        self.tokens = tokens
        self.keywords = keywords
        self.characters = characters
        self.operaciones = ['(', ')', '|', '{', '}', '[', ']']
        self.expressions = []
        self.tokensAccepted = []
        self.estados = []
        self.token2 = token2
        self.producciones = producciones
        self.analizeGrammar()
        alphaaa = []
        # ------------------------------------------
        full_util = {"alphabet": alphaaa,"states": [],"initial_states": "0","accepting_states": [],"transitions": [],}

        # ------------------------------------------
        # print(full_util)
        # prueba
        # ------------------------------------------
        index = 0
        for i in self.expressions:
            currentAlphabet = []
            for j in i:
                if j not in self.operaciones:
                    currentAlphabet.append(j)
                    if j not in alphaaa:
                        alphaaa.append(j)
            self.generateAFN(list(i), currentAlphabet, full_util, self.tokens[index].id)
            index += 1

        afd = self.crear_automata(full_util, alphaaa)
        # ------------------------------------------------------
        # ------------------------------------------------------
        self.generar_scanner(afd)  # Se genera el Scanner
        # ------------------------------------------------------
        # ------------------------------------------------------
        PSintaxis(self.tokens, self.keywords, self.producciones, self.token2)  # Se Genera el parser
    def crear_automata(self, full_util, alphabet):
        # Crear y graficar AFD
        print("Scanner y Parser creados")
        afd_sub = Subconjuntos(full_util['states'], full_util['transitions'], alphabet, full_util['accepting_states'],
                               self.tokensAccepted)
        afd_snodes = afd_sub.generateAFD()
        full_utilx2 = {"alphabet": alphabet,"states": [],"initial_state": "s0","accepting_states": [],"transitions": [],}

        for i in afd_snodes:
            if i.state not in full_utilx2['states']:
                full_utilx2['states'].append(str(i.state))
                if i.accepted == True:
                    full_utilx2['accepting_states'].append(str(i.state))
                for t in i.transitions:
                    full_utilx2['transitions'].append([str(t[0]), t[1], str(i.state)])

        self.estados = afd_sub.getTokensAccepted()
        return full_utilx2

    def generateAFN(self, arr, alphabet, full_util, tokens):
        afn = AFN(arr, alphabet)
        afn_nodes = afn.generateAFN()

        newAccepted = []
        if full_util['states'] == []:
            nextIndex = 1
        else:
            nextIndex = int(full_util['states'][-1]) + 1
        full_util['transitions'].append(['0', 'epsilon', str(int(afn_nodes[0].state) + nextIndex)])
        for i in afn_nodes:
            if str(int(i.state) + nextIndex) not in full_util['states']:
                full_util['states'].append(str(int(i.state) + nextIndex))
                if i.accepted == True:
                    newAccepted.append(str(int(i.state) + nextIndex))
                    full_util['accepting_states'].append(str(int(i.state) + nextIndex))
                for t in i.transitions:
                    full_util['transitions'].append([str(int(t[0]) + nextIndex), t[1], str(int(i.state) + nextIndex)])

        for i in newAccepted:
            self.tokensAccepted.append([i, tokens])
    def analizeGrammar(self):
        # En cada token, convertir ids de caracteres a sus alfabetos
        finalExpression = []
        for i in self.tokens:
            validacion_presente = i.value
            validacion_presente = validacion_presente.replace('"', '')
            nextIndex = 0
            for j in self.characters:
                nextIndex += 1
                goNext = False
                character = validacion_presente.find(j.id)
                if character != -1:
                    for c in self.characters[nextIndex:]:
                        if validacion_presente.find(c.id) == character:
                            goNext = True
                    if goNext:
                        goNext = False
                        continue
                    currentAlphabet = '('
                    if len(j.alphabet) == 1:
                        currentAlphabet = j.alphabet[0]
                    else:
                        currentAlphabet = (currentAlphabet * (len(j.alphabet) - 1)) + j.alphabet[0]
                        for a in j.alphabet[1:]:
                            # Agregar OR para cada valor del alfabeto
                            currentAlphabet += '|' + a + ')'
                    # Reemplazar el id del caracter por su alfabeto
                    validacion_presente = validacion_presente.replace(j.id, currentAlphabet)
            finalExpression.append(validacion_presente)
        self.expressions = finalExpression

    def generar_scanner(self, full):
        f = open("Scanner.py", "w")
        f.write("import pickle \n")
        f.write(f''' 
def procesar_txt(full, keywords, token2, estados):
# -----------------------------------------------------------
    bandera = False
# -----------------------------------------------------------    
    while bandera == False:
        # -----------------------------------------------------------    
        filename = input('Ingrese el nombre del archivo txt --> ')
        # -----------------------------------------------------------
        if filename[-4:] != '.txt':
            print('Doc invalido')
            continue
        try:
            archivoTexto = open(filename)
        except IOError:
            print('No se pudo abrir el doc')
            continue
        bandera = True
# -----------------------------------------------------------
    fileLines = archivoTexto.readlines()
# -----------------------------------------------------------    
    tokens = []
# -----------------------------------------------------------    
    values = []
    for i in fileLines:
# -----------------------------------------------------------
        i = i.replace(enter, '')
        cadena = list(i)
        cadena.append('e')
        done = False
        index = 0
        while done == False:
            i = index
# -----------------------------------------------------------
            recorrido_aceptado = []
# -----------------------------------------------------------
            cadena_verificar = ''
# -----------------------------------------------------------            
            aceptado_0 = 0
            lastToken = ''
# -----------------------------------------------------------            
            nadaaa = False
            maybeKeyword = False
# -----------------------------------------------------------            
            ultimo = ''
            while (i != len(cadena)-1):
# -----------------------------------------------------------
                cadena_verificar += cadena[i]
                validacion_presente = encontrar_valores(full, cadena_verificar, keywords, token2, estados)
                recorrido_aceptado.append([validacion_presente[0], cadena_verificar])
                if(validacion_presente[0] != "Error"):
                    aceptado_0 = i
                    lastToken = validacion_presente[0]
                    ultimo = cadena_verificar
                    if validacion_presente[1] == 'token2':
                        maybeKeyword = True
                elif validacion_presente[1] == 's0':
                    for k in keywords:
                        if k[1].find(cadena_verificar) != -1:
                            maybeKeyword = True
                            break
                    if maybeKeyword == False:
                        nadaaa = True
                        break
                i+=1
                if i == len(cadena)-1 and lastToken == '':
                    tokens.append('Error')
                    nadaaa = True
# -----------------------------------------------------------                    
            if nadaaa == False:
                index = aceptado_0 + 1
                tokens.append(lastToken)
                values.append(ultimo)
            else:index += 1
            if index == len(cadena)-1:break
# -----------------------------------------------------------       
    print("Scanner corrido")
    res = ''
    for i in tokens:
        res += i + ' '
    vals = ''
    for i in values:
        vals += i + ' '
    return res, vals

def encontrar_valores(full, opc, keywords, token2, estados):
    found = False
    for i in keywords:
        if opc == i[1]:return [i[0], 's1']
    for i in token2:
        if opc == i[1]:return [i[0], 'token2']
    if found != True:
        cadena = list(opc)
        if len(cadena) == 0:
            if 's0' in full['accepting_states']:
                for i in estados:
                    if i[0] == 's0':return [i[1], 's1']
            else:
                return ["Error, 's0'"]
        else:
            s = 's0'
            c = cadena[0]
            i = 0
            cadena.append('eof')
            while (c != 'eof'):
                cambio = False
                for j in full['transitions']:
                    if j[0] == s and j[1] == c:
                        s = j[2]
                        cambio = True
                        break
                if cambio == False:break
                i+=1
                c = cadena[i]
            if (s in full['accepting_states'] and cambio):
                for i in estados:
                    if i[0] == s:return [i[1], s]
            else:
                return ["Error", s]
# -----------------------------------------------------------
# -----------------------------------------------------------
''')
        f.write("full = " + str(full))
        keys = []
        for i in self.keywords:
            keys.append([i.id, i.value])
        f.write("\nkeywords = " + str(keys))
        token2_list = []
        for i in self.token2:
            token2_list.append([i.id, i.value])
        f.write("\ntoken2 = " + str(token2_list))
        f.write("\nestados = " + str(self.estados))
        f.write("\nenter = chr(92) + chr(110)")
        f.write(''' 
# -----------------------------------------------------------
# -----------------------------------------------------------        
result, values = procesar_txt(full, keywords, token2, estados)
with open('archivoConTokens.bin', 'wb') as f:
    pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)

with open('archivoConValores.bin', 'wb') as f:
    pickle.dump(values, f, pickle.HIGHEST_PROTOCOL)
# -----------------------------------------------------------
# -----------------------------------------------------------    
    
    ''')





