from Grafos import NodoH
from Plot_tree import draw_tree_non_rec
import copy

class NodoMinMax(NodoH):
    def __init__(self, i, dato, jugador, valor=0, padre=None, hijos=[], coste=1):
        super().__init__(i, dato, padre, hijos, coste)
        self.valor = valor
        self.jugador = jugador # -1 Maquina 1 Jugador

    def real_valor(self):
        return self.valor * self.jugador

    def __repr__(self):
        return f'{"Maquina" if self.jugador == -1 else "Jugador"} \n {self.dato} {self.valor}'

def ramificar_rec(rama : NodoMinMax):
    sticks = rama.dato
    if sticks - 1 > -1:
        rama.set_hijos([NodoMinMax(rama.i + 1, sticks-1, -rama.jugador)])
    if sticks - 2 > -1:
        rama.set_hijos([NodoMinMax(rama.i + 1, sticks-2, -rama.jugador)])
    for hijo in rama.hijos:
        ramificar_rec(hijo)

def minmax(nodo : NodoMinMax):
    if len(nodo.hijos) == 0:
        if nodo.jugador == 1 :
            nodo.valor = nodo.jugador * 333
            return nodo.valor # Si no ramifica más, esto es nodo terminal
        if nodo.jugador == -1:
            nodo.valor = nodo.jugador * 999
            return nodo.valor
    valor = -9999999
    for hijo in nodo.hijos: #Exploramos los hijos
        valor = max(valor, -minmax(hijo))
    nodo.valor = abs(valor)
    return valor


sticks = 15
while True:

    #Maquina
    rama = NodoMinMax(0, sticks, jugador=-1)
    ramificar_rec(rama)
    minmax(rama)
    ch, val = max(enumerate(map(lambda x: x.valor, rama.hijos)))
    camino = rama.hijos[ch].dato
    print(f"{sticks} Maquina quita: {sticks - camino}")
    sticks = camino

    if sticks == 0:
        print('MAQUINA WINS')
        break

    #Dibujar árlbol de decisiones
    #draw_tree_non_rec('11 Sticks', rama)

    #Player
    eleccion = int(input(f"{sticks} Left. Your TURN! Draw 1 or 2"))
    sticks -= eleccion

    if sticks == 0:
        print("YOU WIN")
        break


class Tres_en_raya():
    def __init__(self):
        self.tablero = [[' ' for _ in range(3)] for _ in range(3)]

    # True si se realiza la jugada
    def jugada(self, pieza, x, y):
        try:
            if self.tablero[x][y] == ' ':
                self.tablero[x][y] = pieza
                return True
            return False
        except Exception as e:
            return False

    ''' Representación
        ['O', 'O', ' ']
        [' ', 'X', ' ']
        [' ', 'X', 'X']
    '''
    def __repr__(self):
        return f'{self.tablero[0]}\n{self.tablero[1]}\n{self.tablero[2]}'

    def winner(self):
        for x in range(3):
            if self.tablero[x].count(self.tablero[x][0]) == len(self.tablero[x]) and self.tablero[x][0] != ' ': return self.tablero[x][0]
            if self.tablero[0][x] == self.tablero[1][x] == self.tablero[2][x] != ' ': return self.tablero[0][x]
        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] != ' ': return self.tablero[0][0]
        if self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] != ' ': return self.tablero[0][2]
        if len(list(filter(lambda x : x is True, map(lambda x : x.count(' ') == 0, self.tablero)))) == 3 : return 'Empate'
        return 'Not finished'

class NodoTresRayas(NodoH):
    def __init__(self, i, dato : Tres_en_raya, jugador, padre=None, hijos=[]):
        super().__init__(i, dato, padre, hijos)
        self.tablero = dato
        self.jugador = jugador # 1 Jugador -1 Maquina

    def __repr__(self):
        return f'{self.tablero}'

def ramificar_ter(nodo : NodoTresRayas, limite=3):

    tablero = nodo.tablero
    jugador = 'X' if nodo.jugador == 1 else 'O'
    jugadas = list()
    if limite == 0: return
    if tablero.winner() != 'Not finished': return
    for i in range(3):
        for j in range(3):
            nodo_copia = copy.deepcopy(nodo)
            tablero_copia = nodo_copia.tablero
            if tablero_copia.jugada(jugador, i, j):
                jugadas.append(NodoTresRayas(nodo.i +1, tablero_copia, -nodo.jugador, nodo))
    nodo.set_hijos(jugadas)
    for hijo in nodo.hijos:
        ramificar_ter(hijo, limite-1)

Tablero_Inicial = Tres_en_raya()
Nodo_Inicial = NodoTresRayas(0, Tablero_Inicial, -1)
ramificar_ter(Nodo_Inicial)
draw_tree_non_rec('Tres En Raya', Nodo_Inicial)





import random
#
# while True:
#     print(inicio.tablero)
#     x,y = input('X Y').split(' ')
#
#     if inicio.tablero.jugada('X',int(x), int(y)):
#         if inicio.tablero.winner() is not None:
#             inicio.tablero.winner()
#             break
#
#         print('Movimiento aceptado')
#         print('calculando jugada...')
#
#
#
