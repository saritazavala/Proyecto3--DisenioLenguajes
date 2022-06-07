"""
UNIVERSIDAD DEL VALLE DE GUATEMALA
LENGUAJES DE PROGRAMACION
SARA NOHEMI ZAVALA GUTIERREZ
"""

class Caracteres(object):
    def __init__(self, id, alphabet):
        self.id = id
        self.alphabet = alphabet

class Keywords(object):
    def __init__(self, id, value):
        self.id = id
        self.value = value


class Token(object):
    def __init__(self, id, value):
        self.id = id
        self.value = value

class Node(object):
    def __init__(self, state, transitions, accepted):
        self.state = state
        self.transitions = transitions
        self.accepted = accepted

class Production(object):
    def __init__(self, id, params, value):
        self.id = id
        self.params = params
        self.value = value
        self.primeros = []