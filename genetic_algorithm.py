"""
genetic_algorithm.py
Implementación del algoritmo genético para el paracaidista, basada en el ejemplo proporcionado.
"""
import random
import math
from copy import deepcopy
from parachutist import Parachutist

# --- Parámetros del problema ---
tamano_cromosoma = 4  # V, B, S, F
bounds = [(1.5, 6.0), (-1.5, 1.5), (0.0, 1.0), (0.0, 1.0)]  # límites para V, B, S, F

# --- Parámetros GA ---
tamanoPoblacion = 20
probSeleccion = 0.5
probMutacion = 0.1  # Ajustado para valores continuos
probCruce = 0.8
iteraciones = 100  # Máximo de generaciones

# --- Representación de cromosomas ---
def getIndividuo():
    """Genera un cromosoma aleatorio [V, B, S]."""
    return [random.uniform(bounds[i][0], bounds[i][1]) for i in range(tamano_cromosoma)]

def getPoblacion(n):
    return [getIndividuo() for _ in range(n)]

# --- Función de aptitud ---
def calcularAdaptacion(individuo):
    """Evalúa el fitness del individuo simulando el aterrizaje."""
    genes_dict = {'V': individuo[0], 'B': individuo[1], 'S': individuo[2], 'F': individuo[3]}
    parachute = Parachutist(genes_dict, x=400, y=-40)
    result = parachute.simulate(ground_y=520, render=False)
    return result["fitness"]

# --- Selección ---
def seleccion(poblacion):
    """Selecciona un subconjunto de la población basado en fitness."""
    listaValorados = [(calcularAdaptacion(i), i) for i in poblacion]
    listaOrdenados = sorted(listaValorados, reverse=True, key=lambda x: x[0])
    numSeleccionados = int(len(listaOrdenados) * probSeleccion)
    return [ind for _, ind in listaOrdenados[:numSeleccionados]]

# --- Cruce ---
def cruce(padre1, padre2):
    if random.random() < probCruce:
        punto = random.randint(1, tamano_cromosoma - 1)
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return [hijo1, hijo2]
    return [padre1[:], padre2[:]]

# --- Mutación ---
def mutacion(individuo):
    for i in range(tamano_cromosoma):
        if random.random() < probMutacion:
            # Mutación gaussiana limitada por bounds
            sigma = (bounds[i][1] - bounds[i][0]) * 0.1
            individuo[i] += random.gauss(0, sigma)
            individuo[i] = max(bounds[i][0], min(bounds[i][1], individuo[i]))
    return individuo

# --- Algoritmo principal ---
def ejecutar_algoritmo_genetico():
    poblacion = getPoblacion(tamanoPoblacion)
    generacion = 0

    while generacion < iteraciones:
        generacion += 1
        seleccionados = seleccion(poblacion)
        nuevaPoblacion = []

        while len(nuevaPoblacion) < tamanoPoblacion:
            padres = random.sample(seleccionados, 2)
            hijos = cruce(padres[0], padres[1])
            hijos = [mutacion(h) for h in hijos]
            nuevaPoblacion.extend(hijos)

        poblacion = nuevaPoblacion[:tamanoPoblacion]

        # Verificar si hay solución óptima
        mejor_fitness = max(calcularAdaptacion(ind) for ind in poblacion)
        if mejor_fitness > 0.8:  # Umbral para aterrizaje correcto
            print(f"¡Solución encontrada en generación {generacion}!")
            break

    # Mejor solución
    mejor = max(poblacion, key=lambda ind: calcularAdaptacion(ind))
    print("Mejor cromosoma:", mejor)
    print("Fitness:", calcularAdaptacion(mejor))
    return mejor, generacion

# Para compatibilidad con el código existente, mantener ParIndividual pero adaptado
class ParIndividual:
    """Adaptación para compatibilidad con UI."""

    def __init__(self, cromosoma):
        self.cromosoma = cromosoma  # lista [V, B, S, F]
        self.genes = {'V': cromosoma[0], 'B': cromosoma[1], 'S': cromosoma[2], 'F': cromosoma[3]}
        self.fitness = 0.0

    def copy(self):
        return ParIndividual(deepcopy(self.cromosoma))

class GeneticAlgorithm:
    """Wrapper para compatibilidad."""

    def __init__(self, pop_size=20):
        self.pop_size = pop_size
        self.population = []
        self.generation = 0

    def setup_population(self):
        self.population = [ParIndividual(getIndividuo()) for _ in range(self.pop_size)]
        self.generation = 0

    def evolve(self):
        # Implementar evolución simple
        # Para simplicidad, usar el nuevo algoritmo
        pass
