"""
UNIVERSIDAD DEL VALLE DE GUATEMALA
LENGUAJES DE PROGRAMACION
SARA NOHEMI ZAVALA GUTIERREZ
"""
class PSintaxis(object):
    def __init__(self, tokens, keywords, productions, token2):
        self.tokens = tokens
        self.keywords = keywords
        self.token2 = token2
        self.productions = productions
        self.scannedTokens = []
        self.idsF = []
        self.Tid = []
        self.tabs = 0
        self.continuarL = False

        index = 0
        for i in self.productions:
            self.primero(index, i.value)
            index += 1
            self.idsF.append(i.id)

        for i in self.tokens:
            self.Tid.append(i.id)

        cambio = True
        while cambio:
            cambio = False
            for i in self.productions:
                for j in i.primeros:
                    if j in self.idsF:
                        i.primeros.remove(j)
                        for k in self.productions:
                            if k.id == j:
                                i.primeros += k.primeros
                                cambio = True

        f = open("Parser.py", "w")
        self.analizeProductions(f)
    def analizeExpression(self, file, expression, orOps, firstIf=False, inLoop=False):
        position = 0
        inOr = ''
        while position < len(expression):
            if expression.count('(') != expression.count(')') or expression.count('<') != expression.count('>') or expression.count('[') != expression.count(']') or expression.count('{') != expression.count('}') or expression.count('(.') != expression.count('.)'):
                pass
            if expression[position] == '(':
                if expression[position + 1] == '.':
                    closeSemantic = expression[position:].find('.)')
                    if closeSemantic + position == len(expression) - 2 and inLoop == False:
                        self.tabs = 2
                        if firstIf or self.continuarL:
                            file.write('\n' + '\t\telse:\n\t' + '\t\tprint("Error")\n\t' + '\t\tquit()')
                            firstIf = False
                            self.continuarL = False
                        semantics = expression[position + 2:position + closeSemantic].split(chr(92) + chr(110))
                        for sem in semantics:file.write('\n' + '\t' * self.tabs + sem)
                        position += closeSemantic + 2
                        continue
                    else:
                        semantics = expression[position + 2:position + closeSemantic].split(chr(92) + chr(110))
                        for sem in semantics:file.write('\n' + '\t' * self.tabs + sem)
                        position += closeSemantic + 2
                        continue
                else:
                    orOps = 0
                    exp = self.jalar_subgrupo(expression[position:], '(', ')')
                    self.analizeExpression(file, exp, orOps, firstIf, True)
                    position += len(exp)
                    subs = exp.split('|')

            elif expression[position] == '{':
                orOps = 0
                primeros = ''
                exp = self.jalar_subgrupo(expression[position:], '{', '}')
                subs = exp.split('|')
                hasProd = False
                for i in subs:
                    prim = self.primero(0, i, True)
                    for j in self.productions:
                        if prim.find(j.id) != -1:
                            firsts = ''
                            for k in j.primeros:firsts += "'" + k + "',"
                            firsts = firsts[:-1]
                            prim = prim.replace(j.id, firsts)
                            hasProd = True
                            break
                    if hasProd:primeros += prim
                    else:primeros += "'" + prim + "',"
                if hasProd == False:primeros = primeros[:-1]
                file.write('\n' + '\t' * self.tabs + 'while self.token_presente in [' + primeros + ']:')
                self.tabs += 1
                position += 1
                continue
            elif expression[position] == '[':
                orOps = 0
                exp = self.jalar_subgrupo(expression[position:], '[', ']')
                self.analizeExpression(file, exp, orOps, firstIf, True)
                position += len(exp)
                subs = exp.split('|')
            elif expression[position] == '|':
                inOr = 'el'
                self.tabs -= orOps
                orOps = 0
                position += 1
                continue
            elif expression[position] in [')', '}', ']']:
                self.tabs -= 1
                if expression[position] != ']':
                    file.write('\n' + '\t' * self.tabs + 'else:\n\t' + '\t' * self.tabs + 'print("Error")\n\t' + '\t' * self.tabs + 'quit()')
                self.orOps = 0
                position += 1
                continue
            else:
                found = False
                positioned = False
                for i in self.productions:
                    if expression[position:].find(i.id) == 0:
                        primeros = ''
                        for j in i.primeros:
                            primeros += "'" + j + "',"
                        primeros = primeros[:-1]
                        file.write('\n' + '\t' * self.tabs + 'if self.token_presente in [' + primeros + ']:')
                        if self.tabs == 2:
                            firstIf = True
                            if inLoop:self.continuarL = True
                        self.tabs += 1
                        orOps += 1
                        params = ''
                        code = '\n' + '\t' * self.tabs
                        if expression[position + len(i.id)] == '<':
                            params = self.jalar_subgrupo(expression[position + len(i.id):], '<', '>')
                            code += params + ' = '
                            positioned = True
                            position += expression[position:].find('<') + len(params) + 1
                        code += 'self.' + i.id + '(' + params + ')'
                        file.write(code)
                        if positioned == False:position += len(i.id) - 1
                        found = True
                        break
                if found == False:
                    if expression[position] == '"':
                        anonCLose = expression[position + 1:].find('"')
                        anonym = expression[position + 1:position + 1 + anonCLose]
                        for i in self.token2:
                            if i.id == anonym:
                                code = '\n' + '\t' * self.tabs + inOr + "if self.token_presente == '" + anonym + "':"
                                file.write(code)
                                if self.tabs == 2:
                                    firstIf = True
                                    if inLoop:self.continuarL = True
                                self.tabs += 1
                                orOps += 1
                                file.write('\n' + '\t' * self.tabs + 'self.mover()')
                                position += len(anonym) + 1
                    else:
                        for i in self.tokens:
                            if expression[position:].find(i.id) == 0:
                                file.write('\n' + '\t' * self.tabs + 'self.mover()')
            if inOr != '':
                inOr = ''
            position += 1

    def analizeProductions(self, file):
        file.write('''
import pickle
class Parser(object):

	def __init__(self, tokens, valores):
# -----------------------------------------------------------
		self.tokens = tokens
		self.valores = valores
# -----------------------------------------------------------
# -----------------------------------------------------------		
		self.token_presente = tokens[0]
		self.tokenFF = tokens[0]
# -----------------------------------------------------------
# -----------------------------------------------------------		
		self.valor_presente = valores[0]
		self.valor_tokenF = valores[0]
# -----------------------------------------------------------		
		self.index = 0
# -----------------------------------------------------------			
		self.tokens.pop()
		self.valores.pop()''')
        file.write('\n\t\tself.' + self.productions[0].id + '()')
        file.write('''

	def mover(self):
		self.index += 1
		if (self.index < len(self.tokens)):
			self.tokenFF = self.token_presente
			self.valor_tokenF = self.valor_presente
			self.token_presente = self.tokens[self.index]
			self.valor_presente = self.valores[self.index]
		else:
			quit()
        
        ''')
        for i in self.productions:
            self.tabs = 1
            parameters = ''
            if len(i.params) > 0:
                parameters += ', ' + i.params
            file.write('\n\n\tdef ' + i.id + '(self' + parameters + '):')
            self.tabs += 1
            self.analizeExpression(file, i.value, 0)
            file.write('\n\t\treturn ' + (parameters.replace(', ', '')))

        file.write('''

with open('archivoConTokens.bin', 'rb') as f:
    t = pickle.load(f).split(' ')

with open('archivoConValores.bin', 'rb') as f:
    v = pickle.load(f).split(' ')
parser = Parser(t, v)
        
        ''')

    def primero(self, index, production, search=False):
        semCount = production.count('(.')
        while semCount > 0:
            semStart = production.find('(.')
            semEnd = production.find('.)')
            semantic = production[semStart:semEnd + 2]
            production = production.replace(semantic, '')
            semCount -= 1
            # production = production.replace('(', ' (')
            # production = production.replace('{', ' {')
        production = production.replace('(', ' (')
        production = production.replace('{', ' {')
        production = production.replace('[', ' [')
        production = production.replace('" ', '"')
        # production = production.replace('[', ' [')
        # production = production.replace('" ', '"')
        subs = production.split(' ')
        subs = [x for x in subs if x]
        prodFirst = False
        if subs[0][0] != '{' and subs[0][0] != '[':
            prodFirst = True
        subProd = []
        sub = ''
        for i in subs:
            if i[0] == '(':
                ####production = production.replace('[', ' [')
                # -------------- pRUEBA
                sub = self.jalar_subgrupo(i, '(', ')')
            elif i[0] == '{':
                sub = self.jalar_subgrupo(i, '{', '}')
            elif i[0] == '[':
                ####production = production.replace('[', ' [')
                # -------------- PRUEBA
                #sub = self.jalar_subgrupo(i, '[', ']')
                sub = self.jalar_subgrupo(i, '[', ']')
            else:
                sub = i
            subProd += sub.split('|')

        for sub in subProd:
            found = False
            for i in self.tokens:
                if sub.find(i.id) == 0:
                    if search == False:
                        self.productions[index].primeros.append(i.id)
                    else:
                        return i.id
                    found = True
                    break
            if found == True:
                if prodFirst:
                    break
                continue
            if sub[0] == '"':
                for i in self.token2:
                    if sub[1:].find(i.id) == 0:
                        if search == False:self.productions[index].primeros.append(i.id)
                        else:return i.id
                        found = True
                        break
            if found == True:
                if prodFirst:break
                continue
            for i in self.productions:
                if sub.find(i.id) == 0:
                    if search == False:
                        self.productions[index].primeros.append(i.id)
                    else:return i.id
                    found = True
                    break
            if found == True:
                if prodFirst:
                    break
                continue

    def jalar_subgrupo(self, exp, op, closeOp):
        expression = ''
        pCount = 1
        lastFound = 1
        done = False
        while done == False:
            closeP = exp.find(closeOp, lastFound)
            parens = exp[:closeP].count(op)
            if parens > pCount:
                pCount = parens
                lastFound = exp.find(closeOp, closeP + 1)
            else:
                expression = exp[1:closeP]
                done = True
        return expression
