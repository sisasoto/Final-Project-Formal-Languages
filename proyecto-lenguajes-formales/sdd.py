"""
sdd.py - Ítem 3: la SDD guardada como DATOS
===========================================
Libro:
  - Sección 5.1.1: atributos sintetizados y heredados. Cada regla semántica
    tiene la forma  b = f(c1, ..., ck).
  - Figura 5.1: tabla "Producción | Reglas semánticas".

El enunciado (Paso 5.1) pide que la SDD se guarde como datos: el evaluador
(evaluator.py) no debe saber nada de esta SDD en particular. Por eso aquí
NO se evalúa nada: solo se describe la SDD.

----------------------------------------------------------------------------
NUESTRA SDD: calculadora en notación prefija
----------------------------------------------------------------------------
Gramática (es LL(1) y SLR(1); tiene 4 no terminales y 17 reglas; E y R son
recursivos):

    S -> E
    E -> O(ER) | 0 | 1 | ... | 9   una operación con sus argumentos, o un dígito
    O -> + | * | -                 el operador
    R -> ,ER | e                   los argumentos que siguen después de una coma

El operador va ADELANTE y se aplica a todos sus argumentos, de izquierda a
derecha. Ejemplos:
    +(1,2)       = 1 + 2           = 3
    -(9,2,3)     = (9 - 2) - 3     = 4
    *(2,-(5,1))  = 2 * (5 - 1)     = 8

  op  (O: sintetizado; R: heredado): el operador. Sube desde la hoja del
       operador hasta O, y de ahí pasa a su hermano R y baja por los R.
  acc (R: heredado): el resultado acumulado de los argumentos que están a la
       izquierda (como la variable acumuladora de un ciclo for).
  val (sintetizado): el valor de la expresión. S.val es el resultado.

La técnica del acumulador heredado (acc baja, y R -> e lo devuelve como val)
es la de la Figura 5.4 del libro (T'.inh). La aplicamos a notación prefija,
con un atributo heredado nuevo (op) que decide qué operación hacer.

¿Cómo se escribe una regla semántica?
  Como un diccionario con cuatro datos:
    "define":  el atributo que la regla calcula
    "usa":     la lista de atributos que necesita
    "funcion": la función de Python que hace el cálculo
    "texto":   la regla escrita como en el libro (solo para mostrarla)

  Un atributo se indica con una pareja (posición, nombre):
    posición 0 = la cabeza de la regla; posición 1, 2, ... = los símbolos
    del cuerpo de izquierda a derecha.
  Ejemplo, en la regla  E -> O ( E1 R )  (0 = E, 1 = O, 2 = '(', 3 = E1,
  4 = R, 5 = ')'):
    "R.op = O.op"  se escribe  define (4, "op"), usa [(1, "op")]
"""

from grammar import leer_gramatica

SINTETIZADO = "synthesized"
HEREDADO = "inherited"
LEXVAL = "lexval"     # atributo de los terminales: el mismo carácter


# ----------------------------------------------------------------------
# Funciones que hacen los cálculos de las reglas semánticas
# ----------------------------------------------------------------------
def copiar(x):
    return x


def a_entero(caracter):
    """El lexval de un dígito es un carácter ('7'); su valor es el número 7."""
    return int(caracter)


def operar(operador, a, b):
    """Aplica el operador ('+', '*' o '-') a los números a y b."""
    if operador == "+":
        return a + b
    if operador == "*":
        return a * b
    return a - b


def regla(define, usa, funcion, texto):
    """Arma el diccionario de una regla semántica."""
    return {"define": define, "usa": usa, "funcion": funcion, "texto": texto}


def atributo(simbolo, nombre, tipo, dato, significado):
    """Arma una fila de la tabla de atributos (enunciado, Paso 2.1)."""
    return {"simbolo": simbolo, "nombre": nombre, "tipo": tipo,
            "dato": dato, "significado": significado}


class SDD:
    """Una SDD completa.

    nombre             : nombre para mostrar
    lineas_gramatica   : la gramática en el formato de la entrada
    atributos          : tabla de atributos (lista de diccionarios)
    reglas             : diccionario {"texto de la producción": [reglas]}
    atributo_principal : atributo de S que es el resultado
    parser             : "LL1" o "SLR1", el parser del Ítem 2 que se usa
    """

    def __init__(self, nombre, lineas_gramatica, atributos, reglas,
                 atributo_principal, parser):
        self.nombre = nombre
        self.lineas_gramatica = lineas_gramatica
        self.atributos = atributos
        self.reglas = reglas
        self.atributo_principal = atributo_principal
        self.parser = parser
        # La primera línea es el número n; las demás son las producciones.
        self.la_gramatica = leer_gramatica(lineas_gramatica[1:])

    def gramatica(self):
        return self.la_gramatica

    def reglas_de(self, produccion):
        """Reglas semánticas de una producción (lista vacía si no tiene)."""
        return self.reglas.get(str(produccion), [])

    def tipo_de(self, simbolo, nombre):
        """'synthesized', 'inherited' o None si el atributo no existe."""
        for a in self.atributos:
            if a["simbolo"] == simbolo and a["nombre"] == nombre:
                return a["tipo"]
        return None

    def atributo_existe(self, simbolos, posicion, nombre):
        """True si en la producción (lista simbolos: cabeza y cuerpo) la
        posición existe y su símbolo tiene ese atributo. Un terminal solo
        tiene lexval (lo da el "scanner"); un no terminal tiene los
        atributos de la tabla."""
        if posicion < 0 or posicion >= len(simbolos):
            return False
        simbolo = simbolos[posicion]
        if self.gramatica().es_terminal(simbolo):
            return nombre == LEXVAL
        return self.tipo_de(simbolo, nombre) is not None

    # ------------------------------------------------------------------
    # Revisiones que pide el enunciado (Paso 2), según la Sección 5.1.1
    # ------------------------------------------------------------------
    def validar(self):
        """Devuelve una lista con los errores encontrados (vacía si la SDD
        está bien). Revisa que:
          - haya al menos un atributo sintetizado y uno heredado;
          - S no tenga atributos heredados;
          - cada regla defina un sintetizado de la cabeza o un heredado de
            un símbolo del cuerpo;
          - cada regla use solo atributos (que existan) de los símbolos de
            esa misma producción;
          - en cada producción, cada atributo que hay que definir se defina
            EXACTAMENTE una vez.
        """
        g = self.gramatica()
        errores = []

        tipos = []
        for a in self.atributos:
            tipos.append(a["tipo"])
        if SINTETIZADO not in tipos or HEREDADO not in tipos:
            errores.append("The SDD needs at least one synthesized and one inherited attribute.")
        for a in self.atributos:
            if a["simbolo"] == g.inicial and a["tipo"] == HEREDADO:
                errores.append("The start symbol S must not have inherited attributes.")

        for p in g.producciones:
            simbolos = [p.cabeza] + p.cuerpo     # posición -> símbolo
            definidos = []

            for r in self.reglas_de(p):
                posicion, nombre = r["define"]
                if posicion < 0 or posicion >= len(simbolos):
                    errores.append(str(p) + ": '" + r["texto"] + "' defines an attribute of position " +
                                   str(posicion) + ", which is not in the production.")
                    continue

                # Lo que la regla USA también tiene que ser de esta misma
                # producción y tiene que existir (Sección 5.1.1).
                for (posicion_usada, nombre_usado) in r["usa"]:
                    if not self.atributo_existe(simbolos, posicion_usada, nombre_usado):
                        errores.append(str(p) + ": '" + r["texto"] + "' uses an attribute that is not in "
                                       "this production (position " + str(posicion_usada) +
                                       ", attribute '" + nombre_usado + "').")

                tipo = self.tipo_de(simbolos[posicion], nombre)
                if posicion == 0 and tipo != SINTETIZADO:
                    errores.append(str(p) + ": '" + r["texto"] + "' must define a synthesized attribute of the head.")
                if posicion > 0 and tipo != HEREDADO:
                    errores.append(str(p) + ": '" + r["texto"] + "' must define an inherited attribute of the body.")
                definidos.append(r["define"])

            # Lo que la producción TIENE que definir:
            # los sintetizados de la cabeza ...
            obligatorios = []
            for a in self.atributos:
                if a["simbolo"] == p.cabeza and a["tipo"] == SINTETIZADO:
                    obligatorios.append((0, a["nombre"]))
            # ... y los heredados de cada no terminal del cuerpo.
            for posicion in range(1, len(simbolos)):
                if g.es_no_terminal(simbolos[posicion]):
                    for a in self.atributos:
                        if a["simbolo"] == simbolos[posicion] and a["tipo"] == HEREDADO:
                            obligatorios.append((posicion, a["nombre"]))

            for (posicion, nombre) in obligatorios:
                veces = definidos.count((posicion, nombre))
                if veces != 1:
                    errores.append(str(p) + ": " + simbolos[posicion] + "." + nombre +
                                   " is defined " + str(veces) + " times (must be exactly 1).")
        return errores

    def describir(self):
        """Texto con la gramática, la tabla de atributos y las reglas
        semánticas (formato de la Figura 5.1). Sirve para el informe."""
        lineas = ["SDD: " + self.nombre, "", "Grammar:"]
        for linea in self.lineas_gramatica[1:]:
            lineas.append("  " + linea)
        lineas.append("")
        lineas.append("Attributes:")
        lineas.append("  " + "Symbol".ljust(8) + "Attr".ljust(8) + "Kind".ljust(13) + "Type".ljust(6) + "Meaning")
        for a in self.atributos:
            lineas.append("  " + a["simbolo"].ljust(8) + a["nombre"].ljust(8) + a["tipo"].ljust(13) +
                          a["dato"].ljust(6) + a["significado"])
        lineas.append("")
        lineas.append("Semantic rules:")
        lineas.append("  " + "Production".ljust(14) + "Semantic rules")
        for p in self.gramatica().producciones:
            textos = []
            for r in self.reglas_de(p):
                textos.append(r["texto"])
            lineas.append("  " + str(p).ljust(14) + "; ".join(textos))
        return "\n".join(lineas)


# ============================================================================
# Los DATOS de nuestra SDD
# ============================================================================
def crear_sdd(circular=False):
    """Crea nuestra SDD.

    Con circular=True se cambia UNA regla para que la SDD sea circular
    (enunciado, Paso 6): en E -> O(E1 R) la regla R.acc = E1.val pasa a ser
    R.acc = E.val. Como E.val necesita a R.val, R.val necesita al acc del
    último R, y ese acc depende (a través de los R) de R.acc, se forma el
    ciclo  R.acc -> ... -> R.val -> E.val -> R.acc.
    """
    digitos = "0123456789"
    lineas_gramatica = [
        "4",
        "S -> E",
        "E -> O(ER) " + " ".join(digitos),
        "O -> + * -",
        "R -> ,ER e",
    ]

    atributos = [
        atributo("S", "val", SINTETIZADO, "int", "value of the whole expression (main attribute)"),
        atributo("E", "val", SINTETIZADO, "int", "value of the expression E"),
        atributo("O", "op", SINTETIZADO, "char", "the operator: '+', '*' or '-'"),
        atributo("R", "op", HEREDADO, "char", "operator to apply to the remaining arguments"),
        atributo("R", "acc", HEREDADO, "int", "result of the arguments to the left of R"),
        atributo("R", "val", SINTETIZADO, "int", "result after applying op to all the arguments"),
        atributo("terminal", LEXVAL, SINTETIZADO, "char", "the character itself (given by the scanner)"),
    ]

    if circular:
        regla_R_acc = regla((4, "acc"), [(0, "val")], copiar, "R.acc = E.val   <-- CIRCULAR")
    else:
        regla_R_acc = regla((4, "acc"), [(3, "val")], copiar, "R.acc = E1.val")

    reglas = {
        # S -> E           posiciones: 0=S, 1=E
        "S -> E": [
            regla((0, "val"), [(1, "val")], copiar, "S.val = E.val"),
        ],
        # E -> O ( E1 R )  posiciones: 0=E, 1=O, 2='(', 3=E1, 4=R, 5=')'
        "E -> O(ER)": [
            regla((4, "op"), [(1, "op")], copiar, "R.op = O.op"),
            regla_R_acc,
            regla((0, "val"), [(4, "val")], copiar, "E.val = R.val"),
        ],
        # R -> , E R1      posiciones: 0=R, 1=',', 2=E, 3=R1
        "R -> ,ER": [
            regla((3, "op"), [(0, "op")], copiar, "R1.op = R.op"),
            regla((3, "acc"), [(0, "op"), (0, "acc"), (2, "val")], operar,
                  "R1.acc = R.acc (R.op) E.val"),
            regla((0, "val"), [(3, "val")], copiar, "R.val = R1.val"),
        ],
        # R -> e
        "R -> e": [
            regla((0, "val"), [(0, "acc")], copiar, "R.val = R.acc"),
        ],
    }
    # O -> operador    posiciones: 0=O, 1=operador   (una regla por operador)
    for operador in "+*-":
        reglas["O -> " + operador] = [
            regla((0, "op"), [(1, LEXVAL)], copiar, "O.op = " + operador + ".lexval"),
        ]
    # E -> dígito      posiciones: 0=E, 1=dígito     (una regla por dígito)
    for digito in digitos:
        reglas["E -> " + digito] = [
            regla((0, "val"), [(1, LEXVAL)], a_entero, "E.val = digit.lexval"),
        ]

    nombre = "Prefix calculator"
    if circular:
        nombre = nombre + " (CIRCULAR)"
    return SDD(nombre, lineas_gramatica, atributos, reglas, "val", "LL1")
