"""
parachutist_main.py
Script independiente para ejecutar la simulación del paracaidista en una nueva ventana.
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
    """Función principal para la simulación del paracaidista."""
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Paracaidista - Algoritmo Genético")
    clock = pygame.time.Clock()

    # UI y GA
    ui = UI(screen, ground_y=GROUND_Y, show_back_button=False)  # No back button en ventana separada
    poblacion = []
    generacion = 0
    solution_found = False
    running_simulation = False
    max_generations = 100  # Límite máximo de generaciones para evitar bucles infinitos
    last_parachute = None  # Para mantener la simulación en pantalla

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
            last_parachute = None
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
            ui.generation = generacion
            solution_found = False

        if running_simulation and not solution_found and generacion < max_generations:
            # Convertir a ParIndividual para UI
            ui_population = [ParIndividual(ind) for ind in poblacion]
            # Simular y evaluar cada individuo (con render)
            fitnesses = []
            for i, ind in enumerate(poblacion):
                # Ejecutar una generación
                generacion += 1
                ui.generation = generacion
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
                ui_population[i].fitness = fitness
                # Actualizar panel en tiempo real
                ui.set_population(ui_population)
                ui.render_panel()
                pygame.display.flip()
                # Mostrar valores en cada generación
                print(f"Generación {generacion}: V={genes_dict['V']:.2f}, B={genes_dict['B']:.2f}, S={genes_dict['S']:.2f}, F={genes_dict['F']:.2f}, Fitness={fitness:.2f}")
                if result.get("solution_found", False):
                    last_parachute = parachute
                    solution_found = True
                    running_simulation = False
                    print(f"¡Solución encontrada en generación {generacion}!")
                    break  # Detener simulación de la generación actual

            # Después de procesar toda la población, mostrar valores del mejor individuo
            if ui_population:
                best = max(ui_population, key=lambda p: p.fitness)
                print(f"Generación {generacion + 1}: V={best.genes['V']:.2f}, B={best.genes['B']:.2f}, S={best.genes['S']:.2f}, F={best.genes['F']:.2f}, Fitness={best.fitness:.2f}")

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
                # Incrementar generación después de evolución
                generacion += 1
                ui.generation = generacion
            elif generacion >= max_generations:
                running_simulation = False
                print(f"No se encontró solución en {max_generations} generaciones. Presiona Setup para reiniciar.")

        # Render UI base cuando no estamos en la corrida
        ui.render_background()
        if last_parachute:
            last_parachute.render(screen)
        if solution_found:
            font = pygame.font.SysFont("Arial", 28, bold=True)
            txt = font.render("¡Buen trabajo!", True, (0, 120, 0))
            screen.blit(txt, (SCREEN_SIZE[0] // 2 - 80, GROUND_Y - 60))
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