from itertools import permutations
from pprint import pprint as print
import random

ciudades = {
    'Albacete' : 172816,
    'Ciudad Real': 74641,
    'Cuenca' : 54876,
    'Guadalajara' : 84145,
    'Talavera' : 83303,
    'Toledo' : 83741
}

distancias = {
    'Albacete' : [('Ciudad Real', 206), ('Cuenca', 142), ('Guadalajara', 309), ('Talavera', 313), ('Toledo', 240)],
    'Ciudad Real': [('Cuenca', 241), ('Guadalajara', 254), ('Talavera', 200), ('Toledo', 119), ('Albacete', 206)],
    'Cuenca' : [('Ciudad Real', 241), ('Albacete', 142), ('Toledo', 187), ('Talavera', 253), ('Guadalajara', 186)],
    'Guadalajara' : [('Talavera', 172), ('Toledo', 129), ('Albacete', 309), ('Ciudad Real', 254), ('Cuenca', 186)],
    'Talavera' : [('Toledo', 81), ('Guadalajara', 172), ('Cuenca', 253), ('Albacete', 313), ('Ciudad Real', 200)],
    'Toledo' : [('Talavera', 81), ('Guadalajara', 129), ('Cuenca', 187), ('Ciudad Real', 119), ('Albacete', 240)]              
}

class Entregable5():

    def __init__(self, hospitales):
        ciudadeskeys = ciudades.keys()
        self.hospitales = hospitales
        self.estado = dict(zip(ciudadeskeys, hospitales))


    def evaluacion(self):
        ev = 0
        for ciudad, hosp in self.estado.items():
            hosp = bool(hosp)
            if not hosp:
                '''Devuelve tupla (Ciudad, distancia) con hospital más próxima a la ciudad actual'''
                ciudad_prox = min(filter(lambda x : self.estado[x[0]] == 1, distancias[ciudad]), key=lambda x : x[1])
                ciudad_con_hospital, distancia = ciudad_prox
                ev += ciudades[ciudad] * distancia
        return round((ev / sum(ciudades.values())),2)
    
    def __repr__(self):
        return f"{self.estado} Eval: {self.evaluacion()}"
    

    def generar_vecinos(self):
        def permutar():
            seen = set() 
            for permutation in permutations(self.hospitales): 
                hperm = hash(permutation) 
                if hperm in seen: 
                    continue 
                if len([i for i,j in zip(self.hospitales, permutation) if i != j]) == 2:
                    seen.add(hperm) 
                    yield permutation 
        return [Entregable5(vecino) for vecino in permutar()]
            


ej = Entregable5([0,0,0,1,1,1])

# Hill Climbing
for _ in range(3):

    ej_aux = min(ej.generar_vecinos(), key=lambda x : x.evaluacion())
    if (ej_aux.evaluacion() <= ej.evaluacion()):
        ej = ej_aux
    
    

  
poblacion_inicial = ej.generar_vecinos() + [ej]
print(len(poblacion_inicial))

def algoritmo_genetico():
    
    def funcion_cruce(p1 : list, p2 : list) -> list:
        corte = 3
        h1, h2 = list(), list()
        h1.extend(p1[:corte])
        h1.extend(p2[corte:])
        h2.extend(p2[:corte])
        h2.extend(p1[corte:])
        return h1, h2
    
    def funcion_mutacion(h1 : list) -> list:
        if random.random() > 0.877:
            bit = random.randrange(0, len(h1))
            h1[bit] = abs(h1[bit]-1)
        return h1

    poblacion = sorted(poblacion_inicial, key= lambda x : x.evaluacion())
    epochs = 10
    for _ in range(epochs):
        # Conservamos al super individuo de cada generación
        super_indiv = poblacion[0]

        # Mezclamos aleatoriamente a la población
        random.shuffle(poblacion)

        hospitales = list(map(lambda x : x.hospitales, poblacion))

        #Tupla de padres
        papis = list(zip(hospitales[1::2], hospitales[::2]))

        #Función de cruce sobre los pares de padres
        cruces = list(map(lambda x : funcion_cruce(*x), papis))
        unpackeds = [elem for tuple in cruces for elem in tuple]

        #Operador de mutación y casting a la clase
        mutados = list(map(lambda x : Entregable5(x), list(map(funcion_mutacion, unpackeds))))

        #Población ordenada, sustituimos al mejor por el peor
        poblacion = sorted(mutados + [super_indiv], key = lambda x : x.evaluacion())[:-1]
        
        print(f'El miyor di esta epoch is {poblacion[0]}')

    print(f'Poblasió final {poblacion}')

algoritmo_genetico()