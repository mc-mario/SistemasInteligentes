from graphviz import Digraph
from Grafos import NodoH
from Problema1 import *


def draw_tree(comment, n):
    dot = Digraph(comment=comment)
    try:
        tree_root = n.root()
    except Exception as ex:
        return False

    resultado = list()
    resultado.append(n)

    while n.padre != None:
        resultado.append(n.padre)
        n = n.padre



    def create_nodes(dot, nodo : NodoH, resultado):
        if nodo.uuid in [nodo.uuid for nodo in resultado]:
            dot.node(f'{nodo.uuid}', f'{nodo.color}{nodo.n+1}', shape='star', style='filled')
        else:
            dot.node(f'{nodo.uuid}', f'{nodo.color}{nodo.n+1}', shape='egg')

        for hijo in nodo.hijos:
            create_nodes(dot, hijo, resultado)

        try:
            for hijo in nodo.hijos:
                dot.edge(f'{nodo.uuid}', f'{hijo.uuid}')
        except Exception as e:
            pass



    create_nodes(dot, tree_root, resultado)
    dot.render(f'test-output/{comment}.gv', view=True)

n1 = solve_anchura()
n2 = solve_profundidad_no_iter(limit=20)


draw_tree('Anchura', n1)
draw_tree('Profundidad', n2)
