
import pickle
class Parser(object):

	def __init__(self, tokens, valores):
# -----------------------------------------------------------
		self.tokens = tokens
		self.valores = valores
# -----------------------------------------------------------
# -----------------------------------------------------------		
		self.currentToken = tokens[0]
		self.lastToken = tokens[0]
# -----------------------------------------------------------
# -----------------------------------------------------------		
		self.currentTokenValue = valores[0]
		self.lastTokenValue = valores[0]
# -----------------------------------------------------------		
		self.index = 0

		self.tokens.pop()
		self.valores.pop()
		self.EstadoInicial()

	def getNext(self):
		self.index += 1
		if (self.index < len(self.tokens)):
			self.lastToken = self.currentToken
			self.lastTokenValue = self.currentTokenValue
			self.currentToken = self.tokens[self.index]
			self.currentTokenValue = self.valores[self.index]
		else:
			quit()
        
        

	def EstadoInicial(self):
		while self.currentToken in ['-','(','numero']:
			if self.currentToken in ['-','(','numero']:
				self.Instruccion()
				if self.currentToken == ';':
					self.getNext()
				else:
					print("Error")
					quit()
		return 

	def Instruccion(self):
		resultado=0
		if self.currentToken in ['-','(','numero']:
			resultado = self.Expresion(resultado)
		else:
			print("Error")
			quit()
		print('Resultado:',resultado)
		return 

	def Expresion(self, resultado):
		resultado1=0;resultado2=0
		if self.currentToken in ['-','(','numero']:
			resultado1 = self.Termino(resultado1)
			while self.currentToken in ['+','-']:
				if self.currentToken == '+':
					self.getNext()
					if self.currentToken in ['-','(','numero']:
						resultado2 = self.Termino(resultado2)
						resultado1+=resultado2
				elif self.currentToken == '-':
					self.getNext()
					if self.currentToken in ['-','(','numero']:
						resultado2 = self.Termino(resultado2)
						resultado1-=resultado2
					else:
						print("Error")
						quit()
		else:
			print("Error")
			quit()
		resultado=resultado1
		return resultado

	def Termino(self, resultado):
		resultado1=0;resultado2=0
		if self.currentToken in ['-','(','numero']:
			resultado1 = self.Factor(resultado1)
			while self.currentToken in ['*','/']:
				if self.currentToken == '*':
					self.getNext()
					if self.currentToken in ['-','(','numero']:
						resultado2 = self.Factor(resultado2)
						resultado1*=resultado2
				elif self.currentToken == '/':
					self.getNext()
					if self.currentToken in ['-','(','numero']:
						resultado2 = self.Factor(resultado2)
						resultado1/=resultado2
					else:
						print("Error")
						quit()
		else:
			print("Error")
			quit()
		resultado=resultado1
		return resultado

	def Factor(self, resultado):
		signo=1
		if self.currentToken == '-':
			self.getNext()
			signo=-1
		if self.currentToken in ['numero']:
			resultado = self.Number(resultado)
		elif self.currentToken == '(':
			self.getNext()
			if self.currentToken in ['-','(','numero']:
				resultado = self.Expresion(resultado)
				if self.currentToken == ')':
					self.getNext()
				else:
					print("Error")
					quit()
		else:
			print("Error")
			quit()
		resultado*=signo
		return resultado

	def Number(self, resultado):
		self.getNext()
		resultado=float(self.lastTokenValue)
		return resultado

with open('scannedTokens.bin', 'rb') as f:
    t = pickle.load(f).split(' ')

with open('scannedValues.bin', 'rb') as f:
    v = pickle.load(f).split(' ')
parser = Parser(t, v)
        
        