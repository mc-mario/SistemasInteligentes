import random
from Grafos import NodoP1

# Laberintos aleatorios
def make(n):
    return [True if random.randint(0,10) > 6 else False for n in range(n)]

# Laberinto propuesto en el entregable
def make_ejemplo():
    return [True,False,True,True,True,False,True,True,False,True,False,True,True,False,False,True]

# Este método lo tengo para poder abstraer un poco la lógica
# de profundidad y anchura para adaptar a otros ejercicios estos algoritmos.
# Añade el siguiente paso según el n -> (1, 2, 4), en caso de que falle
# significa que nos saltabamos la casilla final, no es solución
def frontera_entregable(frontera, lab, padre, n):
    try:
        hijo = NodoP1(padre.i+1, [padre.n+n, lab[padre.n+n]], padre=padre, coste=padre.coste+1)
        padre.set_hijos([hijo])
        frontera.append(hijo)
    except IndexError as e:
        pass

def solve_anchura(lab = make_ejemplo()):

    #Inicializamos la frontera con la casilla de salida
    frontera = [NodoP1(0, [0, lab[0]])]
    visitados = list()
    while len(frontera) > 0:
        nodo_actual = frontera.pop(0)
        n = nodo_actual.n
        # N no corresponde a la profundidad (esto es i) si no a la casilla dentro del problema a resolver
        if n not in visitados:
            visitados.append(n)
        else:
            continue
        # Si N es igual al tamaño de lab, hemos llegado a una solución
        if n == len(lab) - 1:
            return nodo_actual

        if nodo_actual.color == 'Blanco':
            frontera_entregable(frontera, lab, nodo_actual, 2)
            frontera_entregable(frontera, lab, nodo_actual, 1)


        else:
            frontera_entregable(frontera, lab, nodo_actual, 4)
            frontera_entregable(frontera, lab, nodo_actual, 1)

    return None #No hay solución

def solve_profundidad(lab=make_ejemplo(), limit=100):
    # La declaración de listas, llamadas iterativas y devolver la solución se encuentran debajo
    def frontera_iter(frontera, limite_max, iter=0):
        #Fin de la ramificación
        if len(frontera) == 0:
            return None

        nodo_actual = frontera.pop(-1)

        # Si N es igual al tamaño de lab, hemos llegado a una solución
        if nodo_actual.n == len(lab) - 1:
            return nodo_actual


        #Expandimos la frontera de manera iterativa, primero una rama y después la otra
        #Esto ocurre mientras que no se supere el límite y existan nodos que visitar en un rama
        if iter < limite_max:
            if nodo_actual.color == 'Blanco':
                frontera_entregable(frontera, lab, nodo_actual, 2)
                x = frontera_iter(frontera, limite_max, iter+1)
                if x is not None: return x
                #nodo_actual.hijos = []

                frontera_entregable(frontera, lab, nodo_actual, 1)
                x = frontera_iter(frontera, limite_max, iter + 1)
                if x is not None: return x


            if nodo_actual.color == 'Negro':
                frontera_entregable(frontera, lab, nodo_actual, 4)
                x = frontera_iter(frontera, limite_max, iter+1)
                if x is not None: return x
                #nodo_actual.hijos = []
                frontera_entregable(frontera, lab, nodo_actual, 2)
                x = frontera_iter(frontera, limite_max, iter+1)
                if x is not None: return x


    # Lógica iterativa
    for max in range(limit):
        frontera = [NodoP1(0, [0, lab[0]])]
        x = frontera_iter(frontera, max)
        if x is not None: return x
    return None

def solve_profundidad_no_iter(lab=make_ejemplo(), limit=100):
    def frontera_iter(frontera, limite_max, iter=0):
        # Fin de la ramificación
        if len(frontera) == 0:
            return None

        nodo_actual = frontera.pop(-1)

        # Si N es igual al tamaño de lab, hemos llegado a una solución
        if nodo_actual.n == len(lab) - 1:
            return nodo_actual

        # Expandimos la frontera de manera iterativa, primero una rama y después la otra
        # Esto ocurre mientras que no se supere el límite y existan nodos que visitar en un rama
        if iter < limite_max:
            if nodo_actual.color == 'Blanco':
                frontera_entregable(frontera, lab, nodo_actual, 2)
                frontera_entregable(frontera, lab, nodo_actual, 1)



                x = frontera_iter(frontera, limite_max, iter + 1)
                if x is not None: return x

            if nodo_actual.color == 'Negro':
                frontera_entregable(frontera, lab, nodo_actual, 4)
                frontera_entregable(frontera, lab, nodo_actual, 2)



                x = frontera_iter(frontera, limite_max, iter + 1)
                if x is not None: return x

    # Lógica iterativa
    for max in range(limit):
        frontera = [NodoP1(0, [0, lab[0]])]
        x = frontera_iter(frontera, max)
        if x is not None: return x
    return None

################Entregable 2
#Heurística para el Entregable 2
def h2(x: NodoP1, N = len(make_ejemplo()) ):
        if x.color == 'Negro':
            return min(abs(N - x.n - 4),abs(N - x.n - 1), N - x.n)
        if x.color == 'Blanco':
            return min(abs(N - x.n - 2),abs(N - x.n - 1), N - x.n)


def solve_bfs(lab=make_ejemplo()):


    frontera = [NodoP1(0, [0, lab[0]])]
    while len(frontera) > 0:
        nodo_actual = frontera.pop(0)
        print(nodo_actual)
        if nodo_actual.n == len(lab) -1:
            return nodo_actual

        if nodo_actual.color == 'Blanco':
            frontera_entregable(frontera, lab, nodo_actual, 2)
            frontera_entregable(frontera, lab, nodo_actual, 1)


        else:
            frontera_entregable(frontera, lab, nodo_actual, 4)
            frontera_entregable(frontera, lab, nodo_actual, 1)

        print(frontera)
        frontera.sort(key=lambda x : h2(x, len(lab)))
        print(frontera)

    return None

def solve_astar(lab=make_ejemplo()):
    frontera = [NodoP1(0, [0, lab[0]], coste=0)]

    while len(frontera) > 0:
        nodo_actual = frontera.pop(0)

        if nodo_actual.n == len(lab) - 1: return nodo_actual

        if nodo_actual.color == 'Blanco':
            frontera_entregable(frontera, lab, nodo_actual, 2)
            frontera_entregable(frontera, lab, nodo_actual, 1)

        if nodo_actual.color == 'Negro':
            frontera_entregable(frontera, lab, nodo_actual, 4)
            frontera_entregable(frontera, lab, nodo_actual, 1)

        print(nodo_actual, h2(nodo_actual) + nodo_actual.coste)
        frontera.sort(key=lambda x: h2(x, len(lab)) + x.coste)

    return None