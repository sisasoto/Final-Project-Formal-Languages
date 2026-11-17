"""
visualizer.py - Ítem 3 (opcional): visualizador en HTML
=======================================================
El enunciado (Paso 5, "Optional: visualizer") propone mostrar el árbol, el
grafo de dependencias y la evaluación paso a paso.

Este archivo NO evalúa nada: solo toma lo que ya calcularon el parser y el
evaluador (el árbol, el grafo y el orden topológico) y lo guarda como datos
JSON dentro de una página HTML. El dibujo lo hace el JavaScript de
visualizer_template.html, en el navegador.

Uso:  python sdd_main.py --html      (crea el archivo visualizer.html)
"""

import json
import os

from sdd import HEREDADO, LEXVAL

PLANTILLA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "visualizer_template.html")
MARCA = "/*__DATOS__*/null"      # en la plantilla, aquí se ponen los datos


def clave(vertice):
    """Un vértice (4, 'd') se escribe como el texto '4.d' para el JSON."""
    return str(vertice[0]) + "." + vertice[1]


def datos_de_un_caso(cadena, raiz, grafo, orden, sdd, circular=False):
    """Convierte un árbol ya evaluado (o uno circular) en un diccionario
    sencillo que se puede escribir como JSON.

    cadena  : la cadena de entrada
    raiz    : raíz del árbol (ya numerado por el evaluador)
    grafo   : el GrafoDependencias que construyó el evaluador
    orden   : lista de vértices en el orden en que se calcularon
    circular: True si el grafo tiene un ciclo (no se evaluó nada)
    """
    # 1. Los nodos del árbol, con los atributos que tiene cada uno.
    atributos_de_nodo = {}
    for v in grafo.vertices:
        atributos_de_nodo.setdefault(v[0], []).append(v[1])

    nodos = []
    for nodo in raiz.todos_los_nodos():
        nombres = atributos_de_nodo.get(nodo.id, [])
        # Como en las figuras del libro: heredados a la izquierda y
        # sintetizados a la derecha.
        heredados = sorted(n for n in nombres if sdd.tipo_de(nodo.simbolo, n) == HEREDADO)
        otros = sorted(n for n in nombres if n not in heredados)
        produccion = ""
        if nodo.produccion is not None:
            produccion = str(nodo.produccion)
        nodos.append({
            "id": nodo.id,
            "simbolo": nodo.simbolo,
            "produccion": produccion,
            "hijos": [h.id for h in nodo.hijos],
            "atributos": heredados + otros,
        })

    # 2. Los vértices del grafo: valor final, regla que lo calcula y tipo.
    vertices = {}
    for v in grafo.vertices:
        nodo = grafo.nodos[v[0]]
        valor = nodo.atributos.get(v[1])
        if v in grafo.regla_de:
            texto_regla = grafo.regla_de[v][0]["texto"]
        else:
            texto_regla = "given by the scanner"
        if v[1] == LEXVAL:
            tipo = "lexval"
        elif sdd.tipo_de(nodo.simbolo, v[1]) == HEREDADO:
            tipo = "inherited"
        else:
            tipo = "synthesized"
        vertices[clave(v)] = {
            "nombre": grafo.nombre(v),
            "atributo": v[1],
            "valor": None if valor is None else str(valor),
            "regla": texto_regla,
            "tipo": tipo,
        }

    # 3. Las flechas u -> v del grafo (v usa a u).
    flechas = []
    for u in sorted(grafo.vertices):
        for v in grafo.flechas[u]:
            flechas.append([clave(u), clave(v)])

    resultado = None
    if not circular:
        resultado = str(raiz.atributos.get(sdd.atributo_principal))

    return {
        "cadena": cadena,
        "nodos": nodos,
        "vertices": vertices,
        "flechas": flechas,
        "orden": [clave(v) for v in orden],
        "circular": circular,
        "no_ordenados": [clave(v) for v in grafo.no_ordenados],
        "resultado": resultado,
    }


def escribir_html(casos, sdd, archivo="visualizer.html"):
    """Escribe la página con todos los casos. Devuelve la ruta del archivo."""
    datos = {
        "sdd": sdd.nombre,
        "principal": sdd.atributo_principal,
        "reglas": sdd.describir(),
        "casos": casos,
    }
    texto_json = json.dumps(datos, ensure_ascii=False)
    # "</" dentro de un <script> podría cerrar la etiqueta antes de tiempo.
    texto_json = texto_json.replace("</", "<\\/")

    with open(PLANTILLA, encoding="utf-8") as f:
        pagina = f.read()
    pagina = pagina.replace(MARCA, texto_json)

    with open(archivo, "w", encoding="utf-8") as f:
        f.write(pagina)
    return archivo
