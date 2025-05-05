import tkinter as tk
from tkinter import messagebox

# Funciones de cálculo (sin cambios)
def calcular_factor_material_broca(material):
    materiales = {
        "acero rapido": 1.0,
        "carburo": 1.5,
        "ceramico": 2.0,
        "diamante": 3.0
    }
    return materiales.get(material.lower(), 1.0)

def calcular_factor_metal_trabajado(metal):
    metales = {
        "aluminio": 1.0,
        "acero": 1.5,
        "hierro fundido": 1.3,
        "titanio": 2.0
    }
    return metales.get(metal.lower(), 1.0)

def calcular_factor_figura(figura):
    figuras = {
        "cilindro": 1.0,
        "cubo": 1.2,
        "rosca": 1.5,
        "cavidad": 1.8
    }
    return figuras.get(figura.lower(), 1.0)

def calcular_desgaste(velocidad_rpm, largo, ancho, avance, tipo_broca, tipo_metal, tipo_figura):
    factor_broca = calcular_factor_material_broca(tipo_broca)
    factor_metal = calcular_factor_metal_trabajado(tipo_metal)
    factor_figura = calcular_factor_figura(tipo_figura)

    volumen_broca = largo * ancho
    esfuerzo_total = velocidad_rpm * avance * volumen_broca

    # Ajuste realista del desgaste
    desgaste = (esfuerzo_total * factor_metal * factor_figura) / (factor_broca * 1e6)
    return desgaste

def calcular_ciclos_vida(desgaste):
    desgaste_maximo = 100
    ciclos = int(desgaste_maximo / desgaste) if desgaste > 0 else 0
    return ciclos

# Función para manejar la animación
def animar_torno(ciclos, velocidad_rpm):
    ciclo_maximo = ciclos
    avance_por_ciclo = 5  # mm por ciclo (simplificado para animación)

    # Tamaño del torno (área de trabajo)
    x_inicial = 150
    y_inicial = 150
    radio = 60

    # Crea la animación del torno (agregar más detalles visuales)
    for ciclo in range(ciclo_maximo):
        if ciclo > 0:
            # Movimiento de la broca hacia adelante por el avance
            canvas.move(broca, avance_por_ciclo, 0)
            canvas.after(500)  # Espera antes de mover

        # Movimiento de la broca (avanzando)
        canvas.coords(torno, x_inicial - radio, y_inicial - radio, x_inicial + radio, y_inicial + radio)

        # Mostrar el torno girando (se simula el movimiento de rotación)
        canvas.itemconfig(torno, outline='black', width=3)
        
        # Simulación de la broca: al principio es gris, y al final se rompe
        if ciclo == ciclo_maximo - 1:
            canvas.itemconfig(broca, fill='red')
            canvas.create_text(x_inicial, y_inicial - 80, text="¡Broca rota!", fill="red", font=("Arial", 12))

        ventana.update_idletasks()
        ventana.update()

# Función principal para el cálculo y animación
def calcular():
    try:
        # Obtener valores de los campos de entrada
        velocidad = float(entry_velocidad.get())
        largo = float(entry_largo.get())
        ancho = float(entry_ancho.get())
        avance = float(entry_avance.get())
        tipo_broca = entry_broca.get()
        tipo_metal = entry_metal.get()
        tipo_figura = entry_figura.get()
        tiempo_ciclo = float(entry_tiempo.get())

        # Calcular el desgaste y ciclos de vida
        desgaste = calcular_desgaste(velocidad, largo, ancho, avance, tipo_broca, tipo_metal, tipo_figura)
        ciclos = calcular_ciclos_vida(desgaste)
        tiempo_total_min = ciclos * tiempo_ciclo
        tiempo_total_hr = tiempo_total_min / 60

        # Mostrar los resultados en el GUI
        label_resultado.config(text=f"Desgaste estimado por ciclo: {desgaste:.4f}\n"
                                   f"Vida útil estimada: {ciclos} ciclos\n"
                                   f"Tiempo total estimado: {tiempo_total_min:.2f} minutos ({tiempo_total_hr:.2f} horas)")

        # Iniciar la animación del torno
        animar_torno(ciclos, velocidad)

    except ValueError:
        messagebox.showerror("Error de entrada", "Por favor, ingrese todos los valores correctamente.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Simulador de Torno con Animación Realista")

# Crear el lienzo para dibujar el torno
canvas = tk.Canvas(ventana, width=400, height=400, bg='white')
canvas.grid(row=0, column=2, rowspan=9)

# Dibujar el torno: Círculo grande para el plato
torno = canvas.create_oval(100, 100, 200, 200, outline='black', width=3)

# Dibujar la broca como un cilindro (rectángulo al principio)
broca = canvas.create_rectangle(180, 180, 190, 250, fill='gray')

# Dibujar detalles del torno: Eje, base, etc.
canvas.create_line(150, 150, 150, 250, width=3, fill='black')  # Eje del torno
canvas.create_oval(140, 250, 160, 270, fill='black')  # Base del torno

# Etiquetas de entrada (como antes)
label_velocidad = tk.Label(ventana, text="Velocidad de giro (RPM):")
label_velocidad.grid(row=0, column=0, sticky="e")

label_largo = tk.Label(ventana, text="Largo de la broca (mm):")
label_largo.grid(row=1, column=0, sticky="e")

label_ancho = tk.Label(ventana, text="Ancho de la broca (mm):")
label_ancho.grid(row=2, column=0, sticky="e")

label_avance = tk.Label(ventana, text="Avance del torno (mm/rev):")
label_avance.grid(row=3, column=0, sticky="e")

label_broca = tk.Label(ventana, text="Tipo de material de la broca:")
label_broca.grid(row=4, column=0, sticky="e")

label_metal = tk.Label(ventana, text="Tipo de metal trabajado:")
label_metal.grid(row=5, column=0, sticky="e")

label_figura = tk.Label(ventana, text="Tipo de figura:")
label_figura.grid(row=6, column=0, sticky="e")

label_tiempo = tk.Label(ventana, text="Duración de cada ciclo (minutos):")
label_tiempo.grid(row=7, column=0, sticky="e")

# Entradas de texto
entry_velocidad = tk.Entry(ventana)
entry_velocidad.grid(row=0, column=1)

entry_largo = tk.Entry(ventana)
entry_largo.grid(row=1, column=1)

entry_ancho = tk.Entry(ventana)
entry_ancho.grid(row=2, column=1)

entry_avance = tk.Entry(ventana)
entry_avance.grid(row=3, column=1)

entry_broca = tk.Entry(ventana)
entry_broca.grid(row=4, column=1)

entry_metal = tk.Entry(ventana)
entry_metal.grid(row=5, column=1)

entry_figura = tk.Entry(ventana)
entry_figura.grid(row=6, column=1)

entry_tiempo = tk.Entry(ventana)
entry_tiempo.grid(row=7, column=1)

# Botón para calcular
boton_calcular = tk.Button(ventana, text="Calcular", command=calcular)
boton_calcular.grid(row=8, column=0, columnspan=2)

# Etiqueta para mostrar resultados
label_resultado = tk.Label(ventana, text="Los resultados aparecerán aquí.", justify="left")
label_resultado.grid(row=9, column=0, columnspan=2)

# Ejecutar la ventana
ventana.mainloop()
