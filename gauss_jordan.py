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


def comprobar_solucion(matriz_original, matriz_final, tipo, pivotes):
    """
    Comprueba la solución obtenida sin usar librerías externas.

    Guarda la matriz original (no la modifica), reconstruye el vector X,
    calcula A_original @ X y lo compara con B_original usando una
    tolerancia equivalente a np.allclose().

    Devuelve None si el sistema es incompatible.
    """

    if tipo == "incompatible":
        return None

    filas = len(matriz_original)
    variables = len(matriz_original[0]) - 1

    # Reconstruir X a partir de la matriz escalonada.
    X = [Fraction(0)] * variables

    for indice, columna in enumerate(pivotes):
        X[columna] = Fraction(matriz_final[indice][variables])

    tolerancia_absoluta = Fraction(1, 10 ** 9)
    tolerancia_relativa = Fraction(1, 10 ** 9)

    comparaciones = []
    correcto = True

    for i in range(filas):

        ax_i = sum(
            Fraction(matriz_original[i][j]) * X[j]
            for j in range(variables)
        )
        b_i = Fraction(matriz_original[i][variables])

        diferencia = abs(ax_i - b_i)
        limite = tolerancia_absoluta + tolerancia_relativa * abs(b_i)

        if diferencia > limite:
            correcto = False

        comparaciones.append((ax_i, b_i))

    return {
        "correcto": correcto,
        "X": X,
        "comparaciones": comparaciones,
        "matriz_original": matriz_original,
        "tipo": tipo,
    }


def texto_comprobacion(comprobacion, modo="fraccion"):
    """
    Convierte el resultado de la comprobación en texto legible,
    dibujando la multiplicación A_original @ X = B_original.
    """

    if comprobacion is None:
        return (
            "No es posible comprobar: "
            "el sistema no tiene solución.\n"
        )

    original = comprobacion["matriz_original"]
    filas = len(original)
    variables = len(original[0]) - 1

    A = [[formatear(original[i][j], modo) for j in range(variables)]
         for i in range(filas)]
    B = [formatear(original[i][variables], modo) for i in range(filas)]
    X = [formatear(x, modo) for x in comprobacion["X"]]

    ancho_a = max(len(t) for fila in A for t in fila) + 2
    ancho_x = max(len(t) for t in X) + 2
    ancho_b = max(len(t) for t in B) + 2

    def bloque_superior(ancho):
        return "┌" + "─" * ancho + "┐"

    def bloque_inferior(ancho):
        return "└" + "─" * ancho + "┘"

    def fila_cerrada(textos, ancho):
        celdas = [t.center(ancho) for t in textos]
        return "│" + "│".join(celdas) + "│"

    ancho_a_total = ancho_a * variables + (variables - 1)

    bloque_a = [bloque_superior(ancho_a_total)]
    bloque_a += [fila_cerrada(fila, ancho_a) for fila in A]
    bloque_a.append(bloque_inferior(ancho_a_total))

    bloque_x = [bloque_superior(ancho_x)]
    bloque_x += [fila_cerrada([t], ancho_x) for t in X]
    bloque_x.append(bloque_inferior(ancho_x))

    bloque_b = [bloque_superior(ancho_b)]
    bloque_b += [fila_cerrada([t], ancho_b) for t in B]
    bloque_b.append(bloque_inferior(ancho_b))

    altura = max(len(bloque_a), len(bloque_x), len(bloque_b))

    def centrar_vertical(bloque, alto):
        falta = alto - len(bloque)
        arriba = falta // 2
        return [""] * arriba + bloque + [""] * (falta - arriba)

    bloque_a = centrar_vertical(bloque_a, altura)
    bloque_x = centrar_vertical(bloque_x, altura)
    bloque_b = centrar_vertical(bloque_b, altura)

    medio = altura // 2
    lineas = []

    for i in range(altura):
        s1 = "·" if i == medio else " "
        s2 = "=" if i == medio else " "
        lineas.append(
            f"{bloque_a[i]} {s1} {bloque_x[i]} {s2} {bloque_b[i]}"
        )

    wa = len(bloque_a[0])
    wx = len(bloque_x[0])
    wb = len(bloque_b[0])

    etiquetas = (
        "A_original".center(wa)
        + " " * 3
        + "X".center(wx)
        + " " * 3
        + "B_original".center(wb)
    )

    lineas.append(etiquetas)
    lineas.append("")

    if comprobacion["tipo"] == "infinitas":
        lineas.append(
            "(variables libres tomadas como 0: solución particular)"
        )

    if comprobacion["correcto"]:
        lineas.append(
            "✓ COMPROBACIÓN CORRECTA: "
            "A_original @ X = B_original."
        )
    else:
        residuales = [
            str(abs(ax_i - b_i))
            for ax_i, b_i in comprobacion["comparaciones"]
        ]
        lineas.append(
            "✗ COMPROBACIÓN INCORRECTA: "
            "A_original @ X ≠ B_original."
        )
        lineas.append(
            "|A_original @ X - B_original| = "
            + "[" + ", ".join(residuales) + "]."
        )

    return "\n".join(lineas) + "\n"


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
        "comprobacion": comprobar_solucion(
            matriz,
            matriz_final,
            tipo,
            pivotes,
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

