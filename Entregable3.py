from Grafos import NodoH
from Plot_tree import draw_tree_non_rec, draw_several_non_rec
from math import sqrt, pow
import copy
import emoji
'''
   [ [    ][ 'R' ] ]
   [ [    ][     ] ]
   [ ['G' ][     ] ]
   Izq
   Derecha
   Arriba
   Abajo
'''
movim = {'Izquierda': (0, -1),
                  'Derecha': (0, 1),
                  'Arriba': (-1, 0),
                  'Abajo': (1, 0)}


class Tablero():
    def __init__(self, gato = (0,0), raton = (2,1)):
        self.tablero = [['     ' for _ in range(2)] for _ in range(3)]
        self.gato_pos = gato
        self.raton_pos = raton
        x_gato, y_gato = self.gato_pos
        x_raton, y_raton = self.raton_pos
        self.tablero[x_gato][y_gato] = emoji.emojize(':cat:')
        self.tablero[x_raton][y_raton] = emoji.emojize(':mouse:')
        self.win_max = False


    def __repr__(self):
        return f'{self.tablero[0]}\n{self.tablero[1]}\n{self.tablero[2]}'

    def aplicar_mov(self, player, new_pos):
        try:
            if new_pos[0] < 0 or new_pos[1] < 0: raise ValueError
            if self.win_max:
                return False
            if player == 1:
                player = self.gato_pos
                if emoji.emojize(':mouse:') == self.tablero[new_pos[0]][new_pos[1]]:
                    self.tablero[self.gato_pos[0]][self.gato_pos[1]] = '     '
                    self.tablero[new_pos[0]][new_pos[1]] = emoji.emojize(':skull:')
                    self.raton_pos = new_pos
                    self.gato_pos = new_pos

                    self.win_max = True
                    return True
                else:
                    self.tablero[player[0]][player[1]] = '     '
                    self.tablero[new_pos[0]][new_pos[1]] = emoji.emojize(':cat:')
                    self.gato_pos = new_pos
                    return True

            elif player == -1:
                player = self.raton_pos
                if emoji.emojize(':cat:') == self.tablero[new_pos[0]][new_pos[1]]:
                    #Se SUICIDA el ratón jaja
                    return False
                else:
                    self.tablero[player[0]][player[1]] = '     '
                    self.tablero[new_pos[0]][new_pos[1]] = emoji.emojize(':mouse:')
                    self.raton_pos = new_pos
                    return True

        except Exception as e:
            return False

    def h(self):
        try:
            return round(1 / sqrt(pow(self.gato_pos[0] - self.raton_pos[0],2) + pow(self.gato_pos[1] - self.raton_pos[1], 2)),2)
        except ZeroDivisionError as e:
            # G y R apuntan a la misma casilla
            return 10


class Estado(NodoH):
    def __init__(self, i, tablero : Tablero, jugador, hijos=[], padre=None, coste=0, mov_previo=''):
        super().__init__(i, tablero, padre, hijos)
        self.tablero = self.dato
        self.jugador = jugador
        self.win_max = self.tablero.win_max
        self.mov_previo = mov_previo


    def aplicar_mov(self, movimiento = movim):
        nuevos_estados = list()
        for key,mov in movimiento.items():
            pos = self.tablero.gato_pos if self.jugador == 1 else self.tablero.raton_pos
            coord = tuple(sum(x) for x in zip(pos, mov))

            aux_tablero = copy.deepcopy(self.tablero)
            if aux_tablero.aplicar_mov(self.jugador, coord):

                nuevos_estados.append(Estado(self.i+1, aux_tablero, -self.jugador, mov_previo=key))
        self.set_hijos(nuevos_estados)

    def __repr__(self):
        if self.win_max:
            return emoji.emojize('Ratón :skull:') + '\n h(estado) = 10'

        kw,jug = ("MIN:","Ratón") if self.jugador == -1 else ("MAX:","Gato")

        if self.coste == 0 or len(self.hijos) == 0:
            return f'Turno de {jug}\n {self.tablero}\n h(estado)={self.tablero.h()}'

        return f'Turno de {jug}\n{self.tablero}\n' \
               f'h(estado)= {self.tablero.h()}\n' \
               f'{kw}={self.coste}' \



def explore(movim = movim):
    nodo = Estado(0, Tablero(), 1) #Estado Inicial
    frontera = [nodo]
    while len(frontera) > 0:
        explorando = frontera.pop(0)

        if explorando.i == 4:
            return explorando

        else:
            explorando.aplicar_mov(movim)
            for hijo in explorando.hijos:
                frontera.append(hijo)


def negmax(nodo : Estado, limite = 5):
    if limite == 0 or nodo.i == 4:
        nodo.coste = 0
        return nodo.tablero.h() * nodo.jugador
    valor = -9999999
    for hijo in nodo.hijos:
        valor = max(valor, -negmax(hijo, limite-1))
    nodo.coste = abs(valor)
    return valor

def negmax_ab(nodo : Estado, limite, alpha, beta, movimiento = movim):
    if limite == 0:
        nodo.coste = nodo.tablero.h() * nodo.jugador
        return nodo.coste
    nodo.aplicar_mov(movimiento)
    if len(nodo.hijos) == 0:
        nodo.coste = nodo.tablero.h() * nodo.jugador
        return nodo.coste

    valor = -9999999

    for hijo in nodo.hijos:
        valor = max(valor, -negmax_ab(hijo, limite-1, -beta, -alpha, movimiento))
        alpha = max(alpha, valor)
        if alpha >= beta:
            break
    nodo.coste = abs(valor)
    return valor


def limpiar(nodo : Estado):
    for hijo in nodo.hijos[:]:
        if hijo.coste == 0 and not hijo.win_max:
            nodo.hijos.remove(hijo)
    for hijo in nodo.hijos:
        limpiar(hijo)


def apartado_a():
    nodo = explore().root()
    draw_tree_non_rec('Apartado A', nodo)
    return nodo


def apartado_b():
    nodo = explore().root()
    negmax(nodo, 4)
    draw_tree_non_rec('Apartado B', nodo)


def apartado_c():
    nodo = Estado(0, Tablero(), 1)
    negmax_ab(nodo, 4, -9999999, 9999999)
    limpiar(nodo)
    draw_tree_non_rec('Apartado C', nodo)


def apartado_d():
    nodo = Estado(0, Tablero(), 1)
    movim2 = {
             'Abajo': (1, 0),
             'Derecha': (0, 1),
             'Arriba': (-1, 0),
        'Izquierda': (0, -1)}
    negmax_ab(nodo, 4, -9999999, 9999999, movim2)

    draw_tree_non_rec('Apartado D', nodo)


#apartado_a()
#apartado_b()
#apartado_c()
#apartado_d()
ab = explore(movim={
             'Abajo': (1, 0),
             'Derecha': (0, 1),
             'Arriba': (-1, 0),
        'Izquierda': (0, -1)}).root()
draw_tree_non_rec('Apartado D1', ab)



