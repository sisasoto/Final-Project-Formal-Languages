"""
grammar.py - La gramática
=========================
Guarda una gramática libre de contexto.

Libro: Sección 4.2.1 (qué es una gramática) y Sección 4.6.2 (gramática
aumentada).

Reglas de la entrada (enunciado, Sección 2.2):
  - 'S' siempre es el símbolo inicial.
  - Los no terminales son letras mayúsculas.
  - Los terminales son caracteres que no son mayúsculas.
  - 'e' significa la cadena vacía (ε).
  - '$' marca el final de una cadena (lo agrega el programa).
"""

# Constantes que usan todos los archivos del proyecto
EPSILON = "e"            # así se escribe ε
FIN = "$"                # marcador de fin de la cadena
INICIAL_AUMENTADO = "S'"  # símbolo inicial nuevo de la gramática aumentada


class Produccion:
    """Una regla de la gramática:  cabeza -> cuerpo

    Ejemplo: la regla  A -> aA  se guarda así:
        cabeza = "A"
        cuerpo = ["a", "A"]
        numero = el número de la regla (sirve para imprimir "r3" en la tabla)

    La regla  A -> e  (vacía) tiene cuerpo = [].
    """

    def __init__(self, cabeza, cuerpo, numero):
        self.cabeza = cabeza
        self.cuerpo = cuerpo
        self.numero = numero

    def es_epsilon(self):
        """True si la regla es A -> e (el cuerpo está vacío)."""
        return len(self.cuerpo) == 0

    def __str__(self):
        """Texto de la regla, por ejemplo 'A -> aA' o 'B -> e'."""
        if self.es_epsilon():
            derecha = EPSILON
        else:
            derecha = "".join(self.cuerpo)
        return self.cabeza + " -> " + derecha


class Gramatica:
    """Una gramática G = (no terminales, terminales, producciones, inicial)."""

    def __init__(self, producciones, inicial="S"):
        self.producciones = producciones
        self.inicial = inicial

        # Los no terminales son los que aparecen a la izquierda de una regla.
        self.no_terminales = set()
        for p in producciones:
            self.no_terminales.add(p.cabeza)

        # Los terminales son los demás símbolos que aparecen en los cuerpos.
        self.terminales = set()
        for p in producciones:
            for simbolo in p.cuerpo:
                if simbolo not in self.no_terminales:
                    self.terminales.add(simbolo)

    def producciones_de(self, A):
        """Lista con todas las reglas cuya cabeza es A."""
        resultado = []
        for p in self.producciones:
            if p.cabeza == A:
                resultado.append(p)
        return resultado

    def es_no_terminal(self, simbolo):
        return simbolo in self.no_terminales

    def es_terminal(self, simbolo):
        return simbolo in self.terminales

    def aumentada(self):
        """Gramática aumentada G' (Libro, Sección 4.6.2).

        Se agrega un símbolo inicial nuevo S' con la regla S' -> S (número 0).
        El parser SLR sabe que terminó cuando puede reducir por S' -> S.
        Como la regla nueva tiene número 0 y las demás 1, 2, 3, ..., en la
        gramática aumentada la regla número k está en la posición k de la lista.
        """
        regla_nueva = Produccion(INICIAL_AUMENTADO, [self.inicial], 0)
        return Gramatica([regla_nueva] + self.producciones, INICIAL_AUMENTADO)


def leer_gramatica(lineas):
    """Convierte las líneas de la entrada en una Gramatica.

    Cada línea tiene la forma   A -> alt1 alt2 ...
    Las alternativas se separan con espacios. Por ejemplo:
        "B -> bBc e"  da las reglas  B -> bBc  y  B -> e
    Las reglas se numeran 1, 2, 3, ... en el orden en que aparecen.
    """
    producciones = []
    numero = 1
    for linea in lineas:
        linea = linea.strip()
        if linea == "":
            continue
        partes = linea.split("->", 1)       # ["B ", " bBc e"]
        cabeza = partes[0].strip()          # "B"
        alternativas = partes[1].split()    # ["bBc", "e"]
        for alternativa in alternativas:
            if alternativa == EPSILON:
                cuerpo = []
            else:
                cuerpo = list(alternativa)  # "bBc" -> ["b", "B", "c"]
            producciones.append(Produccion(cabeza, cuerpo, numero))
            numero = numero + 1
    return Gramatica(producciones)


def tokenizar(texto):
    """Convierte una cadena de entrada en la lista de símbolos que lee el
    parser, y le agrega '$' al final.
        "adbc" -> ["a", "d", "b", "c", "$"]
        "e"    -> ["$"]        (la cadena vacía)
    """
    texto = texto.strip()
    if texto == EPSILON:
        simbolos = []
    else:
        simbolos = list(texto)
    simbolos.append(FIN)
    return simbolos
