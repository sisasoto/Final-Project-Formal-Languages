"""
slr1.py - Ítem 2: parser SLR(1) (de abajo hacia arriba)
=======================================================
Libro:
  - Sección 4.5: análisis por desplazamiento-reducción (shift-reduce) y
    conflictos (4.5.4).
  - Sección 4.6.2: ítems LR(0), CLOSURE (Figura 4.32), GOTO y la colección
    de conjuntos de ítems (Figura 4.33). Ejemplo: Figura 4.31.
  - Sección 4.6.3: algoritmo de análisis LR (Algoritmo 4.44, Figura 4.36).
  - Sección 4.6.4: construcción de la tabla SLR (Algoritmo 4.46).
    Ejemplo: Figura 4.37. Movimientos de ejemplo: Figura 4.38.

¿Cómo guardamos un ítem LR(0)?
  Un ítem es una regla con un punto, por ejemplo  S -> S.+T
  Lo guardamos como una tupla (numero_de_regla, posicion_del_punto):
      S -> S.+T  es la regla 1 con el punto en la posición 1  ->  (1, 1)
  Las tuplas se pueden meter en conjuntos (set) y comparar fácilmente.

¿Cómo guardamos un estado (un conjunto de ítems)?
  Como un frozenset: es un conjunto que no se puede modificar. Lo usamos
  porque Python solo deja usar como llave de un diccionario cosas que no
  cambian, y necesitamos preguntar "¿este conjunto de ítems ya existe?".

¿Cómo guardamos una acción de la tabla ACTION?
  ("shift", 5)   -> desplazar e ir al estado 5         (se imprime s5)
  ("reduce", 3)  -> reducir por la regla número 3      (se imprime r3)
  ("accept", 0)  -> aceptar                            (se imprime acc)
"""

from grammar import FIN, INICIAL_AUMENTADO
from parse_tree import Nodo, hoja_terminal, hoja_epsilon
from ll1 import imprimir_tabla


class AutomataLR0:
    """Colección canónica de conjuntos de ítems LR(0) (el autómata LR(0)).

    self.estados      : lista [I0, I1, I2, ...]; cada estado es un frozenset
    self.transiciones : diccionario {(i, X): j} que significa GOTO(Ii, X) = Ij
    """

    def __init__(self, gramatica_aumentada):
        self.g = gramatica_aumentada
        self.estados = []
        self.transiciones = {}
        self.construir_coleccion()

    # Funciones pequeñas para trabajar con ítems ------------------------
    def regla(self, item):
        """La regla (Produccion) a la que pertenece el ítem."""
        return self.g.producciones[item[0]]

    def simbolo_despues_del_punto(self, item):
        """El símbolo que está justo a la derecha del punto, o None si el
        punto está al final (ítem completo)."""
        cuerpo = self.regla(item).cuerpo
        punto = item[1]
        if punto < len(cuerpo):
            return cuerpo[punto]
        return None

    def texto_item(self, item):
        """Texto del ítem, por ejemplo 'S -> S.+T'."""
        regla = self.regla(item)
        simbolos = list(regla.cuerpo)
        simbolos.insert(item[1], ".")
        return regla.cabeza + " -> " + "".join(simbolos)

    # ------------------------------------------------------------------
    # CLOSURE(I) - Figura 4.32
    # ------------------------------------------------------------------
    def cerradura(self, items):
        """J = I
        repetir:
            para cada ítem A -> α.Bβ en J,
                para cada regla B -> γ,
                    si B -> .γ no está en J, agregarlo a J
        hasta que en una vuelta no se agregue nada."""
        J = set(items)
        cambio = True
        while cambio:
            cambio = False
            for item in list(J):
                B = self.simbolo_despues_del_punto(item)
                if B is not None and self.g.es_no_terminal(B):
                    for regla in self.g.producciones_de(B):
                        nuevo = (regla.numero, 0)        # B -> .γ
                        if nuevo not in J:
                            J.add(nuevo)
                            cambio = True
        return frozenset(J)

    # ------------------------------------------------------------------
    # GOTO(I, X) - Sección 4.6.2
    # ------------------------------------------------------------------
    def ir_a(self, I, X):
        """GOTO(I, X): tomar los ítems de I que tienen X después del punto,
        mover el punto una posición a la derecha (pasar sobre X) y sacar la
        cerradura de ese conjunto."""
        movidos = set()
        for item in I:
            if self.simbolo_despues_del_punto(item) == X:
                movidos.add((item[0], item[1] + 1))
        if len(movidos) == 0:
            return frozenset()
        return self.cerradura(movidos)

    # ------------------------------------------------------------------
    # Colección canónica de conjuntos de ítems - Figura 4.33
    # ------------------------------------------------------------------
    def construir_coleccion(self):
        """C = { CLOSURE({S' -> .S}) }
        repetir:
            para cada conjunto I en C,
                para cada símbolo X,
                    si GOTO(I, X) no es vacío y no está en C, agregarlo a C
        hasta que no se agreguen conjuntos nuevos.

        Recorremos la lista C con un índice: cada conjunto se revisa una vez
        y los nuevos se agregan al final, así que también se revisan. Es lo
        mismo que el "repetir ... hasta" del libro.
        """
        I0 = self.cerradura({(0, 0)})          # S' -> .S es la regla 0
        self.estados = [I0]
        numero_de_estado = {I0: 0}             # frozenset -> número de estado

        i = 0
        while i < len(self.estados):
            I = self.estados[i]
            for X in self.simbolos_despues_del_punto(I):
                J = self.ir_a(I, X)
                if len(J) == 0:
                    continue
                if J not in numero_de_estado:  # es un conjunto nuevo
                    numero_de_estado[J] = len(self.estados)
                    self.estados.append(J)
                self.transiciones[(i, X)] = numero_de_estado[J]
            i = i + 1

    def simbolos_despues_del_punto(self, I):
        """Los símbolos que aparecen después del punto en los ítems de I,
        en el orden de las reglas. Con este orden los estados quedan con la
        misma numeración de la Figura 4.31 del libro."""
        simbolos = []
        for item in sorted(I):
            X = self.simbolo_despues_del_punto(item)
            if X is not None and X not in simbolos:
                simbolos.append(X)
        return simbolos

    def imprimir(self):
        """Imprime los estados con sus ítems y sus transiciones."""
        print("LR(0) automaton (canonical collection of LR(0) items)")
        for i in range(len(self.estados)):
            print("I" + str(i) + ":")
            # Primero los ítems del núcleo (S' -> .S o con el punto que no está
            # al inicio) y después los que agregó la cerradura.
            for item in sorted(self.estados[i]):
                if item[1] > 0 or item[0] == 0:
                    print("    " + self.texto_item(item))
            for item in sorted(self.estados[i]):
                if not (item[1] > 0 or item[0] == 0):
                    print("    " + self.texto_item(item) + "   (closure)")
            for (origen, X) in sorted(self.transiciones):
                if origen == i:
                    destino = self.transiciones[(origen, X)]
                    print("    GOTO(I" + str(i) + ", " + X + ") = I" + str(destino))
        print()


class TablaSLR1:
    """Tablas ACTION y GOTO del parser SLR(1) (Algoritmo 4.46).

    self.accion : diccionario {(estado, terminal): lista de acciones}
    self.goto   : diccionario {(estado, no terminal): estado}
    Si una casilla de ACTION tiene 2 o más acciones, hay un conflicto.
    """

    def __init__(self, gramatica, ff):
        self.gramatica = gramatica                  # gramática original G
        self.aumentada = gramatica.aumentada()      # G' (con S' -> S)
        self.ff = ff                                # FOLLOW de la gramática G
        self.automata = AutomataLR0(self.aumentada)
        self.accion = {}
        self.goto = {}
        self.construir()

    def agregar(self, estado, simbolo, accion):
        if (estado, simbolo) not in self.accion:
            self.accion[(estado, simbolo)] = []
        if accion not in self.accion[(estado, simbolo)]:
            self.accion[(estado, simbolo)].append(accion)

    # ------------------------------------------------------------------
    # Algoritmo 4.46
    # ------------------------------------------------------------------
    def construir(self):
        g = self.aumentada
        automata = self.automata

        # Paso 1: la colección C = {I0, I1, ..., In} ya está en automata.estados.
        # Paso 2: llenar ACTION revisando cada ítem de cada estado.
        for i in range(len(automata.estados)):
            for item in automata.estados[i]:
                a = automata.simbolo_despues_del_punto(item)
                regla = automata.regla(item)

                if a is not None and g.es_terminal(a):
                    # (a) Si A -> α.aβ está en Ii (a terminal) y GOTO(Ii, a) = Ij,
                    #     entonces ACTION[i, a] = shift j
                    j = automata.transiciones[(i, a)]
                    self.agregar(i, a, ("shift", j))

                elif a is None:                     # ítem completo A -> α.
                    if regla.cabeza == INICIAL_AUMENTADO:
                        # (c) Si S' -> S. está en Ii, ACTION[i, $] = accept
                        self.agregar(i, FIN, ("accept", 0))
                    else:
                        # (b) Si A -> α. está en Ii, para cada a en FOLLOW(A):
                        #     ACTION[i, a] = reduce A -> α
                        for b in self.ff.follow[regla.cabeza]:
                            self.agregar(i, b, ("reduce", regla.numero))

        # Paso 3: si GOTO(Ii, A) = Ij con A no terminal, GOTO[i, A] = j
        for (i, X) in automata.transiciones:
            if g.es_no_terminal(X):
                self.goto[(i, X)] = automata.transiciones[(i, X)]

        # Paso 4: las casillas que no se llenaron son "error".
        # Paso 5: el estado inicial es el 0 (el que tiene S' -> .S).

    def conflictos(self):
        """Casillas de ACTION con 2 o más acciones (shift/reduce o
        reduce/reduce, Sección 4.5.4)."""
        lista = []
        for casilla in sorted(self.accion):
            if len(self.accion[casilla]) > 1:
                lista.append(casilla)
        return lista

    def es_slr1(self):
        """La gramática es SLR(1) si y solo si la tabla no tiene conflictos."""
        return len(self.conflictos()) == 0

    def imprimir(self):
        """Imprime las reglas y la tabla ACTION | GOTO (estilo Figura 4.37)."""
        print("Productions:")
        for regla in self.gramatica.producciones:
            print("  (" + str(regla.numero) + ") " + str(regla))
        terminales = sorted(self.gramatica.terminales) + [FIN]
        no_terminales = sorted(self.gramatica.no_terminales)
        filas = list(range(len(self.automata.estados)))
        contenido = {}
        for (estado, a) in self.accion:
            textos = []
            for accion in self.accion[(estado, a)]:
                textos.append(texto_accion(accion))
            contenido[(estado, a)] = "/".join(sorted(textos))
        for (estado, A) in self.goto:
            contenido[(estado, A)] = str(self.goto[(estado, A)])
        imprimir_tabla("SLR(1) parsing table (ACTION: terminals and $, GOTO: nonterminals)",
                       filas, terminales + no_terminales, contenido)


def texto_accion(accion):
    """("shift", 5) -> 's5';  ("reduce", 3) -> 'r3';  ("accept", 0) -> 'acc'."""
    if accion[0] == "shift":
        return "s" + str(accion[1])
    if accion[0] == "reduce":
        return "r" + str(accion[1])
    return "acc"


class ParserSLR1:
    """Algoritmo de análisis LR (Algoritmo 4.44, Figura 4.36)."""

    def __init__(self, tabla_slr1):
        self.tabla = tabla_slr1
        self.reglas = tabla_slr1.aumentada.producciones   # regla número k = reglas[k]

    def analizar(self, entrada, traza=None):
        """Analiza la lista de símbolos `entrada` (que ya termina en '$').

        Devuelve la raíz del árbol si la cadena es aceptada, o None si no.
        Si `traza` es una lista, se guardan los pasos
        (STACK, SYMBOLS, INPUT, ACTION) como en la Figura 4.38.

        El libro usa una pila de estados. Nosotros llevamos además una pila
        de NODOS del árbol (es la columna SYMBOLS de la Figura 4.38):
          - shift: se mete una hoja con el terminal;
          - reduce A -> β: se sacan |β| nodos, que pasan a ser los hijos de
            un nodo nuevo A, y ese nodo se mete a la pila.
        """
        estados = [0]          # al inicio la pila tiene el estado 0
        nodos = []
        i = 0                  # posición de la letra actual

        while True:
            s = estados[-1]    # estado en el tope de la pila
            a = entrada[i]     # letra actual

            if (s, a) not in self.tabla.accion:
                # Casilla vacía: error, la cadena no es válida.
                self.anotar(traza, estados, nodos, entrada, i, "error")
                return None
            accion = self.tabla.accion[(s, a)][0]

            if accion[0] == "shift":
                # Desplazar: meter el estado nuevo y avanzar en la entrada.
                self.anotar(traza, estados, nodos, entrada, i, "shift " + str(accion[1]))
                estados.append(accion[1])
                nodos.append(hoja_terminal(a))
                i = i + 1

            elif accion[0] == "reduce":
                # Reducir por A -> β.
                regla = self.reglas[accion[1]]
                self.anotar(traza, estados, nodos, entrada, i, "reduce by " + str(regla))
                k = len(regla.cuerpo)          # |β|, que vale 0 si β = ε
                if k > 0:
                    hijos = nodos[len(nodos) - k:]      # los k nodos de arriba
                    nodos = nodos[:len(nodos) - k]      # se quitan de la pila
                    estados = estados[:len(estados) - k]
                else:
                    hijos = [hoja_epsilon()]
                t = estados[-1]                         # nuevo tope
                estados.append(self.tabla.goto[(t, regla.cabeza)])   # meter GOTO[t, A]
                nuevo = Nodo(regla.cabeza, regla)
                nuevo.hijos = hijos
                nodos.append(nuevo)

            else:
                # Aceptar: el único nodo que queda es la raíz S.
                self.anotar(traza, estados, nodos, entrada, i, "accept")
                return nodos[-1]

    def anotar(self, traza, estados, nodos, entrada, i, accion):
        """Guarda una fila de la traza (solo si se pidió la traza)."""
        if traza is None:
            return
        lista_estados = []
        for e in estados:
            lista_estados.append(str(e))
        lista_simbolos = []
        for n in nodos:
            lista_simbolos.append(n.simbolo)
        texto_estados = " ".join(lista_estados)
        texto_simbolos = "".join(lista_simbolos)
        traza.append((texto_estados, texto_simbolos, "".join(entrada[i:]), accion))
