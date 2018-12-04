from Grafos import NodoH


# (3,3,0) - Canibales, Misioneros, Barco
class NodoBarco(NodoH):
    def __init__(self, i , dato, padre=None, hijos=[]):
        super().__init__(i, dato, padre, hijos)
        self.canibales = self.dato[0]
        self.misioneros = self.dato[1]
        self.barco = self.dato[2]

    def __repr__(self):
        return f'<C: {3-self.canibales}  M:{3-self.misioneros} -{"Barco Izq" if self.barco == 0 else "Barco Der"}- C:{self.canibales}  M:{self.misioneros}>'

    def __str__(self):
        return f'<C: {3-self.canibales}  M:{3-self.misioneros}  C:{self.canibales}  M:{self.misioneros}>'


def exp_frontera(padre : NodoBarco):
    i = padre.i
    canibales_der = padre.canibales
    misioneros_der = padre.misioneros
    barco = padre.barco
    print(padre)
    frontera = list()
    if barco == 1:
        if canibales_der - 1 > -1:
            frontera.append(NodoBarco(i + 1, (canibales_der -1, misioneros_der, 0), padre=padre))
        if canibales_der - 2 > -1:
            frontera.append(NodoBarco(i + 1, (canibales_der -2, misioneros_der, 0), padre=padre))
        if canibales_der - 1 > -1 and misioneros_der - 1 > -1:
            frontera.append(NodoBarco(i + 1, (canibales_der - 1, misioneros_der -1, 0), padre=padre))
        if misioneros_der - 1 > -1:
            frontera.append(NodoBarco(i + 1, (canibales_der, misioneros_der - 1, 0), padre=padre))
        if misioneros_der - 2 > -1:
            frontera.append(NodoBarco(i + 1, (canibales_der, misioneros_der - 2, 0), padre=padre))

    else:

        if canibales_der + 1 < 4:
            frontera.append(NodoBarco(i + 1, (canibales_der +1, misioneros_der, 1), padre=padre))
        if canibales_der + 2 < 4:
            frontera.append(NodoBarco(i + 1, (canibales_der +2, misioneros_der, 1), padre=padre))
        if canibales_der + 1 < 4 and misioneros_der + 1 < 4:
            frontera.append(NodoBarco(i + 1, (canibales_der + 1, misioneros_der +1, 1), padre=padre))
        if misioneros_der + 1 < 4:
            frontera.append(NodoBarco(i + 1, (canibales_der, misioneros_der + 1, 1), padre=padre))
        if misioneros_der + 2 < 4:
            frontera.append(NodoBarco(i + 1, (canibales_der, misioneros_der + 2, 1), padre=padre))

    for elem in frontera[:]:
        dato = elem.dato
        canibales_izq = 3 - dato[0]
        misioneros_izq = 3 - dato[1]
        canibales_der = dato[0] - 0
        misioneros_der = dato[1] - 0
        if canibales_izq >  misioneros_izq and misioneros_izq != 0:
            frontera.remove(elem)
        if canibales_der > misioneros_der and misioneros_der != 0:
            frontera.remove(elem)



    return frontera



def solve_profundidad_barco():
    n = NodoBarco(0, (3,3,1))
    frontera = [n]
    visitados = list()
    while len(frontera) > 0:
        nodo_actual = frontera.pop(0)
        dato = nodo_actual.dato
        if dato == (0,0,1) or dato == (0,0,0):
            return nodo_actual
        print(dato)


        if dato not in visitados:
            visitados.append(dato)
        else:
            continue

        hijos = exp_frontera(nodo_actual)
        nodo_actual.set_hijos(hijos)
        frontera.extend(hijos)
    return n




