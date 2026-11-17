"""
sdd_main.py - Ítem 3
====================
Programa del evaluador de la SDD.

Cómo se usa (desde la carpeta del proyecto):
    python sdd_main.py              evalúa nuestra SDD
    python sdd_main.py --info       imprime la tabla de atributos y las reglas
    python sdd_main.py --graph      imprime también las flechas del grafo
    python sdd_main.py --circular   usa la versión con una regla circular (Paso 6)
    python sdd_main.py --html       además crea visualizer.html y lo abre (visualizador
                                    opcional del Paso 5) en el navegador
Las opciones se pueden combinar, por ejemplo:  --circular --html

Las cadenas se leen una por línea hasta una línea vacía. Para cada una:
  - si no está en el lenguaje: imprime 'no'
  - si está: imprime el árbol anotado, el orden de evaluación y el valor de S.v
"""

import os
import pathlib                    # biblioteca estándar: rutas de archivos
import sys
import webbrowser                 # biblioteca estándar: abre una página en el navegador

sys.dont_write_bytecode = True   # evita que Python cree la carpeta __pycache__

from grammar import tokenizar
from first_follow import FirstFollow
from ll1 import TablaLL1, ParserLL1
from slr1 import TablaSLR1, ParserSLR1
from sdd import crear_sdd
from evaluator import EvaluadorSDD, SDDCircular
from visualizer import datos_de_un_caso, escribir_html


class ProgramaSDD:
    """Une el parser del Ítem 2 con el evaluador del Ítem 3."""

    def __init__(self, opciones):
        self.opciones = opciones
        self.sdd = crear_sdd(circular="--circular" in opciones)

    def crear_parser(self):
        """Construye el parser que dice la SDD, con NUESTRO código del Ítem 2,
        y revisa que la gramática sea LL(1) o SLR(1) (requisito G1)."""
        gramatica = self.sdd.gramatica()
        ff = FirstFollow(gramatica)
        if self.sdd.parser == "LL1":
            tabla = TablaLL1(gramatica, ff)
            if not tabla.es_ll1():
                return None
            return ParserLL1(tabla)
        tabla = TablaSLR1(gramatica, ff)
        if not tabla.es_slr1():
            return None
        return ParserSLR1(tabla)

    def ejecutar(self):
        # 1. Revisar que la SDD esté bien definida.
        errores = self.sdd.validar()
        if len(errores) > 0:
            print("The SDD is not well defined:")
            for e in errores:
                print("  - " + e)
            return

        if "--info" in self.opciones:
            print(self.sdd.describir())
            print()

        # 2. Construir el parser.
        parser = self.crear_parser()
        if parser is None:
            print("The SDD grammar is not " + self.sdd.parser + ".")
            return
        evaluador = EvaluadorSDD(self.sdd)

        if self.sdd.parser == "LL1":
            nombre_parser = "LL(1)"
        else:
            nombre_parser = "SLR(1)"
        print("SDD: " + self.sdd.nombre + ". Parser: " + nombre_parser + ".")
        print("Enter one string per line (empty line to finish):", flush=True)

        # 3. Leer cadenas hasta una línea vacía.
        casos_html = []                      # lo que se mostrará en el HTML
        while True:
            linea = sys.stdin.readline()
            if linea.strip() == "":          # línea vacía o fin de archivo
                break
            linea = linea.strip()

            arbol = parser.analizar(tokenizar(linea))
            if arbol is None:
                print("no", flush=True)
                continue

            try:
                orden = evaluador.evaluar(arbol)
            except SDDCircular as error:
                print(error)
                print("Evaluation stopped.")
                if "--html" in self.opciones:
                    casos_html.append(datos_de_un_caso(linea, arbol, evaluador.grafo, [],
                                                       self.sdd, circular=True))
                break

            grafo = evaluador.grafo
            if "--html" in self.opciones:
                casos_html.append(datos_de_un_caso(linea, arbol, grafo, orden, self.sdd))
            print("String: " + linea)
            print("Annotated parse tree:")
            print(arbol.dibujar())
            if "--graph" in self.opciones:
                print(grafo.describir())
            print("Evaluation order:")
            paso = 1
            for vertice in orden:
                r, nodo = grafo.regla_de[vertice]
                valor = grafo.nodos[vertice[0]].atributos[vertice[1]]
                print("    " + str(paso).rjust(2) + ". " + grafo.nombre(vertice) +
                      " = " + str(valor) + "    (" + r["texto"] + ")")
                paso = paso + 1
            print("Result: S." + self.sdd.atributo_principal + " = " + str(evaluador.resultado(arbol)))
            print(flush=True)

        # 4. Visualizador opcional: una sola página con todas las cadenas.
        if "--html" in self.opciones:
            archivo = escribir_html(casos_html, self.sdd)
            ruta = os.path.abspath(archivo)
            print("Visualizer written to " + ruta)
            # Abrir la página en el navegador predeterminado (como doble clic).
            # as_uri() convierte la ruta en una dirección file:///C:/... que
            # entiende el navegador.
            direccion = pathlib.Path(ruta).as_uri()
            if not webbrowser.open(direccion):
                print("Open that file in a web browser (double-click it).")


if __name__ == "__main__":
    ProgramaSDD(sys.argv[1:]).ejecutar()
