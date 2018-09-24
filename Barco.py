from Grafos import NodoH


# (3,3,0) - Canibales, Misioneros, Barco
class NodoBarco(NodoH):
    def __init__(self, i , dato, padre=None, hijos=[]):
        super().__init__(i, dato, padre, hijos)
        self.canibales = self.dato[0]
        self.misioneros = self.dato[1]
        self.barco = self.dato[2]

    def __repr__(self):
        return f' IZQ: {3-self.canibales}C {3-self.misioneros}M -{"Izq" if self.barco == 0 else "Der"}- DER: {self.canibales}C {self.misioneros}M '

print(NodoBarco(0, (3,3,1)))

def exp_frontera(padre : NodoBarco):
    canibales_der = padre.canibales
    misioneros_der = padre.misioneros

    if canibales_der > 3 or canibales_der < 0: return []
    if misioneros_der > 3 or misioneros_der < 0 : return []

    barco = padre.barco
    frontera = list()


    if barco == 1:
        if canibales_der >= 1:
            frontera.append(NodoBarco(padre.i + 1, (canibales_der - 1, misioneros_der, 0), NodoBarco))
        if canibales_der >= 2:
            frontera.append(NodoBarco(padre.i + 1, (canibales_der - 2, misioneros_der, 0), NodoBarco))
        if misioneros_der >= 1:
            frontera.append(NodoBarco(padre.i + 1, (canibales_der, misioneros_der-1, 0), NodoBarco))
        if misioneros_der >= 2:
            frontera.append(NodoBarco(padre.i + 1, (canibales_der, misioneros_der-2, 0), NodoBarco))
        if misioneros_der >= 1 and canibales_der >= 1:
            frontera.append(NodoBarco(padre.i + 1, (canibales_der - 1, misioneros_der -1, 0), NodoBarco))

    if barco == 0:
        if canibales_der >= 1:
            frontera.append(NodoBarco(padre.i + 1, (canibales_der + 1, misioneros_der, 0), NodoBarco))
        if canibales_der >= 2:
            frontera.append(NodoBarco(padre.i + 1, (canibales_der + 2, misioneros_der, 0), NodoBarco))
        if misioneros_der >= 1:
            frontera.append(NodoBarco(padre.i + 1, (canibales_der, misioneros_der+1, 0), NodoBarco))
        if misioneros_der >= 2:
            frontera.append(NodoBarco(padre.i + 1, (canibales_der, misioneros_der+2, 0), NodoBarco))
        if misioneros_der >= 1 and canibales_der >= 1:
            frontera.append(NodoBarco(padre.i + 1, (canibales_der - 1, misioneros_der +1, 0), NodoBarco))
    print(frontera)
    return frontera



def solve_profundidad():
    frontera = [NodoBarco(0, (3,3,1))]
    while len(frontera) > 0:
        nodo_actual = frontera.pop(0)
        print(nodo_actual)
        if nodo_actual.dato == (0,0,1) or nodo_actual.dato == (0,0,0):
            return nodo_actual

        hijos = exp_frontera(nodo_actual)
        nodo_actual.set_hijos(hijos)
        frontera.extend(hijos)
    return None

x = solve_profundidad()
print(x)