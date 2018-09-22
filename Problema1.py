import random
from Grafos import NodoH
from utils import time_it

def make(n):
    return [True if random.randint(0,10) > 7 else False for n in range(n)]

def make_ejemplo():
    return [True,False,True,True,True,False,True,True,False,True,False,True,True,False,False,True]

def solve_anchura(lab = make_ejemplo()):
    #print([f'Blanco {index+1}' if elem is True else f'Negro {index+1}' for index, elem in enumerate(lab)])
    #copia_lab = lab[:]

    nodo_inicial = NodoH(0, lab[0])

    frontera = list()
    frontera.append(nodo_inicial)

    visitados = list()

    while len(frontera) > 0:
        #nodo_actual = frontera.pop(-1) --> Profundidad
        nodo_actual = frontera.pop(0)
        n = nodo_actual.n

        hijos_actual = list() #Podriamos obtener los hijos con un mapa

        #if n in [nodo.n for nodo in visitados]:
        #    print('Ya visto')
        #    continue
        #else:
        #    visitados.append(nodo_actual)

        if n == len(lab) - 1:
            #print(' ----- En memoria, momento previo a encontrar solucion: ', frontera)
            return nodo_actual
        try:

            if nodo_actual.color == 'Blanco':
                hijos_actual.append(NodoH(n + 1, nodo_actual.level+1, lab[n + 1], nodo_actual))
                hijos_actual.append(NodoH(n + 2, nodo_actual.level+1, lab[n + 2], nodo_actual))

            else:
                hijos_actual.append(NodoH(n + 1, nodo_actual.level+1, lab[n + 1], nodo_actual))
                hijos_actual.append(NodoH(n + 4, nodo_actual.level+1, lab[n + 4], nodo_actual))

        except Exception as e:
            pass

        finally:
            nodo_actual.set_hijos(hijos_actual)
            frontera.extend(hijos_actual)

    return None

def solve_profundidad(lab=make_ejemplo(), limit=None):


    #print([f'Blanco {index+1}' if elem is True else f'Negro {index+1}' for index, elem in enumerate(lab)])


    nodo_inicial = NodoH(0, 0, lab[0])

    frontera = list()
    frontera.append(nodo_inicial)
    print(frontera, limit)
    visitados = list()

    while len(frontera) > 0:


        nodo_actual = frontera[-1]
        frontera = frontera[:-1]
        n = nodo_actual.n

        #print(f'--- {nodo_actual}', print(frontera), 'limite:', limit, 'level nodo actual:', n)

        if limit is not None:
            if limit < nodo_actual.level:
                continue

        hijos_actual = list() #Podriamos obtener los hijos con un mapa

        #if n in [nodo.n for nodo in visitados]:
        #    print('Ya visto')
        #    continue
        #else:
        #    visitados.append(nodo_actual)
        lena = nodo_actual.n
        if lena == len(lab) - 1:
            #print(' ----- En memoria, momento previo a encontrar solucion: ', frontera)
            return nodo_actual
        try:

            if nodo_actual.color == 'Blanco':
                hijos_actual.append(NodoH(n + 1, nodo_actual.level+1, lab[n + 1], padre=nodo_actual))
                hijos_actual.append(NodoH(n + 2, nodo_actual.level+1, lab[n + 2], padre=nodo_actual))

            else:
                hijos_actual.append(NodoH(n + 1, nodo_actual.level+1, lab[n + 1], padre=nodo_actual))
                hijos_actual.append(NodoH(n + 4, nodo_actual.level+1, lab[n + 4], padre=nodo_actual))

        except Exception as e:
            print(e)

        finally:
            nodo_actual.set_hijos(hijos_actual)
            frontera.extend(hijos_actual)

    return None


def solve_profundiad_limit(r=100):
    for num in range(r):
        sol = solve_profundidad(make_ejemplo(), limit=num)
        if sol is not None:
            return sol

def solve_laberinto_iter_dfs(n, ejemplo):
        if not ejemplo: lab = make(n)
        else: lab = make_ejemplo()
        print([f'Blanco {index+1}' if elem is True else f'Negro {index+1}' for index, elem in enumerate(lab)])
        #copia_lab = lab[:]

        nodo_inicial = NodoH(0, lab[0])

        frontera = list()
        frontera.append(nodo_inicial)

        visitados = list()

        def depth_search(limited):
            print('Accediendo nivel: ', limited)
            if limited > 0:
                nodo_actual = frontera.pop(-1)
                if nodo_actual.n == len(lab) - 1:
                    return nodo_actual
                #if nodo_actual.n in [nodo.n for nodo in visitados]:
                #    return None
                try:
                    if nodo_actual.color == 'Blanco':
                        n = nodo_actual.n
                        Nodo_a_1 = NodoH(n + 1, lab[n + 1], nodo_actual)
                        frontera.append(Nodo_a_1)
                        #Puede dar error
                        Nodo_a_2 = NodoH(n + 2, lab[n + 2], nodo_actual)
                        frontera.append(Nodo_a_2)
                    else:
                        n = nodo_actual.n
                        Nodo_a_1 = NodoH(n + 1, lab[n + 1], nodo_actual)
                        frontera.append(Nodo_a_1)
                                                    #Puede dar error
                        Nodo_a_4 = NodoH(n + 4, lab[n + 4], nodo_actual)
                        frontera.append(Nodo_a_4)
                    sol = depth_search(limited-1)
                    if sol != None: return
                except Exception as e:
                    pass
            return None
        for i in range(100):
            depth_search(i)

def tarea1(n, ejemplo=False):
    if not ejemplo:
        solucion = solve_anchura()
    else:
        solucion = solve_laberinto_iter_dfs(n, ejemplo)

    resultado = list()
    if solucion is None or solucion.padre is None:
        print(solucion, 'Sin solucion?')
        return
    resultado.append(solucion)
    while(solucion.padre != None):
        resultado.append(solucion.padre)
        solucion = solucion.padre


    resultado.reverse()
    return resultado

