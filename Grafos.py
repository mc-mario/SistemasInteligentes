from uuid import uuid4
class Nodo:
    def __init__(self, n, level, es_blanco, padre=None):
        self.n = n
        self.level = level
        self.color = 'Blanco' if es_blanco else 'Negro'
        self.padre = padre

    def __repr__(self):
        return f'<{self.color, self.n}>'

class NodoH(Nodo):

    def __init__(self, n, es_blanco, level=0, padre=None, hijos=[]):
        super().__init__(n, es_blanco, level , padre)
        self.hijos = hijos
        self.uuid = uuid4()

    def set_hijos(self, hijos):
        self.hijos = hijos
        for hijo in self.hijos:
            hijo.padre = self

    def root(self):
        aux = self.padre
        while (aux.padre != None):
            aux = aux.padre
        return aux


def rec(n : NodoH, limit = 3):
    n.hijos = [NodoH(index, True, n) for index in range(2)]
    for hijo in n.hijos:
        if limit > 0:
            print(limit)
            rec(hijo, limit - 1)





