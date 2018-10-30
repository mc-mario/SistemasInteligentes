from Grafos import NodoND
from Plot_tree import draw_tree
class Clausula():

    def __init__(self, terminos):
        self.terminos = terminos

    def check(self, table):
        aux = list()
        for enum, elem in enumerate(table,1):
            termino = self.terminos.get(str(enum), None)
            if termino is not None:
                if termino == '':
                   aux.append(elem)
                else:
                    aux.append(not elem if elem is not None else None)
        return any(aux)
    def __repr__(self):
        aux = ''
        for key, elem in self.terminos.items():
            aux += str(elem) + 'x' + str(key) + ' v '
        aux = aux.rstrip('v ')
        return f'( {aux} )'

class Predicado():
    def __init__(self, clausulas_en_lista):
        if type(clausulas_en_lista[0]) is Clausula:
            self.clausulas = clausulas_en_lista
        else:
            self.clausulas = [Clausula(terminos) for terminos in clausulas_en_lista]

    def check(self,table):
        num_cl = sum(filter(lambda x : x is True, [clausula.check(table) for clausula in self.clausulas]))
        condit = all([clausula.check(table) for clausula in self.clausulas])
        return num_cl, condit

    def __repr__(self):
        return f'{" ^ ".join(str(clausula) for clausula in self.clausulas)}'


class Estado(NodoND):
    def __init__(self,num_terminos,tabla = None, i=0, padre=None, hijos=[], mov_previo=None):
        super().__init__(i, padre, hijos)
        if tabla is None:
            self.tabla = [None for _ in range(num_terminos)]
        else:
            self.tabla = tabla
        self.mov_previo = mov_previo

    def aplicar_mov(self):
        if self.i+1 > len(self.tabla): return
        hijos = list()
        for elem in [True,False]:
            aux = self.tabla[:]
            aux[self.i] = elem
            hijos.append(Estado(len(aux), aux, self.i+1, self.padre, mov_previo=elem))
        self.set_hijos(hijos)

    def __repr__(self, predicado=None):
        return f"{list(map(lambda x : 'T' if x else 'F' if x is False else 'N' if x is None else '', self.tabla))}"


def explore():
    win = [{'1': '', '2': '¬'}, {'1': '¬', '3': '¬'}, {'4': '', '5': '¬'}, {'2': '', '5': ''}, {'3': '', '4': ''}]
    ej1 = Predicado(win)
    es = Estado(5)
    frontera = [es]
    while len(frontera) > 0:
        actual = frontera.pop(0)
        num_cl, condit = ej1.check(actual.tabla)
        if condit: return actual
        actual.aplicar_mov()
        for hijo in actual.hijos:
            frontera.append(hijo)
        #frontera = sorted(frontera, key=lambda x: ej1.check(x.tabla)[1] + x.i, reverse=True)

    return None

aux = explore()
draw_tree('Boloñesa', aux)
