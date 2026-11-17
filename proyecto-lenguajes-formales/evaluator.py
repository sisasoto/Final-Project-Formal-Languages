"""
evaluator.py - Ítem 3: evaluador con grafo de dependencias
==========================================================
Libro:
  - Sección 5.2.1: grafo de dependencias. Hay un vértice por cada atributo
    de cada nodo del árbol, y una flecha DESDE cada atributo que una regla
    usa HACIA el atributo que esa regla calcula (ejemplo: Figura 5.7).
  - Sección 5.2.2: los atributos se calculan en un orden topológico del
    grafo. Si el grafo tiene un ciclo, no hay orden posible y la SDD no se
    puede evaluar.

Este evaluador sirve para CUALQUIER SDD: solo lee las reglas que vienen
como datos desde sdd.py ("define", "usa", "funcion"). No recorre el árbol
en un orden fijo; el orden lo decide el grafo.

Un vértice del grafo es una pareja (número del nodo, nombre del atributo),
por ejemplo (4, "d") es el atributo d del nodo número 4.
"""

from sdd import LEXVAL


class SDDCircular(Exception):
    """Error que se lanza cuando el grafo de dependencias tiene un ciclo."""
    pass


def nodo_en_posicion(nodo, posicion):
    """Traduce una posición de una regla al nodo del árbol:
    posición 0 = el mismo nodo (la cabeza); posición i = su hijo número i."""
    if posicion == 0:
        return nodo
    return nodo.hijos[posicion - 1]


class GrafoDependencias:
    """Grafo de dependencias de un árbol (Sección 5.2.1).

    self.vertices : conjunto de vértices (número de nodo, atributo)
    self.flechas  : {u: [v1, v2, ...]}  significa u -> v1, u -> v2, ...
                    (v usa a u, así que u se calcula antes que v)
    self.regla_de : {vértice: (regla, nodo)}  qué regla calcula cada vértice
                    y en qué nodo del árbol se aplicó esa regla
    self.nodos    : {número: nodo}  para encontrar un nodo por su número
    self.no_ordenados : si hay un ciclo, los vértices que no se pudieron
                    ordenar (los usa el visualizador para pintarlos)
    """

    def __init__(self):
        self.vertices = set()
        self.flechas = {}
        self.regla_de = {}
        self.nodos = {}
        self.no_ordenados = []

    def agregar_vertice(self, v):
        if v not in self.vertices:
            self.vertices.add(v)
            self.flechas[v] = []

    def agregar_flecha(self, u, v):
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.flechas[u].append(v)

    def nombre(self, v):
        """Nombre de un vértice, por ejemplo 'E#4.d'."""
        return self.nodos[v[0]].etiqueta() + "." + v[1]

    # ------------------------------------------------------------------
    # Construcción del grafo (Sección 5.2.1)
    # ------------------------------------------------------------------
    def construir(self, raiz, sdd):
        for nodo in raiz.todos_los_nodos():
            self.nodos[nodo.id] = nodo

            if nodo.es_hoja():
                # Las hojas con un terminal aportan su lexval (ya conocido).
                if LEXVAL in nodo.atributos:
                    self.agregar_vertice((nodo.id, LEXVAL))
                continue

            # Nodo interno: aplicar las reglas de su producción.
            for r in sdd.reglas_de(nodo.produccion):
                posicion, nombre = r["define"]
                calculado = (nodo_en_posicion(nodo, posicion).id, nombre)
                self.agregar_vertice(calculado)
                self.regla_de[calculado] = (r, nodo)

                # Una flecha desde cada atributo que se usa hacia el calculado.
                for (posicion_usada, nombre_usado) in r["usa"]:
                    usado = (nodo_en_posicion(nodo, posicion_usada).id, nombre_usado)
                    self.agregar_flecha(usado, calculado)

    # ------------------------------------------------------------------
    # Orden topológico (Sección 5.2.2)
    # ------------------------------------------------------------------
    def orden_topologico(self):
        """Es el método que describe el libro:
          1. buscar un vértice al que no le llegue ninguna flecha;
          2. ponerlo en el orden y quitarlo del grafo (junto con sus flechas);
          3. repetir con los vértices que quedan.
        Si quedan vértices pero a todos les llega alguna flecha, hay un
        ciclo y la SDD es circular.
        """
        # Cuántas flechas le llegan a cada vértice.
        llegan = {}
        for v in self.vertices:
            llegan[v] = 0
        for u in self.vertices:
            for v in self.flechas[u]:
                llegan[v] = llegan[v] + 1

        pendientes = sorted(self.vertices)    # ordenados para que el resultado
        orden = []                            # salga siempre igual

        while len(pendientes) > 0:
            # Paso 1: buscar un vértice al que no le llegue ninguna flecha.
            elegido = None
            for v in pendientes:
                if llegan[v] == 0:
                    elegido = v
                    break

            if elegido is None:
                # A todos los que quedan les llega alguna flecha: hay un ciclo.
                self.no_ordenados = list(pendientes)
                nombres = []
                for v in pendientes:
                    nombres.append(self.nombre(v))
                raise SDDCircular("The SDD is circular: the dependency graph has a cycle. "
                                  "These attributes could not be ordered: " + ", ".join(nombres))

            # Paso 2: ponerlo en el orden y quitarlo con sus flechas.
            orden.append(elegido)
            pendientes.remove(elegido)
            for v in self.flechas[elegido]:
                llegan[v] = llegan[v] - 1

        return orden

    def describir(self):
        """Lista de flechas del grafo (útil para comparar con el dibujo a mano)."""
        lineas = ["Dependency graph (edge u -> v means v uses u):"]
        for u in sorted(self.vertices):
            for v in sorted(self.flechas[u]):
                lineas.append("    " + self.nombre(u) + " -> " + self.nombre(v))
        return "\n".join(lineas)


class EvaluadorSDD:
    """Evalúa una SDD sobre un árbol (enunciado, Sección 3, Paso 5)."""

    def __init__(self, sdd):
        self.sdd = sdd
        self.grafo = None

    def evaluar(self, raiz):
        """Calcula todos los atributos del árbol y devuelve la lista de
        vértices en el orden en que se calcularon.

        1. Numerar los nodos y construir el grafo de dependencias.
        2. Calcular un orden topológico (lanza SDDCircular si hay ciclo).
        3. Recorrer los vértices en ese orden. Para cada uno: buscar su
           regla, leer los valores que usa (ya están calculados, porque el
           orden lo garantiza), aplicar la función y guardar el resultado.
        """
        raiz.numerar()
        self.grafo = GrafoDependencias()
        self.grafo.construir(raiz, self.sdd)
        orden = self.grafo.orden_topologico()

        calculados = []
        for vertice in orden:
            if vertice not in self.grafo.regla_de:
                continue          # es un lexval: ya se conocía
            r, nodo = self.grafo.regla_de[vertice]

            valores = []
            for (posicion, nombre) in r["usa"]:
                valores.append(nodo_en_posicion(nodo, posicion).atributos[nombre])

            resultado = r["funcion"](*valores)     # el * pasa la lista como argumentos
            numero_nodo, nombre_atributo = vertice
            self.grafo.nodos[numero_nodo].atributos[nombre_atributo] = resultado
            calculados.append(vertice)
        return calculados

    def resultado(self, raiz):
        """Valor del atributo principal de S."""
        return raiz.atributos[self.sdd.atributo_principal]
