"""
genetic_algorithm.py
Contiene la implementación básica del algoritmo genético:
- Individuo (ParIndividual)
- Población y operadores: selección por torneo, cruce (blend), mutación gaussiana.
"""
import random
import math
from copy import deepcopy


class ParIndividual:
    """Representación simple de individuo con genes V, B, S."""

    def __init__(self, genes: dict):
        self.genes = genes  # dict {'V': float, 'B': float, 'S': float}
        self.fitness = 0.0
        self.survived = False

    def copy(self):
        return ParIndividual(deepcopy(self.genes))


class GeneticAlgorithm:
    """Algoritmo genético para optimizar el aterrizaje del paracaidista."""

    def __init__(self, pop_size=20, gene_bounds=None,
                 crossover_rate=0.8, mutation_rate=0.12):
        """
        :param pop_size: tamaño de la población
        :param gene_bounds: dict con (min, max) por gen
        """
        self.pop_size = pop_size
        self.gene_bounds = gene_bounds or {
            "V": (1.0, 6.0),
            "B": (-2.0, 2.0),
            "S": (0.0, 1.0)
        }
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = []
        self.generation = 0

    def setup_population(self):
        """Genera población inicial aleatoria."""
        self.population = []
        for _ in range(self.pop_size):
            genes = {}
            for k, (mn, mx) in self.gene_bounds.items():
                genes[k] = random.uniform(mn, mx)
            self.population.append(ParIndividual(genes))
        self.generation = 0

    def select_tournament(self, k=3):
        """Selección por torneo."""
        aspirants = random.sample(self.population, k)
        aspirants.sort(key=lambda ind: ind.fitness, reverse=True)
        return aspirants[0].copy()

    def crossover(self, parent1: ParIndividual, parent2: ParIndividual):
        """Cruce tipo blend entre dos padres -> 2 hijos."""
        child1 = parent1.copy()
        child2 = parent2.copy()
        for gene in parent1.genes:
            if random.random() < self.crossover_rate:
                a = random.random()
                g1 = parent1.genes[gene]
                g2 = parent2.genes[gene]
                child1.genes[gene] = a * g1 + (1 - a) * g2
                child2.genes[gene] = a * g2 + (1 - a) * g1
        return child1, child2

    def mutate(self, individual: ParIndividual):
        """Mutación gaussiana limitada por bounds."""
        for gene, (mn, mx) in self.gene_bounds.items():
            if random.random() < self.mutation_rate:
                sigma = (mx - mn) * 0.08
                individual.genes[gene] += random.gauss(0, sigma)
                individual.genes[gene] = max(mn, min(mx, individual.genes[gene]))

    def evolve(self):
        """Genera la siguiente generación usando selección, cruce y mutación."""
        new_pop = []
        # Mantener elite (mejor 1)
        self.population.sort(key=lambda ind: ind.fitness, reverse=True)
        if self.population:
            new_pop.append(self.population[0].copy())

        while len(new_pop) < self.pop_size:
            p1 = self.select_tournament()
            p2 = self.select_tournament()
            c1, c2 = self.crossover(p1, p2)
            self.mutate(c1)
            self.mutate(c2)
            new_pop.append(c1)
            if len(new_pop) < self.pop_size:
                new_pop.append(c2)

        self.population = new_pop
        self.generation += 1
