"""
gauss_jordan.py
Motor para resolver sistemas de ecuaciones con Gauss-Jordan.

No usa NumPy ni librerías externas.
Usa únicamente la librería estándar fractions para trabajar con
resultados exactos cuando se solicitan fracciones.
"""

from fractions import Fraction


def formatear(numero, modo="fraccion"):
    """Convierte un número a texto en fracción o decimal."""
    numero = Fraction(numero)

    if modo == "decimal":
        return f"{float(numero):.6f}".rstrip("0").rstrip(".")

    if numero.denominator == 1:
        return str(numero.numerator)

    return f"{numero.numerator}/{numero.denominator}"


def formatear_operacion(operacion, modo="fraccion"):
    """Formatea una operación de fila guardada como datos."""
    tipo = operacion[0]

    if tipo == "intercambio":
        _, a, b = operacion
        return f"F{a} <-> F{b}"

    if tipo == "normalizar":
        _, fila, pivote = operacion
        return f"F{fila} -> F{fila} / {formatear(pivote, modo)}"

    if tipo == "eliminar":
        _, fila, pivote_fila, factor = operacion

        if factor > 0:
            signo = "-"
            valor = factor
        else:
            signo = "+"
            valor = -factor

        valor_texto = formatear(valor, modo)

        if valor == 1:
            valor_texto = ""

        return f"F{fila} -> F{fila} {signo} {valor_texto}F{pivote_fila}"


def matriz_texto(matriz, modo="fraccion"):
    """Devuelve la matriz con el formato de matriz aumentada."""
    filas_texto = []

    for fila in matriz:
        izquierda = []
        derecha = []

        for i, numero in enumerate(fila):
            texto = formatear(numero, modo)

            if i == len(fila) - 1:
                derecha.append(texto)
            else:
                izquierda.append(texto)

        izquierda_texto = "  ".join(f"{x:>8}" for x in izquierda)
        derecha_texto = f"{derecha[0]:>8}"

        filas_texto.append(f"[ {izquierda_texto} | {derecha_texto} ]")

    return "\n".join(filas_texto)


def gauss_jordan(matriz):
    """
    Resuelve una matriz aumentada por Gauss-Jordan.

    Devuelve:
        matriz_final
        pasos
        tipo
        pivotes
        variables_libres
    """

    # Convertimos todos los valores a fracciones exactas.
    A = [[Fraction(x) for x in fila] for fila in matriz]

    filas = len(A)
    columnas = len(A[0])
    variables = columnas - 1

    pasos = []
    fila_pivote = 0
    pivotes = []

    for columna in range(variables):

        if fila_pivote >= filas:
            break

        # Buscar un pivote distinto de cero.
        fila_intercambio = fila_pivote

        while (
            fila_intercambio < filas
            and A[fila_intercambio][columna] == 0
        ):
            fila_intercambio += 1

        if fila_intercambio == filas:
            continue

        # Intercambiar filas.
        if fila_intercambio != fila_pivote:
            A[fila_pivote], A[fila_intercambio] = (
                A[fila_intercambio],
                A[fila_pivote],
            )

            pasos.append((
                "intercambio",
                fila_pivote + 1,
                fila_intercambio + 1,
                [fila[:] for fila in A],
            ))

        # Convertir el pivote en 1.
        pivote = A[fila_pivote][columna]

        if pivote != 1:
            for j in range(columnas):
                A[fila_pivote][j] /= pivote

            pasos.append((
                "normalizar",
                fila_pivote + 1,
                pivote,
                [fila[:] for fila in A],
            ))

        pivotes.append(columna)

        # Hacer ceros arriba y abajo del pivote.
        for i in range(filas):

            if i == fila_pivote:
                continue

            factor = A[i][columna]

            if factor != 0:
                for j in range(columnas):
                    A[i][j] -= factor * A[fila_pivote][j]

                pasos.append((
                    "eliminar",
                    i + 1,
                    fila_pivote + 1,
                    factor,
                    [fila[:] for fila in A],
                ))

        fila_pivote += 1

    # Identificar contradicción: 0 0 ... 0 | número distinto de 0.
    for i in range(filas):
        coeficientes_cero = all(A[i][j] == 0 for j in range(variables))

        if coeficientes_cero and A[i][variables] != 0:
            tipo = "incompatible"
            variables_libres = []
            return A, pasos, tipo, pivotes, variables_libres

    # Identificar variables libres.
    variables_libres = [
        j for j in range(variables)
        if j not in pivotes
    ]

    if len(pivotes) == variables:
        tipo = "unica"
    else:
        tipo = "infinitas"

    return A, pasos, tipo, pivotes, variables_libres


def soluciones_texto(matriz, tipo, pivotes, variables_libres, modo="fraccion"):
    """Construye las soluciones para mostrar en CLI o GUI."""

    variables = len(matriz[0]) - 1

    if tipo == "incompatible":
        return "No tiene solución."

    if tipo == "unica":
        texto = []

        for i in range(variables):
            texto.append(
                f"x{i + 1} = {formatear(matriz[i][variables], modo)}"
            )

        return "\n".join(texto)

    # Caso de infinitas soluciones.
    texto = []
    nombres_libres = {}

    for contador, columna in enumerate(variables_libres):
        if contador == 0:
            nombres_libres[columna] = "t"
        else:
            nombres_libres[columna] = f"t{contador + 1}"

    for columna in variables_libres:
        texto.append(f"x{columna + 1} = {nombres_libres[columna]}")

    for columna in range(variables):
        if columna in variables_libres:
            continue

        fila_pivote = None

        for i in range(len(matriz)):
            if matriz[i][columna] == 1:
                # Verificar que sea el pivote de esa fila.
                es_pivote = True

                for j in range(columna):
                    if matriz[i][j] != 0:
                        es_pivote = False
                        break

                if es_pivote:
                    fila_pivote = i
                    break

        if fila_pivote is None:
            continue

        constante = matriz[fila_pivote][variables]
        expresion = f"x{columna + 1} = "

        if constante != 0:
            expresion += formatear(constante, modo)

        for libre in variables_libres:
            coeficiente = matriz[fila_pivote][libre]

            if coeficiente == 0:
                continue

            # xi + a*t = b  ->  xi = b - a*t
            coeficiente = -coeficiente

            if expresion != f"x{columna + 1} = ":
                if coeficiente > 0:
                    expresion += " + "
                else:
                    expresion += " - "
            elif coeficiente < 0:
                expresion += "-"

            valor = abs(coeficiente)

            if valor != 1:
                expresion += formatear(valor, modo)

            expresion += nombres_libres[libre]

        if expresion == f"x{columna + 1} = ":
            expresion += "0"

        texto.append(expresion)

    return "\n".join(texto)


def resolver(matriz, modo="fraccion"):
    """
    Función principal.

    Devuelve un diccionario listo para que CLI o GUI lo utilicen.
    """

    matriz_final, pasos, tipo, pivotes, variables_libres = gauss_jordan(matriz)

    resultado = {
        "matriz_inicial": matriz,
        "matriz_final": matriz_final,
        "tipo": tipo,
        "pivotes": pivotes,
        "variables_libres": variables_libres,
        "pasos": [],
        "soluciones": soluciones_texto(
            matriz_final,
            tipo,
            pivotes,
            variables_libres,
            modo,
        ),
    }

    for paso in pasos:
        operacion = paso[:-1]
        matriz_paso = paso[-1]

        resultado["pasos"].append({
            "operacion": formatear_operacion(operacion, modo),
            "matriz": matriz_paso,
        })

    return resultado

