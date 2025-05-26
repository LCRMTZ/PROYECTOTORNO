import tkinter as tk
import subprocess
import sys
import os

def ejecutar_simulador():
    script_path = os.path.join(os.path.dirname(__file__), "SimuladorFatiga.py")
    subprocess.Popen([sys.executable, script_path])

def ejecutar_capacitacion():
    script_path = os.path.join(os.path.dirname(__file__), "torsnCapacitacion.py")
    subprocess.Popen([sys.executable, script_path])

def ejecutar_costos():
    script_path = os.path.join(os.path.dirname(__file__), "torsnCostos.py")
    subprocess.Popen([sys.executable, script_path])

def main():
    root = tk.Tk()
    root.title("Menú Principal - TORSN")
    root.geometry("350x200")

    label = tk.Label(root, text="Seleccione un módulo para iniciar:", font=("Arial", 12))
    label.pack(pady=20)

    btn_simulador = tk.Button(root, text="TORSN Simulador", width=25, height=2, command=ejecutar_simulador)
    btn_simulador.pack(pady=10)

    btn_capacitacion = tk.Button(root, text="TORSN Capacitación", width=25, height=2, command=ejecutar_capacitacion)
    btn_capacitacion.pack(pady=5)

    btn_capacitacion = tk.Button(root, text="TORSN Costos", width=25, height=2, command=ejecutar_costos)
    btn_capacitacion.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
