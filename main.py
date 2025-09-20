"""
main.py
Punto de entrada principal con menú de selección.
Permite elegir entre simulación del paracaidista y planificador de ahorro.
Ejecutar: python main.py
"""
import sys
import pygame
import random
import subprocess
import os
from ui import UI
from menu import show_main_menu
from genetic_algorithm import getPoblacion, seleccion, cruce, mutacion, calcularAdaptacion, tamanoPoblacion, iteraciones
from parachutist import Parachutist

FPS = 60
SCREEN_SIZE = (900, 600)
GROUND_Y = 520  # y en píxeles del "suelo"


def run_parachutist_simulation():
    """Ejecuta la simulación del paracaidista en una nueva ventana."""
    try:
        script_path = os.path.join(os.path.dirname(__file__), "parachutist_main.py")
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar la simulación del paracaidista: {e}")
    except FileNotFoundError:
        print("No se encontró el archivo parachutist_main.py")

    return "menu"


def run_savings_planner():
    """Ejecuta el planificador de ahorro genético."""
    try:
        # Ejecutar el script de ahorro genético
        script_path = os.path.join(os.path.dirname(__file__), "ahorro_genetico.py")
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el planificador de ahorro: {e}")
    except FileNotFoundError:
        print("No se encontró el archivo ahorro_genetico.py")

    return "menu"  # Volver al menú después de cerrar la ventana de Tkinter


def main():
    """Función principal que maneja el flujo de la aplicación."""
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Algoritmos Genéticos - Menú Principal")
    clock = pygame.time.Clock()

    current_state = "menu"

    while current_state != "exit":
        if current_state == "menu":
            # Mostrar menú principal
            selection = show_main_menu(screen)
            if selection == "parachutist":
                current_state = "parachutist"
            elif selection == "savings":
                current_state = "savings"
            elif selection == "exit":
                current_state = "exit"

        elif current_state == "parachutist":
            # Ejecutar simulación del paracaidista
            result = run_parachutist_simulation()
            if result == "menu":
                current_state = "menu"
            else:
                current_state = "exit"

        elif current_state == "savings":
            # Ejecutar planificador de ahorro
            result = run_savings_planner()
            if result == "menu":
                current_state = "menu"
            else:
                current_state = "exit"

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
