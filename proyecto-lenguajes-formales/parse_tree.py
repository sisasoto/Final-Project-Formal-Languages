"""
parse_tree.py - El árbol de análisis sintáctico
===============================================
Libro: Sección 4.2.4 (árboles de análisis) y Sección 5.1.2 (árbol anotado:
un árbol que además muestra el valor de los atributos de cada nodo).

Los dos parsers (ll1.py y slr1.py) construyen este árbol y el evaluador
(evaluator.py) le pone los valores de los atributos.
"""


class Nodo:
    """Un nodo del árbol.

    simbolo    : el símbolo del nodo ('S', 'A', 'a', o 'e' para la hoja vacía)
    produccion : la regla que se usó para expandir el nodo (solo en los nodos
                 internos; en las hojas es None)
    hijos      : lista de nodos hijos, de izquierda a derecha
    atributos  : diccionario con los valores, por ejemplo {'d': 1, 'v': 5}.
                 Las hojas con un terminal traen {'lexval': el carácter}.
    id         : número del nodo (1, 2, 3, ...) para nombrarlo en el grafo
    """

    def __init__(self, simbolo, produccion=None):
        self.simbolo = simbolo
        self.produccion = produccion
        self.hijos = []
        self.atributos = {}
        self.id = 0

    def es_hoja(self):
        return self.produccion is None

    def todos_los_nodos(self):
        """Lista de todos los nodos del árbol en preorden
        (primero el nodo, después sus hijos de izquierda a derecha)."""
        lista = [self]
        for hijo in self.hijos:
            lista = lista + hijo.todos_los_nodos()
        return lista

    def numerar(self):
        """Pone los números 1, 2, 3, ... a los nodos, en preorden."""
        numero = 1
        for nodo in self.todos_los_nodos():
            nodo.id = numero
            numero = numero + 1

    def etiqueta(self):
        """Nombre corto del nodo: símbolo#número, por ejemplo 'E#4'."""
        return self.simbolo + "#" + str(self.id)

    def dibujar(self, profundidad=0):
        """Texto del árbol anotado: un nodo por línea, con sangría según la
        profundidad y sus atributos entre llaves."""
        linea = "    " * profundidad + self.etiqueta()
        if len(self.atributos) > 0:
            partes = []
            for nombre in sorted(self.atributos):
                partes.append(nombre + "=" + str(self.atributos[nombre]))
            linea = linea + "  {" + ", ".join(partes) + "}"
        lineas = [linea]
        for hijo in self.hijos:
            lineas.append(hijo.dibujar(profundidad + 1))
        return "\n".join(lineas)


def hoja_terminal(caracter):
    """Hoja con un terminal. Su atributo lexval es el mismo carácter
    (enunciado, Sección 3, Paso 2)."""
    hoja = Nodo(caracter)
    hoja.atributos["lexval"] = caracter
    return hoja


def hoja_epsilon():
    """Hoja 'e' que cuelga de un nodo expandido con una regla A -> e."""
    return Nodo("e")
