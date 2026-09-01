"""
gui.py
Interfaz gráfica para resolver sistemas con Gauss-Jordan.

La lógica matemática está en gauss_jordan.py.
"""

import tkinter as tk
from tkinter import messagebox

from gauss_jordan import resolver, matriz_texto


class GaussJordanGUI:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Método de Gauss-Jordan")
        self.ventana.geometry("900x720")
        self.ventana.resizable(False, False)

        self.entradas = []
        self.ultimo_resultado = None

        # -------------------------------
        # TÍTULO
        # -------------------------------

        tk.Label(
            ventana,
            text="Método de Gauss-Jordan",
            font=("Arial", 20, "bold")
        ).pack(pady=12)

        # -------------------------------
        # CONFIGURACIÓN
        # -------------------------------

        controles = tk.Frame(ventana)
        controles.pack(pady=5)

        tk.Label(
            controles,
            text="Ecuaciones:"
        ).grid(row=0, column=0, padx=5)

        self.entrada_ecuaciones = tk.Entry(
            controles,
            width=5,
            justify="center"
        )
        self.entrada_ecuaciones.grid(row=0, column=1, padx=5)
        self.entrada_ecuaciones.insert(0, "3")

        tk.Label(
            controles,
            text="Variables:"
        ).grid(row=0, column=2, padx=5)

        self.entrada_variables = tk.Entry(
            controles,
            width=5,
            justify="center"
        )
        self.entrada_variables.grid(row=0, column=3, padx=5)
        self.entrada_variables.insert(0, "3")

        tk.Button(
            controles,
            text="Crear matriz",
            command=self.crear_matriz,
            width=13
        ).grid(row=0, column=4, padx=8)

        tk.Button(
            controles,
            text="Limpiar",
            command=self.limpiar_matriz,
            width=13
        ).grid(row=0, column=5, padx=8)

        # -------------------------------
        # MATRIZ
        # -------------------------------

        self.marco_matriz = tk.Frame(ventana)
        self.marco_matriz.pack(pady=15)

        # -------------------------------
        # OPCIÓN DE FORMATO
        # -------------------------------

        formato = tk.Frame(ventana)
        formato.pack(pady=5)

        tk.Label(
            formato,
            text="Mostrar resultados en:"
        ).pack(side="left", padx=5)

        self.modo = tk.StringVar(value="fraccion")

        tk.Radiobutton(
            formato,
            text="Fracciones",
            variable=self.modo,
            value="fraccion"
        ).pack(side="left", padx=5)

        tk.Radiobutton(
            formato,
            text="Decimales",
            variable=self.modo,
            value="decimal"
        ).pack(side="left", padx=5)

        # -------------------------------
        # BOTONES
        # -------------------------------

        botones = tk.Frame(ventana)
        botones.pack(pady=10)

        tk.Button(
            botones,
            text="Resolver",
            command=self.resolver_sistema,
            width=18,
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            botones,
            text="Mostrar pasos",
            command=self.mostrar_pasos,
            width=18,
            font=("Arial", 11, "bold")
        ).grid(row=0, column=1, padx=8)

        # -------------------------------
        # ÁREA DE RESULTADO
        # -------------------------------

        self.salida = tk.Text(
            ventana,
            width=105,
            height=22,
            font=("Courier New", 10),
            state="disabled"
        )
        self.salida.pack(padx=15, pady=8)

        self.crear_matriz()

    # ==================================================
    # CREAR MATRIZ
    # ==================================================

    def crear_matriz(self):

        try:
            ecuaciones = int(self.entrada_ecuaciones.get())
            variables = int(self.entrada_variables.get())

            if ecuaciones < 1 or variables < 1:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Ingrese números enteros mayores que cero."
            )
            return

        # Borrar matriz anterior.
        for widget in self.marco_matriz.winfo_children():
            widget.destroy()

        self.entradas = []
        self.ultimo_resultado = None

        # Encabezados de variables.
        for j in range(variables):
            tk.Label(
                self.marco_matriz,
                text=f"x{j + 1}",
                font=("Arial", 10, "bold")
            ).grid(
                row=0,
                column=j,
                padx=5,
                pady=5
            )

        # Separador.
        tk.Label(
            self.marco_matriz,
            text="│",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=variables,
            padx=8
        )

        tk.Label(
            self.marco_matriz,
            text="b",
            font=("Arial", 10, "bold")
        ).grid(
            row=0,
            column=variables + 1,
            padx=5
        )

        # Campos.
        for i in range(ecuaciones):

            fila_entradas = []

            for j in range(variables):

                entrada = tk.Entry(
                    self.marco_matriz,
                    width=8,
                    justify="center"
                )

                entrada.grid(
                    row=i + 1,
                    column=j,
                    padx=5,
                    pady=4
                )

                fila_entradas.append(entrada)

            tk.Label(
                self.marco_matriz,
                text="│",
                font=("Arial", 12, "bold")
            ).grid(
                row=i + 1,
                column=variables,
                padx=8
            )

            entrada_resultado = tk.Entry(
                self.marco_matriz,
                width=8,
                justify="center"
            )

            entrada_resultado.grid(
                row=i + 1,
                column=variables + 1,
                padx=5,
                pady=4
            )

            fila_entradas.append(entrada_resultado)
            self.entradas.append(fila_entradas)

        self.limpiar_salida()

    # ==================================================
    # LIMPIAR MATRIZ
    # ==================================================

    def limpiar_matriz(self):

        for fila in self.entradas:
            for entrada in fila:
                entrada.delete(0, tk.END)

        self.ultimo_resultado = None
        self.limpiar_salida()

    # ==================================================
    # LEER MATRIZ
    # ==================================================

    def obtener_matriz(self):

        matriz = []

        for fila_entradas in self.entradas:

            fila = []

            for entrada in fila_entradas:

                texto = entrada.get().strip()

                if texto == "":
                    raise ValueError

                fila.append(float(texto))

            matriz.append(fila)

        return matriz

    # ==================================================
    # RESOLVER
    # ==================================================

    def resolver_sistema(self):

        try:
            matriz = self.obtener_matriz()

        except ValueError:
            messagebox.showerror(
                "Error",
                "Complete todos los campos de la matriz con números."
            )
            return

        self.ultimo_resultado = resolver(
            matriz,
            self.modo.get()
        )

        resultado = self.ultimo_resultado

        self.limpiar_salida()

        self.escribir(
            "========================================\n"
            "RESULTADO\n"
            "========================================\n"
        )

        if resultado["tipo"] == "unica":

            self.escribir(
                "Sistema compatible determinado.\n"
                "Tiene una única solución.\n\n"
            )

        elif resultado["tipo"] == "infinitas":

            self.escribir(
                "Sistema compatible indeterminado.\n"
                "Tiene infinitas soluciones.\n\n"
            )

        else:

            self.escribir(
                "Sistema incompatible o inconsistente.\n"
                "No tiene solución.\n\n"
            )

        self.escribir(resultado["soluciones"])

    # ==================================================
    # MOSTRAR PASOS
    # ==================================================

    def mostrar_pasos(self):

        if self.ultimo_resultado is None:

            try:
                matriz = self.obtener_matriz()

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Complete todos los campos de la matriz con números."
                )
                return

            self.ultimo_resultado = resolver(
                matriz,
                self.modo.get()
            )

        resultado = self.ultimo_resultado
        modo = self.modo.get()

        self.limpiar_salida()

        self.escribir(
            "========================================\n"
            "MATRIZ AUMENTADA INICIAL\n"
            "========================================\n\n"
        )

        self.escribir(
            matriz_texto(
                resultado["matriz_inicial"],
                modo
            )
        )

        self.escribir(
            "\n\n========================================\n"
            "PROCEDIMIENTO GAUSS-JORDAN\n"
            "========================================\n"
        )

        for paso in resultado["pasos"]:

            self.escribir(
                "\n" + paso["operacion"] + "\n\n"
            )

            self.escribir(
                matriz_texto(
                    paso["matriz"],
                    modo
                )
            )

        self.escribir(
            "\n\n========================================\n"
            "MATRIZ FINAL\n"
            "========================================\n\n"
        )

        self.escribir(
            matriz_texto(
                resultado["matriz_final"],
                modo
            )
        )

        self.escribir(
            "\n\n========================================\n"
            "RESULTADO\n"
            "========================================\n\n"
        )

        if resultado["tipo"] == "unica":

            self.escribir(
                "Sistema compatible determinado.\n"
                "Tiene una única solución.\n\n"
            )

        elif resultado["tipo"] == "infinitas":

            self.escribir(
                "Sistema compatible indeterminado.\n"
                "Tiene infinitas soluciones.\n\n"
            )

        else:

            self.escribir(
                "Sistema incompatible o inconsistente.\n"
                "No tiene solución.\n\n"
            )

        self.escribir(resultado["soluciones"])

    # ==================================================
    # FUNCIONES DE TEXTO
    # ==================================================

    def limpiar_salida(self):

        self.salida.config(state="normal")
        self.salida.delete("1.0", tk.END)
        self.salida.config(state="disabled")

    def escribir(self, texto):

        self.salida.config(state="normal")
        self.salida.insert(tk.END, texto)
        self.salida.config(state="disabled")


# ======================================================
# INICIAR PROGRAMA
# ======================================================

if __name__ == "__main__":
    ventana = tk.Tk()
    app = GaussJordanGUI(ventana)
    ventana.mainloop()

