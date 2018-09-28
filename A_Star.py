from Grafos import NodoAStar
import pygame, sys
import random

#Pygame
width, height = 1280, 720
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('A Star')
clock = pygame.time.Clock()

def tablero(n,m):
    tablero = list()
    for i in range(n):
        for j in range(m):
            est = False
            if random.randint(0,20) > 15: est = True
            tablero.append(NodoAStar(0,(i,j,est)))
    return tablero


tabler = tablero(49,27)

class Agente():
    def __init__(self, dato):
        self.x, self.y = dato
        self.color = (0,0,255)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x*26, self.y*26, 20,20))

class Premio(Agente):
    def __init__(self, dato):
        super().__init__(dato)
        self.color = (0,255,0)


premio = Premio((random.randint(0,40),(random.randint(0,40))))
agente = Agente((2,2))



def a_star(agente : Agente, premio : Premio):
    x, y = agente.x, agente.y
    x2, y2 = premio.x, premio.y
    tablero = tabler[:]
    #Camino de Manhattan
    def h(x,y): #
        return abs(x-x2 + y -y2)

    #Devuelve una lista de NodosGFB adyacentes a las coordenadas (x,y)
    def mirar_alrededor(x,y, tabler):
        mirar = lambda x,y: [elem for elem in tabler if x == elem.x and y == elem.y]
        alrededor = [mirar(x,y) for (x,y) in ((x+1,y),(x-1,y),(x,y-1),(x,y+1))]
        return [adyacente for casilla in alrededor for adyacente in casilla ]


    frontera = [NodoAStar(0,(x,y,False),h(x,y))]
    visitados = list()
    while len(frontera) > 0:
        elem = frontera.pop(0)

        if elem.x == x2 and elem.y == y2:
            return elem

        for a in mirar_alrededor(elem.x, elem.y, tablero):

            if not a.muro:
                if (a.x, a.y, a.coste) not in visitados:
                    a.padre = elem
                    a.coste = elem.coste + 1 + h(a.x, a.y)
                    visitados.append((a.x, a.y, a.coste))
                    frontera.append(a)

                else:
                    continue

        frontera = sorted(frontera,key= lambda nodo : nodo.coste)

    return None


        





sol = a_star(agente, premio)
while sol is None:
    tabler = tablero(30,30)
    sol = a_star(agente, premio)
while True:
    clock.tick(20)
    screen.fill((30,30,30))

    #Tablero
    for casilla in tabler:
        casilla.draw(screen, pygame)

    # Camino
    aux = sol
    i = 0
    while aux.padre != None:
        aux.draw(screen, pygame,(60,60,60))
        aux = aux.padre
        i += 1

    agente.draw()
    premio.draw()

    pygame.display.flip()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = map(lambda x: (x - (x % 26)) // 26, pos)

            for casilla in tabler:
                if casilla.x == x and casilla.y == y:
                    casilla.muro = not casilla.muro

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                sol = a_star(agente, premio)

            if event.key == pygame.K_LEFT:
                print('Distancia de Manhattan', abs(agente.x-premio.x + agente.y -premio.y))
                print('Coste real: ', i)

