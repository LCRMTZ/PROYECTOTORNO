import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración para alta resolución (Windows)
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# --- Datos de teoría ---
texto_teoria = """
Bienvenido a la sección de teoría para el uso del torno.

1. Antes de encender el torno, asegúrate de que el área esté limpia y sin objetos sueltos.
2. El refrigerante se utiliza para reducir la temperatura y evitar el desgaste prematuro de la herramienta.
3. La velocidad de corte debe ajustarse según el material y la herramienta para optimizar el acabado y la durabilidad.
4. La profundidad de corte afecta directamente el desgaste y el calor generado.
5. Usar refrigerante es fundamental en materiales duros y cortes profundos para prolongar la vida útil de la broca.

SEGURIDAD DE TORNO

6. Bloqueo de emergencia: Verifica siempre la ubicación del botón de parada de emergencia antes de operar.

7. Protección ocular: Usa gafas de seguridad incluso cuando el torno tenga protector transparente.

8. Cabello y ropa: Recoge el cabello largo y evita mangas holgadas que puedan engancharse.

9. Guantes prohibidos: Nunca uses guantes cerca de piezas giratorias (riesgo de atrapamiento).

SELECCION DE HERRAMIENTAS

#Material de la herramienta:

1. Carburo: Ideal para materiales duros (acero inoxidable, fundición).

2. Acero rápido (HSS): Bueno para aluminio y operaciones de acabado.

#GEOMETRIA DE LA CUCHILLA:

1. Ángulo de desprendimiento positivo para materiales blandos (aluminio).

2. Ángulo negativo para materiales duros (mayor resistencia).


Estudia estos conceptos antes de realizar el examen.
"""

# --- Preguntas para el examen ---
preguntas = [
    {
        "pregunta": "¿Qué debes hacer antes de encender el torno?",
        "opciones": [
            "Poner aceite en el motor",
            "Dejar la llave en el chuck",
            "Verificar que no haya objetos sueltos",
            "Ninguna de las anteriores"
        ],
        "respuesta": 2
    },
    {
        "pregunta": "¿Cuál es el propósito principal del refrigerante?",
        "opciones": [
            "Lubricar la pieza",
            "Reducir la temperatura y el desgaste",
            "Aumentar la velocidad del torno",
            "Ninguna de las anteriores"
        ],
        "respuesta": 1
    },
    {
        "pregunta": "¿Qué sucede si se usa una profundidad de corte muy alta sin refrigerante?",
        "opciones": [
            "Mejora el acabado",
            "Disminuye el desgaste",
            "Se aumenta el desgaste y el calor",
            "No afecta"
        ],
        "respuesta": 2
    },
    {
        "pregunta": "¿Cómo influye la velocidad de corte en el uso de refrigerante?",
        "opciones": [
            "A mayor velocidad, se requiere más refrigerante",
            "La velocidad no afecta el uso de refrigerante",
            "A mayor velocidad, se usa menos refrigerante",
            "Ninguna de las anteriores"
        ],
        "respuesta": 0
    },
    {
        "pregunta": "¿Por qué las piezas grandes necesitan más refrigerante?",
        "opciones": [
            "Porque generan menos calor",
            "Para cubrir un área mayor de trabajo y disipar el calor",
            "Porque el refrigerante lubrica más rápido",
            "No necesitan más refrigerante"
        ],
        "respuesta": 1
    },
    {
        "pregunta": "¿Qué tipo de material generalmente requiere menos refrigerante?",
        "opciones": [
            "Acero",
            "Plástico",
            "Hierro fundido",
            "Bronce"
        ],
        "respuesta": 1
    }
]

# --- Variables globales examen ---
indice_pregunta = 0
respuestas_correctas = 0
respuestas_totales = len(preguntas)
historial_ciclos_restantes = []

# --- Funciones --- 
def calcular_datos():
    try:
        rpm = int(entry_rpm.get())
        diametro = float(entry_diametro.get())
        longitud = float(entry_longitud.get())
        profundidad = float(entry_profundidad.get())
        material = combo_material.get()
        tipo_cuchilla = combo_cuchilla.get()
        usar_refrigerante = refrigerante_var.get()

        # Velocidad de corte en mm/min (circunferencia * rpm)
        velocidad_mm_min = rpm * math.pi * diametro  

        # Avance aproximado (mm/rev)
        avance_mm_por_rev = 0.2  
        avance_total = avance_mm_por_rev * rpm  # mm/min

        # Ajuste del tiempo de corte según refrigerante:
        # Si no hay refrigerante, el torno debe parar un 30% del tiempo para enfriar la cuchilla.
        factor_descanso = 1.0
        if not usar_refrigerante:
            factor_descanso = 1.3  # 30% más tiempo por paradas de enfriamiento
        tiempo_corte = (longitud / avance_total) * factor_descanso if avance_total > 0 else 0

        # Factores materiales para desgaste
        factor_material = {
            "Acero": 1.0,
            "Aluminio": 0.7,
            "Bronce": 0.85,
            "Hierro fundido": 1.1,
            "Plástico": 0.5
        }
        fm = factor_material.get(material, 1.0)

        # Factores cuchilla para desgaste
        factor_cuchilla = {
            "Carburo": 0.8,
            "Acero rápido (HSS)": 1.2
        }
        fc = factor_cuchilla.get(tipo_cuchilla, 1.0)

        # Factor refrigerante para desgaste
        # Con refrigerante el desgaste es menor (multiplicado por 0.6)
        # Sin refrigerante, mayor desgaste (multiplicado por 1.2)
        factor_refrigerante = 0.6 if usar_refrigerante else 1.2

        # Cálculo del desgaste total:
        desgaste = profundidad * fm * fc * factor_refrigerante * tiempo_corte * 2

        # Desgaste máximo y desgaste por ciclo (arbitrarios)
        desgaste_maximo = 200
        desgaste_por_ciclo = 10
        ciclos_restantes = max(0, int((desgaste_maximo - desgaste) / desgaste_por_ciclo))
        historial_ciclos_restantes.append(ciclos_restantes)

        # Estimación del uso de refrigerante
        flujo_base_material = {
            "Acero": 70,
            "Aluminio": 50,
            "Bronce": 60,
            "Hierro fundido": 40,
            "Plástico": 30
        }
        base = flujo_base_material.get(material, 60)
        ajuste_velocidad = 1 + (rpm / 1000)
        ajuste_profundidad = 1 + (profundidad / 2)
        area_contacto = (math.pi * diametro * longitud) / 100  # cm² aproximado
        ajuste_area = 1 + (area_contacto / 100)
        flujo_estimado = base * ajuste_velocidad * ajuste_profundidad * ajuste_area if usar_refrigerante else 0

        resultado = f"Tiempo estimado de corte: {tiempo_corte:.2f} minutos\n"
        resultado += f"Ciclos de uso restantes: {ciclos_restantes}\n"
        resultado += f"Desgaste calculado: {desgaste:.2f} unidades\n"
        if usar_refrigerante:
            resultado += f"Uso estimado de refrigerante: {flujo_estimado:.1f} ml/min"
        else:
            resultado += "No se está usando refrigerante.\n" \
                         "El tiempo de corte se ha incrementado para incluir pausas de enfriamiento,\n" \
                         "y el desgaste es mayor debido al calentamiento."

        text_resultado.config(state="normal")
        text_resultado.delete("1.0", tk.END)
        text_resultado.insert(tk.END, resultado)
        text_resultado.config(state="disabled")

        actualizar_grafica()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

def actualizar_grafica():
    ax.clear()
    ax.plot(range(1, len(historial_ciclos_restantes) + 1), historial_ciclos_restantes, marker='o', color='red')
    ax.set_title("Evolución de Ciclos Restantes")
    ax.set_xlabel("Cálculo #")
    ax.set_ylabel("Ciclos restantes")
    ax.grid(True)
    canvas.draw()

def mostrar_pregunta():
    global indice_pregunta
    if indice_pregunta < len(preguntas):
        p = preguntas[indice_pregunta]
        label_pregunta.config(text=p["pregunta"])
        for i, opcion in enumerate(p["opciones"]):
            radios[i].config(text=opcion, value=i, state="normal")
        respuesta_var.set(-1)
        label_retro.config(text="")
    else:
        label_pregunta.config(text=f"Examen finalizado.\nResultado: {respuestas_correctas} / {respuestas_totales} correctas.")
        for r in radios:
            r.config(state="disabled")
        boton_responder.config(state="disabled")
        boton_siguiente.config(state="disabled")

def responder_pregunta():
    global respuestas_correctas
    seleccion = respuesta_var.get()
    if seleccion == -1:
        messagebox.showwarning("Advertencia", "Debes seleccionar una opción antes de responder.")
        return

    p = preguntas[indice_pregunta]
    if seleccion == p["respuesta"]:
        label_retro.config(text="Correcto", foreground="green")
        respuestas_correctas += 1
    else:
        correcta = p["opciones"][p["respuesta"]]
        label_retro.config(text=f"Incorrecto. La respuesta correcta es: {correcta}", foreground="red")

    for r in radios:
        r.config(state="disabled")
    boton_responder.config(state="disabled")
    boton_siguiente.config(state="normal")

def siguiente_pregunta():
    global indice_pregunta
    indice_pregunta += 1
    mostrar_pregunta()
    boton_siguiente.config(state="disabled")

def reiniciar_examen():
    global indice_pregunta, respuestas_correctas
    indice_pregunta = 0
    respuestas_correctas = 0
    mostrar_pregunta()
    boton_reiniciar.config(state="disabled")
    boton_siguiente.config(state="disabled")
    boton_responder.config(state="disabled")
    label_retro.config(text="")
    for r in radios:
        r.config(state="normal")
    boton_reiniciar.config(state="normal")

def exportar_resultados():
    try:
        with open("resultados_examen.txt", "w", encoding="utf-8") as f:
            f.write(f"Resultado examen: {respuestas_correctas} / {respuestas_totales}\n")
        messagebox.showinfo("Exportar", "Resultados exportados a resultados_examen.txt")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar: {e}")

# --- GUI principal ---
root = tk.Tk()
root.title("Simulador TORSN - Uso de Torno")
root.geometry("800x700")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky="nsew")

# Pestaña Teoría
frame_teoria = ttk.Frame(notebook)
frame_teoria.grid(row=0, column=0, sticky="nsew")
notebook.add(frame_teoria, text="Teoría")

text_teoria_widget = tk.Text(frame_teoria, wrap="word", font=("Arial", 11))
text_teoria_widget.insert("1.0", texto_teoria)
text_teoria_widget.config(state="disabled")
text_teoria_widget.pack(expand=True, fill="both", padx=10, pady=10)

# Pestaña Simulación
frame_simulacion = ttk.Frame(notebook)
frame_simulacion.grid(row=0, column=0, sticky="nsew")
notebook.add(frame_simulacion, text="Simulación")

ttk.Label(frame_simulacion, text="Velocidad de giro (rpm):", font=("Arial", 12)).grid(column=0, row=0, sticky="e", padx=10, pady=5)
entry_rpm = ttk.Entry(frame_simulacion, font=("Arial", 12))
entry_rpm.grid(column=1, row=0, sticky="ew", padx=10, pady=5)
entry_rpm.insert(0, "600")

ttk.Label(frame_simulacion, text="Diámetro de la pieza (mm):", font=("Arial", 12)).grid(column=0, row=1, sticky="e", padx=10, pady=5)
entry_diametro = ttk.Entry(frame_simulacion, font=("Arial", 12))
entry_diametro.grid(column=1, row=1, sticky="ew", padx=10, pady=5)
entry_diametro.insert(0, "50")

ttk.Label(frame_simulacion, text="Longitud de la pieza (mm):", font=("Arial", 12)).grid(column=0, row=2, sticky="e", padx=10, pady=5)
entry_longitud = ttk.Entry(frame_simulacion, font=("Arial", 12))
entry_longitud.grid(column=1, row=2, sticky="ew", padx=10, pady=5)
entry_longitud.insert(0, "100")

ttk.Label(frame_simulacion, text="Profundidad de corte (mm):", font=("Arial", 12)).grid(column=0, row=3, sticky="e", padx=10, pady=5)
entry_profundidad = ttk.Entry(frame_simulacion, font=("Arial", 12))
entry_profundidad.grid(column=1, row=3, sticky="ew", padx=10, pady=5)
entry_profundidad.insert(0, "0.5")

ttk.Label(frame_simulacion, text="Material de la pieza:", font=("Arial", 12)).grid(column=0, row=4, sticky="e", padx=10, pady=5)
combo_material = ttk.Combobox(frame_simulacion, values=["Acero", "Aluminio", "Bronce", "Hierro fundido", "Plástico"], state="readonly", font=("Arial", 12))
combo_material.grid(column=1, row=4, sticky="ew", padx=10, pady=5)
combo_material.current(0)

ttk.Label(frame_simulacion, text="Tipo de cuchilla:", font=("Arial", 12)).grid(column=0, row=5, sticky="e", padx=10, pady=5)
combo_cuchilla = ttk.Combobox(frame_simulacion, values=["Carburo", "Acero rápido (HSS)"], state="readonly", font=("Arial", 12))
combo_cuchilla.grid(column=1, row=5, sticky="ew", padx=10, pady=5)
combo_cuchilla.current(0)

refrigerante_var = tk.BooleanVar()
ttk.Checkbutton(frame_simulacion, text="Usar refrigerante", variable=refrigerante_var).grid(column=0, row=6, columnspan=2, pady=10)

ttk.Button(frame_simulacion, text="Calcular", command=calcular_datos).grid(column=0, row=7, columnspan=2, pady=10)

text_resultado = tk.Text(frame_simulacion, height=6, font=("Arial", 12), state="disabled", background="#f0f0f0")
text_resultado.grid(column=0, row=8, columnspan=2, sticky="nsew", padx=10, pady=5)

frame_simulacion.columnconfigure(1, weight=1)
frame_simulacion.rowconfigure(8, weight=1)

fig, ax = plt.subplots(figsize=(6, 3))
canvas = FigureCanvasTkAgg(fig, master=frame_simulacion)
canvas.get_tk_widget().grid(column=0, row=9, columnspan=2, sticky="nsew", padx=10, pady=5)
frame_simulacion.rowconfigure(9, weight=1)

# Pestaña Examen
frame_examen = ttk.Frame(notebook)
frame_examen.grid(row=0, column=0, sticky="nsew")
notebook.add(frame_examen, text="Examen")

frame_examen.columnconfigure(0, weight=1)
for i in range(10):
    frame_examen.rowconfigure(i, weight=0)

label_pregunta = ttk.Label(frame_examen, text="", font=("Arial", 14), wraplength=650)
label_pregunta.grid(column=0, row=0, sticky="w", padx=20, pady=10)

respuesta_var = tk.IntVar(value=-1)
radios = []
for i in range(4):
    r = ttk.Radiobutton(frame_examen, text="", variable=respuesta_var, value=i, command=lambda: boton_responder.config(state="normal"))
    r.grid(column=0, row=i+1, sticky="w", padx=50, pady=2)
    radios.append(r)

label_retro = ttk.Label(frame_examen, text="", font=("Arial", 12))
label_retro.grid(column=0, row=5, sticky="w", padx=20, pady=5)

boton_responder = ttk.Button(frame_examen, text="Responder", command=responder_pregunta, state="disabled")
boton_responder.grid(column=0, row=6, sticky="w", padx=20, pady=5)

boton_siguiente = ttk.Button(frame_examen, text="Siguiente", command=siguiente_pregunta, state="disabled")
boton_siguiente.grid(column=0, row=7, sticky="w", padx=20, pady=5)

frame_botones_extra = ttk.Frame(frame_examen)
frame_botones_extra.grid(column=0, row=8, pady=10)

boton_reiniciar = ttk.Button(frame_botones_extra, text="Reiniciar Examen", command=reiniciar_examen)
boton_reiniciar.grid(row=0, column=0, padx=10)

boton_exportar = ttk.Button(frame_botones_extra, text="Exportar Resultados", command=exportar_resultados)
boton_exportar.grid(row=0, column=1, padx=10)

mostrar_pregunta()

root.mainloop()