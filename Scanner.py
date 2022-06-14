import pickle 
 
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
full = {'alphabet': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'C', 'H', 'R', '+'], 'states': ['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21', 's22', 's23', 's24', 's25', 's26', 's27', 's28', 's29', 's30', 's31', 's32', 's33', 's34', 's35', 's36', 's37', 's38', 's39', 's40', 's41', 's42'], 'initial_state': 's0', 'accepting_states': ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21', 's42'], 'transitions': [['s0', '0', 's1'], ['s0', '1', 's2'], ['s0', '2', 's3'], ['s0', '3', 's4'], ['s0', '4', 's5'], ['s0', '5', 's6'], ['s0', '6', 's7'], ['s0', '7', 's8'], ['s0', '8', 's9'], ['s0', '9', 's10'], ['s0', 'C', 's11'], ['s1', '0', 's12'], ['s2', '0', 's12'], ['s3', '0', 's12'], ['s4', '0', 's12'], ['s5', '0', 's12'], ['s6', '0', 's12'], ['s7', '0', 's12'], ['s8', '0', 's12'], ['s9', '0', 's12'], ['s10', '0', 's12'], ['s12', '0', 's12'], ['s13', '0', 's12'], ['s14', '0', 's12'], ['s15', '0', 's12'], ['s16', '0', 's12'], ['s17', '0', 's12'], ['s18', '0', 's12'], ['s19', '0', 's12'], ['s20', '0', 's12'], ['s21', '0', 's12'], ['s1', '1', 's13'], ['s2', '1', 's13'], ['s3', '1', 's13'], ['s4', '1', 's13'], ['s5', '1', 's13'], ['s6', '1', 's13'], ['s7', '1', 's13'], ['s8', '1', 's13'], ['s9', '1', 's13'], ['s10', '1', 's13'], ['s12', '1', 's13'], ['s13', '1', 's13'], ['s14', '1', 's13'], ['s15', '1', 's13'], ['s16', '1', 's13'], ['s17', '1', 's13'], ['s18', '1', 's13'], ['s19', '1', 's13'], ['s20', '1', 's13'], ['s21', '1', 's13'], ['s1', '2', 's14'], ['s2', '2', 's14'], ['s3', '2', 's14'], ['s4', '2', 's14'], ['s5', '2', 's14'], ['s6', '2', 's14'], ['s7', '2', 's14'], ['s8', '2', 's14'], ['s9', '2', 's14'], ['s10', '2', 's14'], ['s12', '2', 's14'], ['s13', '2', 's14'], ['s14', '2', 's14'], ['s15', '2', 's14'], ['s16', '2', 's14'], ['s17', '2', 's14'], ['s18', '2', 's14'], ['s19', '2', 's14'], ['s20', '2', 's14'], ['s21', '2', 's14'], ['s1', '3', 's15'], ['s2', '3', 's15'], ['s3', '3', 's15'], ['s4', '3', 's15'], ['s5', '3', 's15'], ['s6', '3', 's15'], ['s7', '3', 's15'], ['s8', '3', 's15'], ['s9', '3', 's15'], ['s10', '3', 's15'], ['s12', '3', 's15'], ['s13', '3', 's15'], ['s14', '3', 's15'], ['s15', '3', 's15'], ['s16', '3', 's15'], ['s17', '3', 's15'], ['s18', '3', 's15'], ['s19', '3', 's15'], ['s20', '3', 's15'], ['s21', '3', 's15'], ['s1', '4', 's16'], ['s2', '4', 's16'], ['s3', '4', 's16'], ['s4', '4', 's16'], ['s5', '4', 's16'], ['s6', '4', 's16'], ['s7', '4', 's16'], ['s8', '4', 's16'], ['s9', '4', 's16'], ['s10', '4', 's16'], ['s12', '4', 's16'], ['s13', '4', 's16'], ['s14', '4', 's16'], ['s15', '4', 's16'], ['s16', '4', 's16'], ['s17', '4', 's16'], ['s18', '4', 's16'], ['s19', '4', 's16'], ['s20', '4', 's16'], ['s21', '4', 's16'], ['s1', '5', 's17'], ['s2', '5', 's17'], ['s3', '5', 's17'], ['s4', '5', 's17'], ['s5', '5', 's17'], ['s6', '5', 's17'], ['s7', '5', 's17'], ['s8', '5', 's17'], ['s9', '5', 's17'], ['s10', '5', 's17'], ['s12', '5', 's17'], ['s13', '5', 's17'], ['s14', '5', 's17'], ['s15', '5', 's17'], ['s16', '5', 's17'], ['s17', '5', 's17'], ['s18', '5', 's17'], ['s19', '5', 's17'], ['s20', '5', 's17'], ['s21', '5', 's17'], ['s1', '6', 's18'], ['s2', '6', 's18'], ['s3', '6', 's18'], ['s4', '6', 's18'], ['s5', '6', 's18'], ['s6', '6', 's18'], ['s7', '6', 's18'], ['s8', '6', 's18'], ['s9', '6', 's18'], ['s10', '6', 's18'], ['s12', '6', 's18'], ['s13', '6', 's18'], ['s14', '6', 's18'], ['s15', '6', 's18'], ['s16', '6', 's18'], ['s17', '6', 's18'], ['s18', '6', 's18'], ['s19', '6', 's18'], ['s20', '6', 's18'], ['s21', '6', 's18'], ['s1', '7', 's19'], ['s2', '7', 's19'], ['s3', '7', 's19'], ['s4', '7', 's19'], ['s5', '7', 's19'], ['s6', '7', 's19'], ['s7', '7', 's19'], ['s8', '7', 's19'], ['s9', '7', 's19'], ['s10', '7', 's19'], ['s12', '7', 's19'], ['s13', '7', 's19'], ['s14', '7', 's19'], ['s15', '7', 's19'], ['s16', '7', 's19'], ['s17', '7', 's19'], ['s18', '7', 's19'], ['s19', '7', 's19'], ['s20', '7', 's19'], ['s21', '7', 's19'], ['s1', '8', 's20'], ['s2', '8', 's20'], ['s3', '8', 's20'], ['s4', '8', 's20'], ['s5', '8', 's20'], ['s6', '8', 's20'], ['s7', '8', 's20'], ['s8', '8', 's20'], ['s9', '8', 's20'], ['s10', '8', 's20'], ['s12', '8', 's20'], ['s13', '8', 's20'], ['s14', '8', 's20'], ['s15', '8', 's20'], ['s16', '8', 's20'], ['s17', '8', 's20'], ['s18', '8', 's20'], ['s19', '8', 's20'], ['s20', '8', 's20'], ['s21', '8', 's20'], ['s1', '9', 's21'], ['s2', '9', 's21'], ['s3', '9', 's21'], ['s4', '9', 's21'], ['s5', '9', 's21'], ['s6', '9', 's21'], ['s7', '9', 's21'], ['s8', '9', 's21'], ['s9', '9', 's21'], ['s10', '9', 's21'], ['s12', '9', 's21'], ['s13', '9', 's21'], ['s14', '9', 's21'], ['s15', '9', 's21'], ['s16', '9', 's21'], ['s17', '9', 's21'], ['s18', '9', 's21'], ['s19', '9', 's21'], ['s20', '9', 's21'], ['s21', '9', 's21'], ['s11', 'H', 's22'], ['s22', 'R', 's23'], ['s23', '9', 's24'], ['s24', '+', 's25'], ['s25', 'C', 's26'], ['s26', 'H', 's27'], ['s27', 'R', 's28'], ['s28', '1', 's29'], ['s29', '0', 's30'], ['s30', '+', 's31'], ['s31', 'C', 's32'], ['s32', 'H', 's33'], ['s33', 'R', 's34'], ['s34', '1', 's35'], ['s35', '3', 's36'], ['s36', '+', 's37'], ['s37', 'C', 's38'], ['s38', 'H', 's39'], ['s39', 'R', 's40'], ['s40', '2', 's41'], ['s41', '0', 's42']]}
keywords = []
token2 = [[';', ';'], ['Resultado:', 'Resultado:'], ['-', '-'], ['Término:', 'Término:'], ['/', '/'], ['Factor:', 'Factor:'], ['Número:', 'Número:'], ['Token:', 'Token:']]
estados = [['s1', 'numeroToken'], ['s2', 'numeroToken'], ['s3', 'numeroToken'], ['s4', 'numeroToken'], ['s5', 'numeroToken'], ['s6', 'numeroToken'], ['s7', 'numeroToken'], ['s8', 'numeroToken'], ['s9', 'numeroToken'], ['s10', 'numeroToken'], ['s12', 'numeroToken'], ['s13', 'numeroToken'], ['s14', 'numeroToken'], ['s15', 'numeroToken'], ['s16', 'numeroToken'], ['s17', 'numeroToken'], ['s18', 'numeroToken'], ['s19', 'numeroToken'], ['s20', 'numeroToken'], ['s21', 'numeroToken'], ['s42', 'IGNORE']]
enter = chr(92) + chr(110) 
# -----------------------------------------------------------
# -----------------------------------------------------------        
result, values = procesar_txt(full, keywords, token2, estados)
with open('archivoConTokens.bin', 'wb') as f:
    pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)

with open('archivoConValores.bin', 'wb') as f:
    pickle.dump(values, f, pickle.HIGHEST_PROTOCOL)
# -----------------------------------------------------------
# -----------------------------------------------------------    
    
    