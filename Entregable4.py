from itertools import groupby
from pprint import pprint
from copy import deepcopy
import random

class Estado():
    def __init__(self, nombre, rew, final=False):
        self.nombre = nombre
        self.rew = rew
        self.utilidad = 0
        self.final = final
        if final:
            self.utilidad = rew

    def __repr__(self):
        return f"{self.nombre}"

    def __hash__(self):
        return hash((self.nombre, self.rew))

class Accion():
    def __init__(self, nombre, dic_direcc):
        self.nombre = nombre
        self.dic_direcc = dic_direcc

    def u(self):
       return sum([prob * new_st.utilidad for new_st, prob in self.dic_direcc.items()])

    def __repr__(self):
        return f"{self.nombre}"
    
    def __gt__(self, other):
        return self.u() > other.u()

    def __eq__(self, other):
        return self.nombre == other.nombre

    def __hash__(self):
        return hash((self.nombre, tuple(self.dic_direcc.items())))

class Nodo():
    def __init__(self, estado : Estado, acciones=[], politica=None):
        self.estado = estado
        self.acciones = acciones
        self.politica = politica  #[Acción escogida]



    def __repr__(self):
        return f"{self.estado}"

'''Ejercicio Diapositiva'''
# s1 = Estado('s1', 0)
# s2 = Estado('s2', 0)
# s3 = Estado('s3', 0)
# s4 = Estado('s4', 1, final=True)
# a1 = Accion('a', {s2:0.9, s1:0.1})
# b1 = Accion('b', {s3:1})
#
# a3 = Accion('a3', {s3:0.5, s4:0.5})
#
# a2 = Accion('a', {s4:1})
# b2 = Accion('b', {s1:0.9, s3:0.1})
# n1 = Nodo(s1, [a1,b1])
# n2 = Nodo(s2, [a2,b2])
# n3 = Nodo(s3, [a3])
# n4 = Nodo(s4, [])
# nodos = [n1,n2,n3,n4]

# '''Ejercicio Entregable'''
# #Estados y Acciones
# estados = list()
# s0 = Estado('S0', -1)
# s1 = Estado('S1', -1)
# s2 = Estado('S2', -1)
# s3 = Estado('S3', -1)
# s4 = Estado('S4', -10, final=True)
# s5 = Estado('S5', 10, final=True)
# s6 = Estado('S6', -10, final=True)
# a0 = Accion('a', {s0:0.5, s1:0.5 })
# a1 = Accion('a', {s4:0.9, s5:0.1})
# a2 = Accion('a', {s3:1})
# a3 = Accion('a', {s0:0.5, s2:0.5})
# b0 = Accion('b', {s1:0.9, s2:0.1})
# b2 = Accion('b', {s1:1.0})
# b3 = Accion('b', {s6:0.9, s5:0.1})
# c0 = Accion('c', {s3:1})
# c1 = Accion('c', {s5:0.9,s2:0.1})

# # Nodos -> Estado y Accion
# n0 = Nodo(s0, [a0, b0, c0], a0)
# n1 = Nodo(s1, [a1, c1], a1)
# n2 = Nodo(s2, [a2, b2], a2)
# n3 = Nodo(s3, [a3, b3], a3)
# n4 = Nodo(s4)
# n5 = Nodo(s5)
# n6 = Nodo(s6)

# nodos = [n0, n1, n2, n3, n4, n5, n6]

'''Ejercicio Clase 2 Noviembre'''
# s0 = Estado('s1',-1)
# s1 = Estado('s2',-1)
# s2 = Estado('s3',-1)
# s3 = Estado('s4',10)

# a0 = Accion('a', {0.6:s1, 0.4:s2})
# b0 = Accion('b', {0.2:s1, 0.8:s2})
# a2 = Accion('a', {0.9:s1, 0.1:s3})
# a1 = Accion('a', {0.3:s2, 0.7:s3})
# b1 = Accion('b', {0.8:s2, 0.2:s3})
# b2 = Accion('b', {0.9:s3, 0.1:s1})

# n0 = Nodo(s0, [a0,b0])
# n1 = Nodo(s1, [a1,b1])
# n2 = Nodo(s2, [a2,b2])
# n3 = Nodo(s3)

# nodos = [n0,n1,n2,n3]

s0 = Estado('s0',0)
s1 = Estado('s1', 0)
s2 = Estado('s2', 0)
s3 = Estado('s3',1, final=True)
a0 = Accion('a', {s1:0.9, s0:0.1})
b0 = Accion('b', {s2:1})
a1 = Accion('a', {s0:0.9, s2:0.1})
b1 = Accion('b', {s3:1})
a2 = Accion('a', {s2:0.5, s3:0.5})
n0 = Nodo(s0, [a0, b0])
n1 = Nodo(s1, [a1, b1])
n2 = Nodo(s2, [a2])
n3 = Nodo(s3)
nodos = [n0,n1,n2,n3]


gamma = 0.999

def iteracion_valores(gamma, nodos, epsilon = 0.01):
    while True:
        new_util = list()
        delta = 0

        for nodo in nodos:
            nueva_u = nodo.estado.rew
            if nodo.acciones:
                max_util = max(nodo.acciones, key=lambda x : x.u())
                nodo.politica = max_util
                nueva_u += gamma * max_util.u()

            new_util.append(round(nueva_u, 2))
            delta = max(delta, abs(nodo.estado.utilidad - nueva_u))
            nodo.estado.utilidad = nueva_u
        print(new_util)
        if delta < epsilon * (1 - gamma) / gamma:
            print('Converged' ' Delta: ' f'{delta}')
            return


'''Apartado 2. Iteración de Políticas'''
def policy_evaluation(nodos, gamma = 0.999, epsilon=0.01):
    while True:
        delta = 0
        for nodo in nodos:
            u_prime = nodo.estado.rew
            if nodo.politica:
                u_prime += nodo.politica.u()
            delta = max(delta, abs(u_prime-nodo.estado.utilidad))
            nodo.estado.utilidad = u_prime

        if delta < epsilon * (1 - gamma) / gamma:
            return 

def policy_improvement(nodos):
    u_prime = list()
    for nodo in nodos:
        u = max(nodo.acciones, key=lambda x: x.u() , default=None)
        u_prime.append(u)
    return u_prime


def policy_iteration():
    politica_prime = list()
    for nodo in nodos:
        politica_prime.append(nodo.politica)

    while True:
        for enum, nodo in enumerate(nodos):
            nodo.politica = politica_prime[enum]
        policy = [nodo.politica for nodo in nodos]
        policy_evaluation(nodos)
        politica_prime = policy_improvement(nodos)
        print('π ', policy)
        print("π'",politica_prime)
        if policy == politica_prime:             
            return politica_prime





'''Apartado 3, Q_Learning '''
learning_ratio = 0.5
pseudo_ran = [0.18, 0.73, 0.12, 0.67, 0.43, 0.72, 0.81, 0.39, 0.42, 0.79, 0.07,0.54,0.89,0.04,0.21]
def q_learning(epochs = 3):

    q_table = {nodo.estado: {accion: 0 for accion in nodo.acciones} for nodo in nodos}
    new_state = None

    while True:
        state = n0.estado
        while True:
            accion, q = max(q_table[state].items(), key=lambda x: x[1])

            ran = random.random()
            
            for key, value in accion.dic_direcc.items():
                if ran <= value:
                    new_state = key
                    print(state, '->', new_state, f'{accion} {ran}')
                    break
                else: ran -= value
            if new_state.final:
                q = (1 - learning_ratio) * q + learning_ratio * new_state.rew
                q_table[state][accion] = q
                print('s0: ', q_table[s0], '\n', 's1: ', q_table[s1], '\n', 's2: ', q_table[s2],
                      '\n', 's3: ', q_table[s3] )
                print('\n')
                break
            else:
                _ , q_prime = max(q_table[new_state].items(), key=lambda x: x[1])
                q = (1-learning_ratio) * q + learning_ratio * (new_state.rew + q_prime)


                q_table[state][accion] = q

            state = new_state
        epochs -= 1
        if epochs == 0: break



#çq_learning(4)
iteracion_valores(0.99, nodos)
# # print('Politica', [nodo.politica for nodo in nodos])
# #policy_iteration()
# #print([nodo.politica for nodo in nodos])