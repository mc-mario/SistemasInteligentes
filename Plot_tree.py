from graphviz import Digraph
from Grafos import NodoH, rec
from Problema1 import *
dot = Digraph(comment='plot_tree')

def draw_tree(n):
    if n is None:
        return False
    tree_root = n.root()

    resultado = list()
    resultado.append(n)

    while n.padre != None:
        resultado.append(n.padre)
        n = n.padre



    def create_nodes(dot, nodo : NodoH, resultado):
        if nodo.uuid in [nodo.uuid for nodo in resultado]:
            dot.node(f'{nodo.uuid}', f'{nodo.color}{nodo.n}', shape='star', style='filled')
        else:
            dot.node(f'{nodo.uuid}', f'{nodo.color}{nodo.n}', shape='egg')

        for hijo in nodo.hijos:
            create_nodes(dot, hijo, resultado)

        try:
            for hijo in nodo.hijos:
                dot.edge(f'{nodo.uuid}', f'{hijo.uuid}')
        except Exception as e:
            pass

    def show_way(dot, nodo : NodoH):
        pass

    create_nodes(dot, tree_root, resultado)
    dot.render('test-output/round-table.gv', view=True)

n1 = solve_anchura()
n2 = solve_profundiad_limit(13)


draw_tree(n2)


