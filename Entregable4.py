from itertools import groupby
from pprint import pprint

class Estado():
    def __init__(self, nombre, rew):
        self.nombre = nombre
        self.inmediate_reward = rew
        self.utilidad = 0

    def __repr__(self):
        return f"{self.nombre} R({self.utilidad})"

class Accion():
    def __init__(self, accion, prob, estado : Estado):
        self.accion = accion
        self.probabilidad = prob
        self.nuevo_estado = estado

    def utilidad(self):
        return self.probabilidad * self.nuevo_estado.utilidad

    def __repr__(self):
        return f"{self.accion} P{self.probabilidad} {self.nuevo_estado.nombre}"

class Nodo():
    def __init__(self, estado : Estado, acciones=[]):
        self.estado = estado
        self.acciones = acciones

    def __repr__(self):
        return f"{self.estado}: Acciones{self.acciones}"


# s1 = Estado('s1', 0)
# s2 = Estado('s2', 0)
# s3 = Estado('s3', 0)
# s4 = Estado('s4', 1)
# a13 = Accion('A2', 1, s3)
# a33 = Accion('A3', 0.5, s3)
# a34 = Accion('A3', 0.5, s4)
# a35 = Accion('A4', 1, s1)
# a24 = Accion('A2', 1, s4)
# n1 = Nodo(s1, [a13])
# n2 = Nodo(s2, [a24])
# n3 = Nodo(s3, [a33, a34, a35])
# n4 = Nodo(s4, [])
# nodos = [n1,n2,n3,n4]

# Estados y Acciones
estados = list()
s0 = Estado('S0', -1)
s1 = Estado('S1', -1)
s2 = Estado('S2', -1)
s3 = Estado('S3', -1)
s4 = Estado('S4', -10)
s5 = Estado('S5', 10)
s6 = Estado('S6', -10)
a01 = Accion('A', 0.5, s1)
a00 = Accion('A', 0.5, s0)
a14 = Accion('A', 0.9, s4)
a15 = Accion('A', 0.1, s5)
a23 = Accion('A', 1, s3)
a32 = Accion('A', 0.5, s2)
a30 = Accion('A', 0.5, s0)
b01 = Accion('B', 0.9, s1)
b02 = Accion('B', 0.1, s2)
b36 = Accion('B', 0.9, s6)
b35 = Accion('B', 0.1, s5)
c03 = Accion('C', 1, s3)
c12 = Accion('C', 0.1, s2)
c15 = Accion('C', 0.9, s5)

# Nodos -> Estado y Accion
n0 = Nodo(s0, [a01, a00, b01, b02, c03])
n1 = Nodo(s1, [a14, a15, c12, c15])
n2 = Nodo(s2, [a23])
n3 = Nodo(s3, [a30, a32, b35, b36])
n4 = Nodo(s4)
n5 = Nodo(s5)
n6 = Nodo(s6)

nodos = [n0, n1, n2, n3, n4, n5, n6]

gamma = 0.999

def iteracion_valores(gamma, nodos, epsilon = 0.01):
    iteraciones = list()

    while True:
        nuevas_u = list()
        delta = 0

        for nodo in nodos:
            acciones = [list(v) for k,v in groupby(nodo.acciones, lambda x: x.accion)]
            u_prime = [sum([elem.utilidad() for elem in xs]) for xs in acciones]
            zipped_val = tuple(zip(acciones, u_prime))
            print(zipped_val)
            if u_prime: nueva_u = nodo.estado.inmediate_reward + gamma * max(u_prime)
            else:       nueva_u = nodo.estado.inmediate_reward     #Es estado final
            nuevas_u.append(round(nueva_u, 2))
            delta = max(delta, abs(nodo.estado.utilidad - nueva_u))
            nodo.estado.utilidad = nueva_u

        iteraciones.append([delta,nuevas_u])
        if delta < epsilon * (1 - gamma) / gamma:
            return iteraciones







pprint(iteracion_valores(gamma, nodos))
