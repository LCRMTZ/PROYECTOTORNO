from flask import Flask, render_template, redirect, url_for
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def principal():
    return render_template("principal.html")

@app.route("/quienes-somos")
def quienes_somos():
    return render_template("quienes-somos.html")

@app.route("/simulador")
def ejecutar_simulacion():
    try:
        # Abre el simulador en una ventana independiente
        subprocess.Popen(["python", "SimuladorFatiga.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        return redirect(url_for("principal"))  # O simplemente: return redirect("/")
    except Exception as e:
        return f"Error al ejecutar el simulador: {e}"

if __name__ == "__main__":
    app.run(debug=True)
