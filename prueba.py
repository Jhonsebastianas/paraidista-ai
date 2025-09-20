import tkinter as tk
from tkinter import ttk
import random as rd

def algoritmo_genetico(ingreso_mensual, meta_ahorro, plazo_meses):
    tamano_poblacion = 12
    iteraciones = 50
    prob_mutacion = 0.3

    def crear_individuo():
        return [rd.uniform(0.1, 0.8)]

    def crear_poblacion():
        return [crear_individuo() for _ in range(tamano_poblacion)]

    def fitness(individuo):
        porcentaje = individuo[0]
        ahorro_total = ingreso_mensual * porcentaje * plazo_meses
        print("Absoluto raro: ", -abs(meta_ahorro - ahorro_total))
        return -abs(meta_ahorro - ahorro_total)

    def seleccionar_padres(poblacion):
        return rd.sample(poblacion, 2)

    def cruce(p1, p2):
        return [(p1[0] + p2[0]) / 2]

    def mutacion(individuo):
        if rd.random() < prob_mutacion:
            individuo[0] = rd.uniform(0.1, 0.8)
        return individuo

    poblacion = crear_poblacion()
    for _ in range(iteraciones):
        poblacion = sorted(poblacion, key=fitness, reverse=True)
        nueva = poblacion[:2]
        while len(nueva) < tamano_poblacion:
            padres = seleccionar_padres(poblacion[:5])
            hijo = cruce(*padres)
            hijo = mutacion(hijo)
            nueva.append(hijo)
        poblacion = nueva

    mejor = max(poblacion, key=fitness)
    ahorro_mensual = mejor[0] * ingreso_mensual
    ahorro_total = ingreso_mensual * mejor[0] * plazo_meses
    return mejor[0], ahorro_mensual, ahorro_total

def calcular():
    try:
        ingreso = float(entry_ingreso.get())
        meta = float(entry_meta.get())
        plazo = int(entry_plazo.get())
        porcentaje, mensual, total = algoritmo_genetico(ingreso, meta, plazo)
        resultado.set(
            f"Ahorro mensual: {porcentaje*100:.2f}%\n"
            f"Ahorro mensual: ${mensual:,.2f}\n"
            f"Ahorro total: ${total:,.2f}\n"
            f"Meta: ${meta:,.2f}"
        )
    except Exception as e:
        resultado.set("Error en los datos ingresados.")



# --- Interfaz moderna ---
root = tk.Tk()
root.title("Planificador de Ahorro - Algoritmo Genético")
root.geometry("900x450")  # Ventana más grande
root.configure(bg="#f0f4f8")

# Colores y estilos
COLOR_PRIMARIO = "#1976d2"
COLOR_SECUNDARIO = "#ffffff"
COLOR_BOTON = "#43a047"
COLOR_BOTON_TXT = "#ffffff"
FUENTE_TITULO = ("Segoe UI", 18, "bold")
FUENTE_LABEL = ("Segoe UI", 12)
FUENTE_RESULT = ("Consolas", 13, "bold")

main_frame = tk.Frame(root, bg="#f0f4f8", padx=30, pady=30)
main_frame.pack(fill="both", expand=True)

# Izquierda: Entradas
frame_izq = tk.Frame(main_frame, bg=COLOR_SECUNDARIO, bd=2, relief="groove")
frame_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 30), ipadx=20, ipady=20)

tk.Label(frame_izq, text="Planificador de Ahorro", font=FUENTE_TITULO, fg=COLOR_PRIMARIO, bg=COLOR_SECUNDARIO).grid(row=0, column=0, columnspan=2, pady=(0, 20))

tk.Label(frame_izq, text="💰 Ingreso mensual:", font=FUENTE_LABEL, bg=COLOR_SECUNDARIO).grid(row=1, column=0, sticky="w")
entry_ingreso = ttk.Entry(frame_izq, font=FUENTE_LABEL, width=20)
entry_ingreso.grid(row=2, column=0, pady=(0, 15), sticky="w")

tk.Label(frame_izq, text="🎯 Meta de ahorro total:", font=FUENTE_LABEL, bg=COLOR_SECUNDARIO).grid(row=3, column=0, sticky="w")
entry_meta = ttk.Entry(frame_izq, font=FUENTE_LABEL, width=20)
entry_meta.grid(row=4, column=0, pady=(0, 15), sticky="w")

tk.Label(frame_izq, text="📅 Plazo en meses:", font=FUENTE_LABEL, bg=COLOR_SECUNDARIO).grid(row=5, column=0, sticky="w")
entry_plazo = ttk.Entry(frame_izq, font=FUENTE_LABEL, width=20)
entry_plazo.grid(row=6, column=0, pady=(0, 20), sticky="w")

btn_calcular = tk.Button(
    frame_izq, text="Calcular", command=calcular,
    font=("Segoe UI", 12, "bold"), bg=COLOR_BOTON, fg=COLOR_BOTON_TXT,
    activebackground="#388e3c", activeforeground=COLOR_BOTON_TXT, bd=0, padx=20, pady=8, cursor="hand2"
)
btn_calcular.grid(row=7, column=0, pady=(10, 0), sticky="w")

# Derecha: Resultados
frame_der = tk.Frame(main_frame, bg=COLOR_SECUNDARIO, bd=2, relief="groove")
frame_der.grid(row=0, column=1, sticky="nsew", ipadx=20, ipady=20)

tk.Label(frame_der, text="🔹 Resultados", font=FUENTE_TITULO, fg=COLOR_PRIMARIO, bg=COLOR_SECUNDARIO).pack(anchor="w", pady=(0, 10))
resultado = tk.StringVar()
tk.Label(frame_der, textvariable=resultado, font=FUENTE_RESULT, bg=COLOR_SECUNDARIO, fg="#222").pack(anchor="w", pady=10)

root.mainloop()