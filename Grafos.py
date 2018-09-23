from uuid import uuid4
class Nodo:
    def __init__(self, i, dato, padre=None):
        self.i = i
        self.dato = dato
        self.padre = padre

    def __repr__(self):
        return f'<{self.dato, self.i}>'

#Suple las carencias de Nodo, pudiendo añadir hijos y con identificador único
class NodoH(Nodo):
    def __init__(self, i, dato, padre=None, hijos=[]):
        super().__init__(i, dato, padre)
        self.hijos = hijos
        self.uuid = uuid4()

    def set_hijos(self, hijos):
        if len(self.hijos) > 0:
            self.hijos.extend(hijos)
        else: self.hijos = hijos
        for hijo in hijos:
            hijo.padre = self

    def root(self):
        aux = self.padre
        while (aux.padre != None):
            aux = aux.padre
        return aux

class NodoP1(NodoH):
    def __init__(self, i, dato, padre=None, hijos=[]):
        super().__init__(i, dato, padre, hijos)
        self.n = self.dato[0]
        if self.dato[1] : self.color = 'Blanco' #True representa el color Blanco y vcv
        else: self.color = 'Negro'

    def __repr__(self):
        return f'<{self.color}, {self.n}>'

