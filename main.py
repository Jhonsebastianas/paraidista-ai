"""
main.py
Punto de entrada para la simulación del paracaidista con algoritmo genético.
Ejecutar: python main.py
"""
import sys
import pygame
import random
from ui import UI
from genetic_algorithm import getPoblacion, seleccion, cruce, mutacion, calcularAdaptacion, tamanoPoblacion, iteraciones
from parachutist import Parachutist

FPS = 60
SCREEN_SIZE = (900, 600)
GROUND_Y = 520  # y en píxeles del "suelo"


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Paracaidista - Algoritmo Genético")
    clock = pygame.time.Clock()

    # UI y GA
    ui = UI(screen, ground_y=GROUND_Y)
    poblacion = []
    generacion = 0
    solution_found = False
    running_simulation = False
    max_generations = 100  # Límite máximo de generaciones para evitar bucles infinitos

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_event(event)

        # Botones
        if ui.clicked_setup:
            # Genera población inicial
            poblacion = getPoblacion(tamanoPoblacion)
            # Convertir a ParIndividual para UI
            from genetic_algorithm import ParIndividual
            ui_population = [ParIndividual(ind) for ind in poblacion]
            for ind in ui_population:
                ind.fitness = calcularAdaptacion(ind.cromosoma)
            ui.set_population(ui_population)
            generacion = 0
            ui.generation = generacion
            solution_found = False
            ui.clicked_setup = False

        if ui.clicked_run:
            ui.clicked_run = False
            if solution_found:
                print("Solución ya encontrada. Presiona Setup para reiniciar.")
                continue
            if not poblacion:
                print("Primero presiona Setup para generar la población inicial.")
                continue
            # Iniciar simulación automática
            running_simulation = True
            generacion = 0  # Iniciar con generación 0
            simulation_count = 0  # Contador de simulaciones
            ui.generation = simulation_count
            solution_found = False

        if running_simulation and not solution_found and generacion < max_generations:
            # Ejecutar una generación
            generacion += 1
            # Simular y evaluar cada individuo (con render)
            fitnesses = []
            for ind in poblacion:
                simulation_count += 1
                ui.generation = simulation_count
                # Crear instancia visual de Parachutist con genes
                genes_dict = {'V': ind[0], 'B': ind[1], 'S': ind[2], 'F': ind[3]}
                parachute = Parachutist.from_genes(genes_dict, start_x=SCREEN_SIZE[0] // 2)
                # Simula con render callback para ver caída
                result = parachute.simulate(
                    screen=screen,
                    ground_y=GROUND_Y,
                    render=True,
                    ui=ui
                )
                fitness = result["fitness"]
                fitnesses.append(fitness)
                if result.get("solution_found", False):
                    solution_found = True
                    running_simulation = False
                    print(f"¡Solución encontrada en generación {generacion}!")
                    break  # Detener simulación de la generación actual

            # Mostrar panel una vez por generación
            # Convertir a ParIndividual para UI
            ui_population = [ParIndividual(ind) for ind in poblacion]
            for ind, fit in zip(ui_population, fitnesses):
                ind.fitness = fit
            # Los no simulados quedan con fitness 0
            ui.set_population(ui_population)
            pygame.display.flip()
            pygame.time.delay(600)

            if not solution_found:
                # Evolución
                seleccionados = seleccion(poblacion)
                nuevaPoblacion = []
                while len(nuevaPoblacion) < tamanoPoblacion:
                    padres = random.sample(seleccionados, 2)
                    hijos = cruce(padres[0], padres[1])
                    hijos = [mutacion(h) for h in hijos]
                    nuevaPoblacion.extend(hijos)
                poblacion = nuevaPoblacion[:tamanoPoblacion]
            elif generacion >= max_generations:
                running_simulation = False
                print(f"No se encontró solución en {max_generations} generaciones. Presiona Setup para reiniciar.")

        # Render UI base cuando no estamos en la corrida
        ui.render_background()
        if poblacion:
            ui_population = [ParIndividual(ind) for ind in poblacion]
            for ind in ui_population:
                ind.fitness = calcularAdaptacion(ind.cromosoma)
            ui.render_population_preview(ui_population)
        else:
            ui.render_population_preview([])
        ui.render_panel()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
