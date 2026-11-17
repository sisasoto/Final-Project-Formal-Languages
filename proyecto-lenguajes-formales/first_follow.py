"""
first_follow.py - Ítem 1: conjuntos FIRST y FOLLOW
==================================================
Libro: Sección 4.4.2 "FIRST and FOLLOW".

  FIRST(X)  = letras (terminales) con las que puede EMPEZAR algo que salga
              de X. Si X puede desaparecer (producir ε), ε también está.
  FOLLOW(A) = letras que pueden aparecer JUSTO DESPUÉS de A.
              '$' está en FOLLOW(S).

El libro dice que las reglas se aplican "hasta que no se pueda agregar nada
a ningún conjunto". Por eso los dos cálculos usan un ciclo que se repite
mientras algún conjunto haya crecido.
"""

from grammar import EPSILON, FIN


class FirstFollow:
    """Calcula y guarda FIRST y FOLLOW de una gramática.

    self.first[X]  es un conjunto (set) para cada símbolo X.
    self.follow[A] es un conjunto (set) para cada no terminal A.
    """

    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.first = {}
        self.follow = {}
        self.calcular_first()
        self.calcular_follow()

    # ------------------------------------------------------------------
    # FIRST de cada símbolo (Sección 4.4.2, reglas 1, 2 y 3)
    # ------------------------------------------------------------------
    def calcular_first(self):
        g = self.gramatica

        # Regla 1: si X es terminal, FIRST(X) = {X}.
        for t in g.terminales:
            self.first[t] = {t}
        # Los no terminales empiezan con el conjunto vacío.
        for A in g.no_terminales:
            self.first[A] = set()

        cambio = True
        while cambio:                       # repetir mientras algo crezca
            cambio = False
            for p in g.producciones:        # para cada regla X -> Y1 Y2 ... Yk
                conjunto = self.first[p.cabeza]
                tamano_antes = len(conjunto)

                if p.es_epsilon():
                    # Regla 2: si X -> e, agregar ε a FIRST(X).
                    conjunto.add(EPSILON)
                else:
                    # Regla 3: agregar FIRST(Y1) sin ε. Si Y1 puede
                    # desaparecer, agregar también FIRST(Y2) sin ε, y así.
                    # Si TODOS los Yi pueden desaparecer, agregar ε.
                    todos_desaparecen = True
                    for Y in p.cuerpo:
                        for a in self.first[Y]:
                            if a != EPSILON:
                                conjunto.add(a)
                        if EPSILON not in self.first[Y]:
                            todos_desaparecen = False
                            break           # Y no desaparece: no seguimos
                    if todos_desaparecen:
                        conjunto.add(EPSILON)

                if len(conjunto) != tamano_antes:
                    cambio = True

    # ------------------------------------------------------------------
    # FIRST de una cadena X1 X2 ... Xn (Sección 4.4.2)
    # ------------------------------------------------------------------
    def first_de_cadena(self, simbolos):
        """FIRST(X1 X2 ... Xn).

        Igual que la regla 3: se agrega FIRST(X1) sin ε; si X1 puede
        desaparecer se agrega FIRST(X2) sin ε; etc. Si todos pueden
        desaparecer (o la cadena es vacía), se agrega ε.
        """
        resultado = set()
        for X in simbolos:
            for a in self.first[X]:
                if a != EPSILON:
                    resultado.add(a)
            if EPSILON not in self.first[X]:
                return resultado            # X no desaparece: terminamos
        resultado.add(EPSILON)
        return resultado

    # ------------------------------------------------------------------
    # FOLLOW de cada no terminal (Sección 4.4.2, reglas 1, 2 y 3)
    # ------------------------------------------------------------------
    def calcular_follow(self):
        g = self.gramatica
        for A in g.no_terminales:
            self.follow[A] = set()

        # Regla 1: '$' está en FOLLOW(S).
        self.follow[g.inicial].add(FIN)

        cambio = True
        while cambio:                       # repetir mientras algo crezca
            cambio = False
            for p in g.producciones:        # para cada regla A -> ...
                A = p.cabeza
                for i in range(len(p.cuerpo)):
                    B = p.cuerpo[i]
                    if not g.es_no_terminal(B):
                        continue            # FOLLOW solo es de no terminales

                    conjunto = self.follow[B]
                    tamano_antes = len(conjunto)
                    beta = p.cuerpo[i + 1:]               # lo que va después de B
                    first_beta = self.first_de_cadena(beta)

                    # Regla 2: si A -> αBβ, todo FIRST(β) menos ε va a FOLLOW(B).
                    for a in first_beta:
                        if a != EPSILON:
                            conjunto.add(a)

                    # Regla 3: si β puede desaparecer (o no hay β),
                    # todo FOLLOW(A) va a FOLLOW(B).
                    if EPSILON in first_beta:
                        for a in self.follow[A]:
                            conjunto.add(a)

                    if len(conjunto) != tamano_antes:
                        cambio = True

    # ------------------------------------------------------------------
    # Impresión con el formato exacto del enunciado (opción --sets)
    # ------------------------------------------------------------------
    def formato_conjunto(self, conjunto):
        """Devuelve el texto '{a, d, e, $}': primero los terminales en orden
        ASCII, luego 'e' (si está) y al final '$' (si está)."""
        terminales = []
        for x in conjunto:
            if x != EPSILON and x != FIN:
                terminales.append(x)
        terminales.sort()                   # sort() ordena por código ASCII
        if EPSILON in conjunto:
            terminales.append(EPSILON)
        if FIN in conjunto:
            terminales.append(FIN)
        return "{" + ", ".join(terminales) + "}"

    def imprimir(self):
        """Imprime todas las líneas First(...) y luego todas las Follow(...),
        con los no terminales en orden alfabético."""
        no_terminales = sorted(self.gramatica.no_terminales)
        for A in no_terminales:
            print("First(" + A + ") = " + self.formato_conjunto(self.first[A]))
        for A in no_terminales:
            print("Follow(" + A + ") = " + self.formato_conjunto(self.follow[A]))
