"""
cli.py
Versión de consola del programa de Gauss-Jordan.
"""

from gauss_jordan import resolver, matriz_texto, formatear, texto_comprobacion


def pedir_matriz():
    print("========================================")
    print("       MÉTODO DE GAUSS-JORDAN")
    print("========================================")

    ecuaciones = int(input("Número de ecuaciones: "))
    variables = int(input("Número de variables: "))

    matriz = []

    print("\nIngrese los coeficientes de cada ecuación.")
    print("Después ingrese el término independiente.\n")

    for i in range(ecuaciones):

        print(f"Ecuación {i + 1}")
        fila = []

        for j in range(variables):
            valor = float(
                input(f"Coeficiente de x{j + 1}: ")
            )
            fila.append(valor)

        termino = float(input("Término independiente: "))
        fila.append(termino)

        matriz.append(fila)

    return matriz


def main():

    matriz = pedir_matriz()

    print("\n¿Cómo desea mostrar los resultados?")
    print("1. Fracciones")
    print("2. Decimales")

    opcion = input("Seleccione una opción: ")

    while opcion not in ("1", "2"):
        print("Opción no válida.")
        opcion = input("Seleccione 1 o 2: ")

    modo = "fraccion" if opcion == "1" else "decimal"

    resultado = resolver(matriz, modo)

    print("\n========================================")
    print("MATRIZ AUMENTADA INICIAL")
    print("========================================\n")

    print(matriz_texto(resultado["matriz_inicial"], modo))

    print("\n========================================")
    print("PROCEDIMIENTO")
    print("========================================")

    for paso in resultado["pasos"]:
        print("\n" + paso["operacion"])
        print(matriz_texto(paso["matriz"], modo))

    print("\n========================================")
    print("MATRIZ FINAL")
    print("========================================\n")

    print(matriz_texto(resultado["matriz_final"], modo))

    print("\n========================================")
    print("RESULTADO")
    print("========================================")

    if resultado["tipo"] == "unica":
        print("Sistema compatible determinado.")
        print("Tiene una única solución.")

    elif resultado["tipo"] == "infinitas":
        print("Sistema compatible indeterminado.")
        print("Tiene infinitas soluciones.")

    else:
        print("Sistema incompatible o inconsistente.")
        print("No tiene solución.")

    print("\n" + resultado["soluciones"])

    comprobar = input("\n¿Desea comprobar el resultado? (s/n): ")

    while comprobar.lower() not in ("s", "n", "si", "no"):
        comprobar = input("Seleccione s o n: ")

    if comprobar.lower() in ("s", "si"):

        print("\n========================================")
        print("COMPROBACIÓN (A_original @ X vs B_original)")
        print("========================================")

        print(texto_comprobacion(resultado["comprobacion"], modo))


if __name__ == "__main__":
    main()

