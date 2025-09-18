import random as rd

# --- Categorías de presupuesto ---
categorias = ["Ahorro", "Alimentación", "Vivienda", "Entretenimiento", "Educación"]
tamano = len(categorias)
tamanoPoblacion = 8
iteraciones = 50
probMutacion = 0.3
probCruce = 0.8

# --- Generar un plan financiero (cromosoma) ---
def getIndividuo():
    plan = [rd.randint(0, 100) for _ in range(tamano)]
    total = sum(plan)
    # Normalizamos a 100%
    return [round((p/total)*100) for p in plan]

def getPoblacion(n):
    return [getIndividuo() for _ in range(n)]

# --- Función de aptitud (fitness) ---
def calcularAdaptacion(individuo):
    pesos = [2.0, 1.0, 1.0, 0.5, 1.5]  # prioridades: más ahorro y educación
    score = sum(individuo[i]*pesos[i] for i in range(tamano))
    if sum(individuo) != 100:  # penalización si no suma 100%
        return 0
    return score

# --- Selección ---
def seleccion(poblacion):
    valorados = [(calcularAdaptacion(i), i) for i in poblacion]
    valorados = sorted(valorados, reverse=True, key=lambda x: x[0])
    return [ind for _, ind in valorados[:len(valorados)//2]]

# --- Cruce ---
def cruce(p1, p2):
    if rd.random() < probCruce:
        punto = rd.randint(1, tamano-1)
        h1 = p1[:punto] + p2[punto:]
        h2 = p2[:punto] + p1[punto:]
        return [h1, h2]
    return [p1, p2]

# --- Mutación ---
def mutacion(ind):
    if rd.random() < probMutacion:
        pos = rd.randint(0, tamano-1)
        cambio = rd.randint(-10, 10)
        ind[pos] = max(0, ind[pos] + cambio)
        total = sum(ind)
        if total > 0:
            ind = [round((p/total)*100) for p in ind]
    return ind

# --- Algoritmo principal ---
poblacion = getPoblacion(tamanoPoblacion)

for gen in range(iteraciones):
    seleccionados = seleccion(poblacion)
    nuevaPoblacion = []
    while len(nuevaPoblacion) < tamanoPoblacion:
        padres = rd.sample(seleccionados, 2)
        hijos = cruce(padres[0], padres[1])
        hijos = [mutacion(h) for h in hijos]
        nuevaPoblacion.extend(hijos)
    poblacion = nuevaPoblacion[:tamanoPoblacion]

# --- Mejor plan ---
mejor = max(poblacion, key=lambda ind: calcularAdaptacion(ind))
print("\nMejor plan financiero después de 50 generaciones:")
for cat, val in zip(categorias, mejor):
    print(f"{cat}: {val}%")
print("Puntaje:", calcularAdaptacion(mejor))
