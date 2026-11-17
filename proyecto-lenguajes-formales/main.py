"""
main.py - Ítems 1 y 2
=====================
Programa con la entrada y salida EXACTAS de la Sección 2.2 del enunciado.

Cómo se usa (desde la carpeta del proyecto):
    python main.py              ejecución normal
    python main.py --sets       además imprime FIRST y FOLLOW
    python main.py --tables     además imprime la tabla LL(1), el autómata LR(0)
                                y la tabla SLR(1) (para el informe)
    python main.py --trace      antes de cada yes/no imprime el análisis paso a paso

Qué hace (Sección 2.2.2 del enunciado):
  1. Si la gramática es LL(1) y SLR(1): muestra el menú
     "Select a parser (T: for LL(1), B: for SLR(1), Q: quit):"
  2. Si solo es LL(1):  "Grammar is LL(1)."  y analiza cadenas con LL(1)
  3. Si solo es SLR(1): "Grammar is SLR(1)." y analiza cadenas con SLR(1)
  4. Si no es ninguna:  "Grammar is neither LL(1) nor SLR(1)." y termina
Las cadenas se leen una por línea hasta una línea vacía; 'e' es la cadena vacía.
"""

import sys

sys.dont_write_bytecode = True   # evita que Python cree la carpeta __pycache__

from grammar import leer_gramatica, tokenizar
from first_follow import FirstFollow
from ll1 import TablaLL1, ParserLL1, imprimir_traza
from slr1 import TablaSLR1, ParserSLR1

MENU = "Select a parser (T: for LL(1), B: for SLR(1), Q: quit):"


class Programa:
    """Lee la gramática, decide qué parsers sirven y analiza las cadenas."""

    def __init__(self, opciones):
        self.opciones = opciones        # por ejemplo ["--sets"]

    def leer_linea(self):
        """Lee una línea de la entrada. Devuelve None si ya no hay más
        líneas (fin de archivo). Quita el salto de línea del final."""
        linea = sys.stdin.readline()
        if linea == "":
            return None
        return linea.rstrip("\r\n")     # \r aparece en archivos de Windows

    def leer_entrada_gramatica(self):
        """Lee el número n y luego n líneas con producciones."""
        linea = self.leer_linea()
        while linea is not None and linea.strip() == "":   # saltar líneas vacías
            linea = self.leer_linea()
        n = int(linea.strip())
        lineas = []
        while len(lineas) < n:
            linea = self.leer_linea()
            if linea is None:
                break
            if linea.strip() != "":
                lineas.append(linea)
        return leer_gramatica(lineas)

    def analizar_cadenas(self, parser, tipo):
        """Lee cadenas hasta una línea vacía e imprime yes o no por cada una."""
        while True:
            linea = self.leer_linea()
            if linea is None or linea.strip() == "":
                return
            entrada = tokenizar(linea)

            if "--trace" in self.opciones:
                traza = []
                arbol = parser.analizar(entrada, traza)
                if tipo == "LL1":
                    imprimir_traza(traza, ["MATCHED", "STACK", "INPUT", "ACTION"])
                else:
                    imprimir_traza(traza, ["STACK", "SYMBOLS", "INPUT", "ACTION"])
            else:
                arbol = parser.analizar(entrada)

            if arbol is not None:
                print("yes", flush=True)
            else:
                print("no", flush=True)

    def ejecutar(self):
        gramatica = self.leer_entrada_gramatica()

        # Ítem 1: FIRST y FOLLOW.
        ff = FirstFollow(gramatica)
        if "--sets" in self.opciones:
            ff.imprimir()

        # Ítem 2: construir las dos tablas y ver si tienen conflictos.
        tabla_ll1 = TablaLL1(gramatica, ff)
        tabla_slr1 = TablaSLR1(gramatica, ff)
        es_ll1 = tabla_ll1.es_ll1()
        es_slr1 = tabla_slr1.es_slr1()

        if "--tables" in self.opciones:
            tabla_ll1.imprimir()
            tabla_slr1.automata.imprimir()
            tabla_slr1.imprimir()

        parser_ll1 = ParserLL1(tabla_ll1)
        parser_slr1 = ParserSLR1(tabla_slr1)

        if es_ll1 and es_slr1:
            # Caso 1: las dos sirven; el usuario elige.
            while True:
                print(MENU, flush=True)
                opcion = self.leer_linea()
                if opcion is None:
                    return
                opcion = opcion.strip().upper()
                if opcion == "Q":
                    return
                elif opcion == "T":
                    self.analizar_cadenas(parser_ll1, "LL1")
                elif opcion == "B":
                    self.analizar_cadenas(parser_slr1, "SLR1")
                # Con cualquier otra letra se vuelve a mostrar el menú.

        elif es_ll1:
            # Caso 2: solo LL(1).
            print("Grammar is LL(1).", flush=True)
            self.analizar_cadenas(parser_ll1, "LL1")

        elif es_slr1:
            # Caso 3: solo SLR(1).
            print("Grammar is SLR(1).", flush=True)
            self.analizar_cadenas(parser_slr1, "SLR1")

        else:
            # Caso 4: ninguna.
            print("Grammar is neither LL(1) nor SLR(1).", flush=True)


if __name__ == "__main__":
    Programa(sys.argv[1:]).ejecutar()
