import tkinter as tk
from tkinter import messagebox

class TORSNCostos:
    def __init__(self, root):  # CORREGIDO
        self.root = root
        self.root.title("TORSN - Simulador de Costos de Corte")
        self.root.geometry("450x350")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Desgaste cuchilla (%)").grid(row=0, column=0, sticky="w")
        self.entry_desgaste = tk.Entry(self.root)
        self.entry_desgaste.grid(row=0, column=1)

        tk.Label(self.root, text="Tipo de cuchilla (carburo/acero)").grid(row=1, column=0, sticky="w")
        self.entry_tipo_cuchilla = tk.Entry(self.root)
        self.entry_tipo_cuchilla.grid(row=1, column=1)

        tk.Label(self.root, text="Refrigerante usado (ml)").grid(row=2, column=0, sticky="w")
        self.entry_refrigerante = tk.Entry(self.root)
        self.entry_refrigerante.grid(row=2, column=1)

        tk.Label(self.root, text="Tiempo de corte (horas)").grid(row=3, column=0, sticky="w")
        self.entry_tiempo = tk.Entry(self.root)
        self.entry_tiempo.grid(row=3, column=1)

        self.btn_calcular = tk.Button(self.root, text="Calcular costo", command=self.calcular_costo)
        self.btn_calcular.grid(row=4, column=0, columnspan=2, pady=10)

        self.lbl_resultado = tk.Label(self.root, text="", fg="blue")
        self.lbl_resultado.grid(row=5, column=0, columnspan=2)

    def calcular_costo(self):
        try:
            desgaste_pct = float(self.entry_desgaste.get()) / 100
            tipo_cuchilla = self.entry_tipo_cuchilla.get().strip().lower()
            refrigerante_ml = float(self.entry_refrigerante.get())
            tiempo_horas = float(self.entry_tiempo.get())

            if tipo_cuchilla not in ['carburo', 'acero']:
                messagebox.showerror("Error", "Tipo de cuchilla debe ser 'carburo' o 'acero'")
                return

            precio = self.calcular_precio_corte(desgaste_pct, tipo_cuchilla, refrigerante_ml, tiempo_horas)
            self.lbl_resultado.config(text=f"Precio estimado del corte: ${precio:.2f} pesos")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos")

    def calcular_precio_corte(self, desgaste_porcentaje, tipo_cuchilla, refrigerante_ml, tiempo_corte_horas):
        precio_refrigerante_por_litro = 250
        precio_cuchilla_carburo = 200
        precio_cuchilla_acero = 150
        costo_mano_obra_por_hora = 120

        precio_cuchilla = precio_cuchilla_carburo if tipo_cuchilla == 'carburo' else precio_cuchilla_acero

        costo_desgaste_cuchilla = desgaste_porcentaje * precio_cuchilla
        litros_refrigerante = refrigerante_ml / 1000.0
        costo_refrigerante = litros_refrigerante * precio_refrigerante_por_litro
        costo_mano_obra = costo_mano_obra_por_hora * tiempo_corte_horas

        suma_parcial = costo_desgaste_cuchilla + costo_refrigerante + costo_mano_obra
        precio_estimado = suma_parcial * 4
        precio_final = precio_estimado * 1.16  # IVA 16%

        return precio_final

# CORREGIDO
if __name__ == "__main__":
    root = tk.Tk()
    app = TORSNCostos(root)
    root.mainloop()
