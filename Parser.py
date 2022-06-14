
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
		self.valores.pop()
		self.EstadoInicial()

	def mover(self):
		self.index += 1
		if (self.index < len(self.tokens)):
			self.tokenFF = self.token_presente
			self.valor_tokenF = self.valor_presente
			self.token_presente = self.tokens[self.index]
			self.valor_presente = self.valores[self.index]
		else:
			quit()
        
        

	def EstadoInicial(self):
		while self.token_presente in ['numeroToken']:
			if self.token_presente in ['numeroToken']:
				self.Instruccion()
				if self.token_presente == ';':
					self.mover()
				else:
					print("Error")
					quit()
		return 

	def Instruccion(self):
		resultado=0
		if self.token_presente in ['numeroToken']:
			resultado = self.Expresion(resultado)
		else:
			print("Error")
			quit()
		print("Resultado:",resultado)
		return 

	def Expresion(self, resultado):
		resultado1=0;resultado2=0
		if self.token_presente in ['numeroToken']:
			resultado1 = self.Termino(resultado1)
			while self.token_presente in ['-']:
				if self.token_presente == '-':
					self.mover()
					if self.token_presente in ['numeroToken']:
						resultado2 = self.Termino(resultado2)
						resultado1-=resultado2;print("Término:",resultado1)
					else:
						print("Error")
						quit()
		else:
			print("Error")
			quit()
		resultado=resultado1;print("Término:",resultado)
		return resultado

	def Termino(self, resultado):
		resultado1=0;resultado2=0
		if self.token_presente in ['numeroToken']:
			resultado1 = self.Factor(resultado1)
			while self.token_presente in ['/']:
				if self.token_presente == '/':
					self.mover()
					if self.token_presente in ['numeroToken']:
						resultado2 = self.Factor(resultado2)
						resultado1/=resultado2;print("Factor:",resultado1)
					else:
						print("Error")
						quit()
		else:
			print("Error")
			quit()
		resultado=resultado1;print("Factor:",resultado)
		return resultado

	def Factor(self, resultado):
		resultado1=0
		if self.token_presente in ['numeroToken']:
			resultado1 = self.Numero(resultado1)
		else:
			print("Error")
			quit()
		resultado=resultado1;print("Número:",resultado)
		return resultado

	def Numero(self, resultado):
		self.mover()
		resultado=float(self.valor_tokenF);print("Token:",resultado)
		return resultado

with open('archivoConTokens.bin', 'rb') as f:
    t = pickle.load(f).split(' ')

with open('archivoConValores.bin', 'rb') as f:
    v = pickle.load(f).split(' ')
parser = Parser(t, v)
        
        