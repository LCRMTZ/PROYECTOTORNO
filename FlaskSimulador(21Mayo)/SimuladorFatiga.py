import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from scipy.stats import kstest, expon
from scipy.stats import weibull_min
from tkinter import ttk
from tkinter import simpledialog

import os
import json
import tkinter.simpledialog

PERFILES_PATH = "perfiles.json"
perfil_actual = {"nombre": None, "datos": {}}
etiqueta_perfil_actual = None

def guardar_perfil(nombre, datos):
    perfiles = {}
    if os.path.exists(PERFILES_PATH):
        with open(PERFILES_PATH, "r") as f:
            perfiles = json.load(f)

    for otro_nombre, otros_datos in perfiles.items():
        if otros_datos == datos:
            messagebox.showerror("Duplicado", f"Ya existe un perfil con los mismos datos: '{otro_nombre}'")
            return

    perfiles[nombre] = datos
    with open(PERFILES_PATH, "w") as f:
        json.dump(perfiles, f, indent=4)


def cargar_perfiles_disponibles():
    if os.path.exists(PERFILES_PATH):
        with open(PERFILES_PATH, "r") as f:
            return json.load(f)
    return {}


import tkinter.simpledialog

#Función para guardar valores de las entradas en algún perfil seleccionado NO SE PUEDEN DUPLICAR
def guardar_valor_en_perfil(clave, valor):
    global perfil_actual

    if not valor.strip():
        messagebox.showwarning("Valor vacío", "Debes ingresar un valor antes de guardarlo.")
        return

    if perfil_actual["nombre"] is None:
        nombre = simpledialog.askstring("Nuevo perfil", "Ingresa el nombre del perfil para guardar:")
        if not nombre:
            return
        perfil_actual["nombre"] = nombre
        perfil_actual["datos"] = {}

    # Cargar perfiles existentes
    perfiles = cargar_perfiles_disponibles()

    # Si el perfil ya existe, cargar sus datos completos
    if perfil_actual["nombre"] in perfiles:
        perfil_actual["datos"] = perfiles[perfil_actual["nombre"]]

    # Si el campo ya está y es idéntico, no hacer nada
    if clave in perfil_actual["datos"] and perfil_actual["datos"][clave] == valor:
        messagebox.showinfo("Sin cambios", f"El campo '{clave}' ya contiene ese valor.")
        return

    # Actualizar el valor y guardar
    perfil_actual["datos"][clave] = valor
    guardar_perfil(perfil_actual["nombre"], perfil_actual["datos"])
    messagebox.showinfo("Actualizado", f"'{clave}' actualizado en el perfil '{perfil_actual['nombre']}'.")




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

#Calcula el DESGASTE estimado por CICLO usando los factores y condiciones de corte.
def calcular_desgaste(velocidad_rpm, largo, ancho, avance, tipo_broca, tipo_metal, tipo_figura):
    factor_broca = calcular_factor_material_broca(tipo_broca)
    factor_metal = calcular_factor_metal_trabajado(tipo_metal)
    factor_figura = calcular_factor_figura(tipo_figura)

    volumen_broca = largo * ancho
    esfuerzo_total = velocidad_rpm * avance * volumen_broca

    # Ajuste realista del desgaste por ciclo
    desgaste = (esfuerzo_total * factor_metal * factor_figura) / (factor_broca * 1e6)
    return desgaste

#Calcula los CICLOS de VIDA útiles antes de que la broca se desgaste por completo.
def calcular_ciclos_vida(desgaste):
    desgaste_maximo = 100
    ciclos = int(desgaste_maximo / desgaste) if desgaste > 0 else 0
    return ciclos

# Función para manejar la animación
def animar_torno(ciclos, velocidad_rpm, largo, ancho):
    canvas.delete("all")  # Borra todo del canvas

    ciclo_maximo = min(ciclos, 30)  # Máximo 30 ciclos visibles
    avance_por_ciclo = 6

    x_inicial = 60
    y_inicial = 150
    radio = 50

    # Tamaño de la broca basado en valores reales
    largo_px = int(largo / 5)
    ancho_px = int(ancho / 3)
    largo_px = max(20, min(largo_px, 100))
    ancho_px = max(5, min(ancho_px, 30))

    # Dibujar el torno (pieza circular)
    torno = canvas.create_oval(220, y_inicial - radio, 220 + 2*radio, y_inicial + radio, outline='black', width=3)
    canvas.create_line(220 + radio, y_inicial, 220 + radio, y_inicial + 80, fill='black', width=3)  # eje base
    canvas.create_oval(220 + radio - 10, y_inicial + 80, 220 + radio + 10, y_inicial + 100, fill='black')

    # Crear la broca inicial
    broca_x = x_inicial
    broca = canvas.create_rectangle(broca_x, y_inicial - ancho_px//2,
                                    broca_x + largo_px, y_inicial + ancho_px//2, fill='gray')

    # Animación
    for ciclo in range(ciclo_maximo):
        # Cambiar grosor del torno (simula rotación)
        canvas.itemconfig(torno, width=2 + (ciclo % 3))

        # Color dinámico
        factor_color = ciclo / ciclo_maximo
        if factor_color < 0.4:
            color = 'gray'
        elif factor_color < 0.8:
            color = 'orange'
        else:
            color = 'red'
        canvas.itemconfig(broca, fill=color)

        # Mover broca a la derecha
        canvas.move(broca, avance_por_ciclo, 0)

        ventana.update_idletasks()
        ventana.update()
        canvas.after(300)

    # Mensaje al romperse
    canvas.create_text(200, y_inicial - 80, text="¡Broca rota!", fill="red", font=("Arial", 12, "bold"))



#RUIDO GAUSSIANO; Función agregada para simular varias veces el proceso con pequeñas variaciones aleatorias.
import numpy as np

def simular_una_vez(velocidad, largo, ancho, avance, tipo_broca, tipo_metal, tipo_figura):
    # Variación aleatoria controlada (5% ruido gaussiano)
    velocidad_real = np.random.normal(velocidad, 0.05 * velocidad)
    largo_real = np.random.normal(largo, 0.03 * largo)
    ancho_real = np.random.normal(ancho, 0.03 * ancho)
    avance_real = np.random.normal(avance, 0.1 * avance)

    desgaste = calcular_desgaste(velocidad_real, largo_real, ancho_real, avance_real, tipo_broca, tipo_metal, tipo_figura)
    ciclos = calcular_ciclos_vida(desgaste)
    return ciclos

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
        btn_guardar_velocidad = tk.Button(ventana, text="💾", command=lambda: guardar_valor_en_perfil("velocidad", entry_velocidad.get()))
        btn_guardar_velocidad.grid(row=0, column=1, sticky="e", padx=(5, 0))

        btn_guardar_largo = tk.Button(ventana, text="💾", command=lambda: guardar_valor_en_perfil("largo", entry_largo.get()))
        btn_guardar_largo.grid(row=1, column=1, sticky="e", padx=(5, 0))

        btn_guardar_ancho = tk.Button(ventana, text="💾", command=lambda: guardar_valor_en_perfil("ancho", entry_ancho.get()))
        btn_guardar_ancho.grid(row=2, column=1, sticky="e", padx=(5, 0))

        btn_guardar_avance = tk.Button(ventana, text="💾", command=lambda: guardar_valor_en_perfil("avance", entry_avance.get()))
        btn_guardar_avance.grid(row=3, column=1, sticky="e", padx=(5, 0))

        btn_guardar_broca = tk.Button(ventana, text="💾", command=lambda: guardar_valor_en_perfil("tipo_broca", entry_broca.get()))
        btn_guardar_broca.grid(row=4, column=1, sticky="e", padx=(5, 0))

        btn_guardar_metal = tk.Button(ventana, text="💾", command=lambda: guardar_valor_en_perfil("tipo_metal", entry_metal.get()))
        btn_guardar_metal.grid(row=5, column=1, sticky="e", padx=(5, 0))

        btn_guardar_figura = tk.Button(ventana, text="💾", command=lambda: guardar_valor_en_perfil("tipo_figura", entry_figura.get()))
        btn_guardar_figura.grid(row=6, column=1, sticky="e", padx=(5, 0))

        btn_guardar_tiempo = tk.Button(ventana, text="💾", command=lambda: guardar_valor_en_perfil("tiempo_ciclo", entry_tiempo.get()))
        btn_guardar_tiempo.grid(row=7, column=1, sticky="e", padx=(5, 0))


        #NO DEJAR NÚMEROS NEGATIVOS PARA EL TIEMPO DE CADA CICLO
        if tiempo_ciclo<=0:
            messagebox.showerror("Valor inválido", "La duración de cada ciclo debe ser un número positivo.")
            return

        # Calcular el desgaste y ciclos de vida
        desgaste = calcular_desgaste(velocidad, largo, ancho, avance, tipo_broca, tipo_metal, tipo_figura)
        ciclos = calcular_ciclos_vida(desgaste)
        tiempo_total_min = ciclos * tiempo_ciclo
        tiempo_total_hr = tiempo_total_min / 60
        tiempo_corte_seg = largo / (avance * velocidad)

        # Simulaciones múltiples con variabilidad
        n_simulaciones = 100
        global resultados_ciclos
        resultados_ciclos = [simular_una_vez(velocidad, largo, ancho, avance, tipo_broca, tipo_metal, tipo_figura)
                            for _ in range(n_simulaciones)]

        media_ciclos = np.mean(resultados_ciclos)
        desviacion = np.std(resultados_ciclos)
        
        # Histograma de los resultados
        plt.figure(figsize=(8,5))
        plt.hist(resultados_ciclos, bins=10, color='skyblue', edgecolor='black', density=True, label="Datos simulados")

        # Distribución teórica (por ejemplo, exponencial con misma media)
        loc, scale = expon.fit(resultados_ciclos)
        x = np.linspace(0, max(resultados_ciclos), 100)
        y = expon.pdf(x, loc=loc, scale=scale)
        plt.plot(x, y, 'r-', lw=2, label='Distribución Exponencial teórica')
        
        # Ajuste y graficado de Weibull
        shape, loc_w, scale_w = weibull_min.fit(resultados_ciclos, floc=0)
        y_weibull = weibull_min.pdf(x, shape, loc_w, scale_w)
        plt.plot(x, y_weibull, 'g--', lw=2, label='Distribución Weibull')

        # Prueba de Kolmogorov–Smirnov
        ks_stat, p_value = kstest(resultados_ciclos, 'expon', args=(loc, scale))

        print(f"\nEstadístico de prueba KS: {ks_stat:.4f}")
        print(f"Valor p: {p_value:.6f}")

        # Asignar texto a la variable (para GUI)
        if p_value > 0.05:
            resultado_ks = "✅ No se rechaza la hipótesis nula: los datos podrían provenir de una distribución exponencial."
        else:
            resultado_ks = "❌ Se rechaza la hipótesis nula: los datos NO provienen de una distribución exponencial."

        # Mostrar también en consola
        print(resultado_ks)

        # Mostrar resumen de los RESULTADOS en GUI
        # Diccionario con los datos a mostrar
        datos_resultado = {
            "Desgaste estimado por ciclo": f"{desgaste:.4f}",
            "Promedio de vida útil": f"{media_ciclos:.1f} ciclos",
            "Desviación estándar": f"{desviacion:.1f} ciclos",
            "Simulación base (sin ruido)": f"{ciclos} ciclos",
            "Tiempo de corte real estimado": f"{tiempo_corte_seg:.2f} segundos",
            "Tiempo total estimado": f"{tiempo_total_min:.2f} min ({tiempo_total_hr:.2f} h)",
            "Estadístico de prueba KS": f"{ks_stat:.4f}",
            "Valor p": f"{p_value:.6f}",
            "Resultado KS": resultado_ks
        }
        mostrar_resultados(datos_resultado)

        plt.title("Distribución de Ciclos de Vida Simulados vs Teoría")
        plt.xlabel("Ciclos de vida")
        plt.ylabel("Probabilidad estimada")
        plt.legend()
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(0.1)

        # Iniciar la animación del torno
        animar_torno(ciclos, velocidad, largo, ancho)

    except ValueError:
        messagebox.showerror("Error de entrada", "Por favor asegurese de que se ingresaron números positivos sin signos e ingrese todos los valores correctamente.")
   

#### FUNCIÓN PARA EXPORTAR LOS RESULTADOS A UN ARCHIVO CSV
import csv

def exportar_csv():
    with open("resultados_simulacion.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Simulación", "Ciclos"])
        for i, ciclos in enumerate(resultados_ciclos, 1):
            writer.writerow([i, ciclos])
    messagebox.showinfo("Exportado", "Resultados exportados a 'resultados_simulacion.csv'")

def mostrar_explicacion(titulo, texto):
    ventana_info = tk.Toplevel(ventana)
    ventana_info.title(titulo)
    ventana_info.geometry("400x250")
    ventana_info.configure(bg="white")

    etiqueta = tk.Label(ventana_info, text=texto, wraplength=380, justify="left", bg="white")
    etiqueta.pack(pady=20, padx=20)

    boton_cerrar = tk.Button(ventana_info, text="Cerrar", command=ventana_info.destroy, bg="#267c9c", fg="white")
    boton_cerrar.pack(pady=10)

def mostrar_resultados(datos):
    # Si ya existe el frame, lo destruimos para limpiarlo
    global frame_resultados
    try:
        frame_resultados.destroy()
    except:
        pass

    # Creamos uno nuevo
    frame_resultados = tk.Frame(ventana, bg="white")
    frame_resultados.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=5)

    # Diccionario de explicaciones
    explicaciones = {
        "Desgaste estimado por ciclo": "El desgaste por ciclo es una estimación del daño acumulado que sufre la broca en cada giro del torno, considerando material y condiciones de corte.",
        "Promedio de vida útil": "Es el número de ciclos aproximados que resistirá la broca antes de romperse o quedar inservible.",
        "Desviación estándar": "Mide cuánto varían los ciclos simulados respecto al promedio. Alta desviación implica variabilidad elevada.",
        "Simulación base (sin ruido)": "Es la estimación de ciclos sin considerar variaciones aleatorias (ruido), usando valores exactos ingresados.",
        "Tiempo de corte real estimado": "Tiempo que tarda la broca en completar un solo corte según dimensiones y avance.",
        "Tiempo total estimado": "Suma de todos los ciclos multiplicado por la duración de cada uno.",
        "Estadístico de prueba KS": "El valor estadístico KS mide la diferencia máxima entre la distribución simulada y una teórica. Un valor bajo indica buen ajuste.",
        "Valor p": "El valor p indica la probabilidad de que los datos simulados provengan de la distribución teórica. Si es mayor a 0.05, el ajuste es adecuado.",
        "Resultado KS": "Interpretación de la prueba de Kolmogorov–Smirnov."
    }

    # Agregamos cada resultado y su botón ℹ️
    for i, (clave, valor) in enumerate(datos.items()):
        label = tk.Label(frame_resultados, text=f"{clave}: {valor}", anchor="w", bg="white", font=("Segoe UI", 9))
        label.grid(row=i, column=0, sticky="w", padx=(5,15), pady=1)

        if clave in explicaciones:
            boton = tk.Button(frame_resultados, text="ℹ️", width=2, command=lambda t=clave: mostrar_explicacion(t, explicaciones[t]))
            boton.grid(row=i, column=1, padx=(0,10), pady=(2,5), sticky="w")



# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Simulador de Torno con Animación Realista")

#Se crea un texto mostrandonos en que perfil estamos (si estamos en alguno)
etiqueta_perfil_actual = tk.Label(ventana, text="🔒 Perfil actual: Ninguno", font=("Segoe UI", 9, "bold"), fg="gray")
etiqueta_perfil_actual.grid(row=0, column=4, padx=10, pady=5, sticky="ne")

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

materiales_broca = ["acero rapido", "carburo", "ceramico", "diamante"]
entry_broca = ttk.Combobox(ventana, values=materiales_broca)
entry_broca.grid(row=4, column=1)

metales_trabajados = ["aluminio", "acero", "hierro fundido", "titanio"]
entry_metal = ttk.Combobox(ventana, values=metales_trabajados)
entry_metal.grid(row=5, column=1)

figuras_trabajo = ["cilindro", "cubo", "rosca", "cavidad"]
entry_figura = ttk.Combobox(ventana, values=figuras_trabajo)
entry_figura.grid(row=6, column=1)

entry_tiempo = tk.Entry(ventana)
entry_tiempo.grid(row=7, column=1)

#Función para eliminar un perfil desde la interfaz del programa
def eliminar_perfil():
    perfiles = cargar_perfiles_disponibles()
    if not perfiles:
        messagebox.showinfo("Sin perfiles", "No hay perfiles guardados.")
        return

    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar perfil")
    ventana_eliminar.geometry("300x200")

    tk.Label(ventana_eliminar, text="Selecciona un perfil para eliminar:").pack(pady=10)
    perfil_a_eliminar = tk.StringVar()
    combo = ttk.Combobox(ventana_eliminar, textvariable=perfil_a_eliminar, values=list(perfiles.keys()), state="readonly")
    combo.pack(pady=5)

    def confirmar_eliminacion():
        nombre = perfil_a_eliminar.get()
        if nombre:
            confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar el perfil '{nombre}'?")
            if confirmacion:
                del perfiles[nombre]
                with open(PERFILES_PATH, "w") as f:
                    json.dump(perfiles, f, indent=4)
                messagebox.showinfo("Eliminado", f"Perfil '{nombre}' eliminado.")
                ventana_eliminar.destroy()

    tk.Button(ventana_eliminar, text="Eliminar perfil", command=confirmar_eliminacion, bg="red", fg="white").pack(pady=10)


# ---- CARGAR PERFIL (si existe) ----
def cargar_datos_perfil(perfil):
    entry_velocidad.delete(0, tk.END)
    entry_largo.delete(0, tk.END)
    entry_ancho.delete(0, tk.END)
    entry_avance.delete(0, tk.END)
    entry_tiempo.delete(0, tk.END)

    if "velocidad" in perfil: entry_velocidad.insert(0, perfil["velocidad"])
    if "largo" in perfil: entry_largo.insert(0, perfil["largo"])
    if "ancho" in perfil: entry_ancho.insert(0, perfil["ancho"])
    if "tipo_broca" in perfil: entry_broca.set(perfil["tipo_broca"])
    if "tipo_metal" in perfil: entry_metal.set(perfil["tipo_metal"])
    if "tipo_figura" in perfil: entry_figura.set(perfil["tipo_figura"])
    if "avance" in perfil: entry_avance.insert(0, perfil["avance"])
    if "tiempo_ciclo" in perfil: entry_tiempo.insert(0, perfil["tiempo_ciclo"])

    global etiqueta_perfil_actual, perfil_actual
    etiqueta_perfil_actual.config(text=f"🔒 Perfil actual: {perfil_actual['nombre']}", fg="green")



#Función para seleccionar perfil
def seleccionar_perfil_existente():
    perfiles = cargar_perfiles_disponibles()
    if not perfiles:
        return  # No hay perfiles guardados

    ventana_perfil = tk.Toplevel()
    ventana_perfil.title("Seleccionar perfil")
    ventana_perfil.geometry("300x200")

    tk.Label(ventana_perfil, text="Selecciona un perfil:").pack(pady=10)
    perfil_seleccionado = tk.StringVar()
    opciones = list(perfiles.keys())
    combo = ttk.Combobox(ventana_perfil, textvariable=perfil_seleccionado, values=opciones, state="readonly")
    combo.pack(pady=5)

    def cargar_y_cerrar():
        nombre = perfil_seleccionado.get()
        perfil_actual["nombre"] = nombre
        perfil_actual["datos"] = perfiles[nombre]
        cargar_datos_perfil(perfiles[nombre])

        if nombre:
            cargar_datos_perfil(perfiles[nombre])
            ventana_perfil.destroy()

    tk.Button(ventana_perfil, text="Cargar perfil", command=cargar_y_cerrar).pack(pady=10)

# Preguntar si quiere cargar perfil
if messagebox.askyesno("Perfil", "¿Deseas cargar un perfil existente?"):
    seleccionar_perfil_existente()

#Función para reiniciar el programa por completo
def reiniciar_perfil():
    global perfil_actual
    perfil_actual = {"nombre": None, "datos": {}}
    etiqueta_perfil_actual.config(text="🔒 Perfil actual: Ninguno", fg="gray")
    entry_velocidad.delete(0, tk.END)
    entry_largo.delete(0, tk.END)
    entry_ancho.delete(0, tk.END)
    entry_avance.delete(0, tk.END)
    entry_tiempo.delete(0, tk.END)
    entry_broca.set("")
    entry_metal.set("")
    entry_figura.set("")
    messagebox.showinfo("Reiniciado", "Se ha reiniciado la sesión del perfil.\nPuedes crear o cargar uno nuevo.")

# Botón para calcular
boton_calcular = tk.Button(ventana, text="Calcular", command=calcular)
boton_calcular.grid(row=8, column=0, columnspan=2)

# Frame lateral para botones de ayuda
frame_botones_info = tk.Frame(ventana, bg="white")
frame_botones_info.grid(row=9, column=2, padx=(10, 0), sticky="n")

#Botón para exportar los resultados de los 100 datos simulados a un archivo CSV
boton_exportar = tk.Button(ventana, text="📤 Exportar CSV", command=exportar_csv)
boton_exportar.grid(row=0, column=3, padx=10, pady=5, sticky="e")

#Botón para cargar perfil desde la interfaz del programa
boton_cargar = tk.Button(ventana, text="🗂 Cargar perfil", command=seleccionar_perfil_existente)
boton_cargar.grid(row=1, column=3, padx=10, pady=5, sticky="e")

#Botón para eliminar un perfil desde la interfaz del programa
boton_borrar = tk.Button(ventana, text="🗑 Borrar perfil", command=eliminar_perfil)
boton_borrar.grid(row=2, column=3, padx=10, pady=5, sticky="e")

#Botón para reiniciar por completo el programa
boton_reiniciar = tk.Button(ventana, text="🔄 Reiniciar perfil", command=reiniciar_perfil, bg="#8b0000", fg="white")
boton_reiniciar.grid(row=3, column=3, padx=10, pady=5, sticky="e")

# Ejecutar la ventana
ventana.mainloop()
