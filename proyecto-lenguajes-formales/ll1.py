"""
ll1.py - Ítem 2: parser LL(1) (de arriba hacia abajo)
=====================================================
Libro:
  - Sección 4.4.3: definición de gramática LL(1) y Algoritmo 4.31
    (construcción de la tabla M). Ejemplo: Figura 4.17.
  - Sección 4.4.4: Algoritmo 4.34, parser predictivo con pila, sin
    recursión (Figura 4.20). Movimientos de ejemplo: Figura 4.21.

Regla del enunciado: la gramática NO se modifica antes de revisar si es
LL(1) (no se quita la recursión por la izquierda).
"""

from grammar import EPSILON, FIN
from parse_tree import Nodo, hoja_terminal, hoja_epsilon


class TablaLL1:
    """La tabla M[A, a] y la prueba de si la gramática es LL(1).

    self.tabla es un diccionario:
        llave = (no terminal, terminal), por ejemplo ("A", "a")
        valor = lista de reglas que van en esa casilla
    Si una casilla queda con 2 o más reglas, hay un conflicto.
    Si una casilla no existe en el diccionario, es una casilla de error.
    """

    def __init__(self, gramatica, ff):
        self.gramatica = gramatica
        self.ff = ff
        self.tabla = {}
        self.construir()

    def agregar(self, A, a, regla):
        """Pone una regla en la casilla M[A, a] (sin repetirla)."""
        if (A, a) not in self.tabla:
            self.tabla[(A, a)] = []
        if regla not in self.tabla[(A, a)]:
            self.tabla[(A, a)].append(regla)

    # ------------------------------------------------------------------
    # Algoritmo 4.31: construcción de la tabla predictiva
    # ------------------------------------------------------------------
    def construir(self):
        for regla in self.gramatica.producciones:      # para cada A -> α
            A = regla.cabeza
            first_alfa = self.ff.first_de_cadena(regla.cuerpo)

            # Paso 1: para cada terminal a en FIRST(α), M[A, a] = A -> α
            for a in first_alfa:
                if a != EPSILON:
                    self.agregar(A, a, regla)

            # Paso 2: si ε está en FIRST(α), para cada b en FOLLOW(A)
            # (incluido $), M[A, b] = A -> α
            if EPSILON in first_alfa:
                for b in self.ff.follow[A]:
                    self.agregar(A, b, regla)

    # ------------------------------------------------------------------
    # Condición LL(1) (definición al inicio de la Sección 4.4.3)
    # ------------------------------------------------------------------
    def cumple_condicion_ll1(self):
        """El libro dice que G es LL(1) si para cada par de alternativas
        distintas A -> α | β se cumple:

          1. α y β no pueden empezar con el mismo terminal, y como mucho
             una de las dos puede producir ε:
                 FIRST(α) y FIRST(β) no tienen nada en común (contando ε).
          2. Si β puede producir ε, α no puede empezar con un terminal de
             FOLLOW(A). Y lo mismo al revés.
        """
        g = self.gramatica
        for A in g.no_terminales:
            alternativas = g.producciones_de(A)
            # Revisar cada pareja (i, j) de alternativas con i < j.
            for i in range(len(alternativas)):
                for j in range(i + 1, len(alternativas)):
                    first_a = self.ff.first_de_cadena(alternativas[i].cuerpo)
                    first_b = self.ff.first_de_cadena(alternativas[j].cuerpo)
                    follow_A = self.ff.follow[A]

                    # Condición 1
                    if len(first_a & first_b) > 0:       # & = intersección
                        return False
                    # Condición 2
                    if EPSILON in first_b and len((first_a - {EPSILON}) & follow_A) > 0:
                        return False
                    if EPSILON in first_a and len((first_b - {EPSILON}) & follow_A) > 0:
                        return False
        return True

    def es_ll1(self):
        """Respuesta de la prueba de la definición, que es la que pide el
        enunciado. Si se cumple, ninguna casilla de la tabla tiene dos
        reglas, así que el parser siempre sabe qué regla usar."""
        return self.cumple_condicion_ll1()

    def conflictos(self):
        """Lista de casillas con más de una regla (para mostrar/depurar)."""
        lista = []
        for casilla in sorted(self.tabla):
            if len(self.tabla[casilla]) > 1:
                lista.append(casilla)
        return lista

    def imprimir(self):
        """Imprime la tabla M en el estilo de la Figura 4.17."""
        columnas = sorted(self.gramatica.terminales) + [FIN]
        filas = sorted(self.gramatica.no_terminales)
        contenido = {}
        for casilla in self.tabla:
            textos = []
            for regla in self.tabla[casilla]:
                textos.append(str(regla))
            contenido[casilla] = " | ".join(textos)
        imprimir_tabla("LL(1) parsing table M", filas, columnas, contenido)


class ParserLL1:
    """Parser predictivo con pila (Algoritmo 4.34, Figura 4.20)."""

    def __init__(self, tabla_ll1):
        self.tabla = tabla_ll1.tabla
        self.gramatica = tabla_ll1.gramatica

    def analizar(self, entrada, traza=None):
        """Analiza la lista de símbolos `entrada` (que ya termina en '$').

        Devuelve la raíz del árbol si la cadena es aceptada, o None si no.

        Si `traza` es una lista, en ella se guardan los pasos
        (MATCHED, STACK, INPUT, ACTION) como en la Figura 4.21.

        Cada elemento de la pila es una pareja [símbolo, nodo del árbol].
        Así, cuando expandimos A -> Y1...Yk, el nodo de A recibe sus hijos
        y el árbol se construye desde la raíz hacia las hojas.
        """
        g = self.gramatica
        raiz = Nodo(g.inicial)
        pila = [[FIN, None], [g.inicial, raiz]]   # el tope es el final de la lista
        i = 0                                     # posición de la letra actual
        leido = ""

        while True:
            X = pila[-1][0]          # símbolo en el tope de la pila
            nodo = pila[-1][1]
            a = entrada[i]           # letra actual de la entrada

            if X == FIN:
                # Solo queda $ en la pila. Se acepta si también se acabó la
                # entrada; si sobran letras, la cadena no es válida.
                if a == FIN:
                    self.anotar(traza, leido, pila, entrada, i, "accept")
                    return raiz
                self.anotar(traza, leido, pila, entrada, i, "error")
                return None

            if X == a:
                # El tope coincide con la letra: sacar de la pila y avanzar.
                self.anotar(traza, leido, pila, entrada, i, "match " + a)
                pila.pop()
                leido = leido + a
                i = i + 1

            elif not g.es_no_terminal(X):
                # El tope es un terminal distinto de la letra: error.
                self.anotar(traza, leido, pila, entrada, i, "error")
                return None

            elif (X, a) not in self.tabla:
                # La casilla M[X, a] está vacía: error.
                self.anotar(traza, leido, pila, entrada, i, "error")
                return None

            else:
                # M[X, a] = X -> Y1 Y2 ... Yk
                regla = self.tabla[(X, a)][0]
                self.anotar(traza, leido, pila, entrada, i, "output " + str(regla))
                pila.pop()
                nodo.produccion = regla

                if regla.es_epsilon():
                    nodo.hijos = [hoja_epsilon()]
                else:
                    # Crear un hijo por cada símbolo del cuerpo.
                    for Y in regla.cuerpo:
                        if g.es_no_terminal(Y):
                            nodo.hijos.append(Nodo(Y))
                        else:
                            nodo.hijos.append(hoja_terminal(Y))
                    # Meter Yk, ..., Y2, Y1 para que Y1 quede en el tope.
                    for k in range(len(regla.cuerpo) - 1, -1, -1):
                        pila.append([regla.cuerpo[k], nodo.hijos[k]])

    def anotar(self, traza, leido, pila, entrada, i, accion):
        """Guarda una fila de la traza (solo si se pidió la traza).
        La pila se escribe con el tope a la izquierda, como en el libro."""
        if traza is None:
            return
        texto_pila = ""
        for k in range(len(pila) - 1, -1, -1):
            texto_pila = texto_pila + pila[k][0]
        traza.append((leido, texto_pila, "".join(entrada[i:]), accion))


# ----------------------------------------------------------------------
# Funciones para imprimir tablas (también las usa slr1.py y main.py)
# ----------------------------------------------------------------------
def imprimir_tabla(titulo, filas, columnas, contenido):
    """Imprime una tabla con bordes.
    contenido es un diccionario {(fila, columna): texto}."""
    encabezado = [""] + [str(c) for c in columnas]
    datos = []
    for f in filas:
        renglon = [str(f)]
        for c in columnas:
            renglon.append(contenido.get((f, c), ""))
        datos.append(renglon)

    # Ancho de cada columna = el texto más largo de esa columna.
    anchos = []
    for j in range(len(encabezado)):
        ancho = len(encabezado[j])
        for renglon in datos:
            ancho = max(ancho, len(renglon[j]))
        anchos.append(ancho)

    def formatear(valores):
        celdas = []
        for j in range(len(valores)):
            celdas.append(valores[j].ljust(anchos[j]))
        return " " + " | ".join(celdas)

    separador = []
    for w in anchos:
        separador.append("-" * (w + 2))

    print(titulo)
    print(formatear(encabezado))
    print("+".join(separador))
    for renglon in datos:
        print(formatear(renglon))
    print()


def imprimir_traza(filas, encabezados):
    """Imprime una traza paso a paso (Figura 4.21 o Figura 4.38)."""
    anchos = []
    for j in range(len(encabezados)):
        ancho = len(encabezados[j])
        for fila in filas:
            ancho = max(ancho, len(str(fila[j])))
        anchos.append(ancho)
    celdas = []
    for j in range(len(encabezados)):
        celdas.append(encabezados[j].ljust(anchos[j]))
    print("  ".join(celdas))
    for fila in filas:
        celdas = []
        for j in range(len(fila)):
            celdas.append(str(fila[j]).ljust(anchos[j]))
        print("  ".join(celdas))
    print()
