"""
main.py
Punto de entrada para la simulación del paracaidista con algoritmo genético.
Ejecutar: python main.py
"""
import sys
import pygame
from ui import UI
from genetic_algorithm import GeneticAlgorithm
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
    ga = GeneticAlgorithm(pop_size=18, gene_bounds={
        "V": (1.5, 6.0),    # velocidad de caída base
        "B": (-1.5, 1.5),   # balanceo lateral (der/izq)
        "S": (0.0, 1.0)     # estabilidad (reduce rotación)
    })

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_event(event)

        # Botones
        if ui.clicked_setup:
            # Genera población inicial
            ga.setup_population()
            ui.set_population(ga.population)
            ui.generation = 0
            ui.clicked_setup = False

        if ui.clicked_run:
            # Bloqueante hasta que al menos uno sobreviva
            ui.clicked_run = False
            solution_found = False
            max_generations = 200
            while not solution_found and ui.generation < max_generations:
                ui.generation = ga.generation
                # Simular y evaluar cada individuo (con render)
                fitnesses = []
                survivors = []
                for p in ga.population:
                    # Crear instancia visual de Parachutist con genes
                    parachute = Parachutist.from_genes(p.genes, start_x=SCREEN_SIZE[0] // 2)
                    # Simula con render callback para ver caída
                    result = parachute.simulate(
                        screen=screen,
                        ground_y=GROUND_Y,
                        render=True,
                        ui=ui
                    )
                    p.fitness = result["fitness"]
                    p.survived = result["survived"]
                    fitnesses.append(p.fitness)
                    survivors.append(p.survived)

                # Mostrar panel una vez por generación
                ui.set_population(ga.population)
                pygame.display.flip()
                pygame.time.delay(600)

                # Check
                if any(survivors):
                    solution_found = True
                    print(f"¡Solución encontrada en generación {ga.generation}!")
                else:
                    ga.evolve()
                    ui.generation = ga.generation

            if not solution_found:
                print("No se consiguió solución dentro del máximo de generaciones.")

        # Render UI base cuando no estamos en la corrida
        ui.render_background()
        ui.render_population_preview(ga.population)
        ui.render_panel()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
