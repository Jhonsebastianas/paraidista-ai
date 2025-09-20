import random as rd

# === Entrada de usuario ===
ingreso_mensual = float(input("💰 Ingreso mensual: "))
meta_ahorro = float(input("🎯 Meta de ahorro total: "))
plazo_meses = int(input("📅 Plazo en meses: "))

# === Parámetros del AG ===
tamano_poblacion = 12
iteraciones = 50
prob_mutacion = 0.3

# Cromosoma: porcentaje destinado a ahorro
def crear_individuo():
    return [rd.uniform(0.1, 0.8)]  # porcentaje de ahorro entre 10% y 80%

def crear_poblacion():
    return [crear_individuo() for _ in range(tamano_poblacion)]

def fitness(individuo):
    porcentaje = individuo[0]
    ahorro_total = ingreso_mensual * porcentaje * plazo_meses
    return -abs(meta_ahorro - ahorro_total)

def seleccionar_padres(poblacion):
    return rd.sample(poblacion, 2)

def cruce(p1, p2):
    return [(p1[0] + p2[0]) / 2]

def mutacion(individuo):
    if rd.random() < prob_mutacion:
        individuo[0] = rd.uniform(0.1, 0.8)
    return individuo

# === Algoritmo Genético ===
poblacion = crear_poblacion()
for _ in range(iteraciones):
    poblacion = sorted(poblacion, key=fitness, reverse=True)
    nueva = poblacion[:2]  # elitismo
    print(nueva)
    while len(nueva) < tamano_poblacion:
        padres = seleccionar_padres(poblacion[:5])
        hijo = cruce(*padres)
        hijo = mutacion(hijo)
        nueva.append(hijo)
    poblacion = nueva

mejor = max(poblacion, key=fitness)
print("\n🔹 Mejor plan encontrado (Meta de ahorro en X meses)")
print(f"Ahorro mensual: {mejor[0]*100:.2f}% del ingreso")
print(f"Ahorro total: {ingreso_mensual * mejor[0] * plazo_meses:.2f} / Meta: {meta_ahorro}")
