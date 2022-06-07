"""
UNIVERSIDAD DEL VALLE DE GUATEMALA
LENGUAJES DE PROGRAMACION
SARA NOHEMI ZAVALA GUTIERREZ
"""
from AnalizadorLexico import *
from CrearSP import Producir_utils

# Lectura ATG
try:
    atg = open(input("Ingrese archivo ATG --> "))
    atg_read = atg.readlines()
    ###############

    #### Analizador Lexico
    analizar_archivo(atg_read)
    tokens, keywords, characters, productions, tokens_2 = get_data()
    ########

    #### Genera el Parser y el Scanner
    Producir_utils(tokens, keywords, characters, tokens_2, productions)
except:
    print("Doc invalido")
