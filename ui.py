"""
ui.py
Contiene clases UI simples: Button, Panel y lógica de render básico.
Se implementa patrón de eventos para botones y panel lateral con V, B, S, F.
"""
import pygame


class Button:
    """Botón simple con callback (patrón de eventos)."""

    def __init__(self, rect, text, font, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.is_pressed = False

    def draw(self, screen):
        pygame.draw.rect(screen, (230, 230, 230), self.rect)
        pygame.draw.rect(screen, (80, 80, 80), self.rect, 2)
        txt = self.font.render(self.text, True, (20, 20, 20))
        txt_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                if self.callback:
                    self.callback()
            else:
                self.is_pressed = False


class UI:
    """Interfaz sencilla con botones Setup y Ejecutar y panel lateral."""

    def __init__(self, screen, ground_y=520):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.ground_y = ground_y
        self.font = pygame.font.SysFont("Arial", 16)
        # Botones
        self.clicked_setup = False
        self.clicked_run = False
        btn_w, btn_h = 100, 36
        self.btn_setup = Button((20, 20, btn_w, btn_h), "Setup", self.font,
                                callback=self._on_setup)
        self.btn_run = Button((140, 20, btn_w, btn_h), "Ejecutar", self.font,
                              callback=self._on_run)
        # Panel data
        self.panel_rect = pygame.Rect(self.width - 220, 0, 220, self.height)
        self.population = []
        self.generation = 0

    def _on_setup(self):
        self.clicked_setup = True

    def _on_run(self):
        self.clicked_run = True

    def handle_event(self, event):
        self.btn_setup.handle_event(event)
        self.btn_run.handle_event(event)

    def render_background(self):
        # cielo y suelo
        self.screen.fill((200, 220, 255))
        pygame.draw.rect(self.screen, (60, 170, 65),
                         (0, self.ground_y, self.width, self.height - self.ground_y))
        # dibujar botones
        self.btn_setup.draw(self.screen)
        self.btn_run.draw(self.screen)

    def render_panel(self):
        pygame.draw.rect(self.screen, (245, 245, 245), self.panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), self.panel_rect, 2)
        x = self.panel_rect.x + 12
        y = 18
        title = self.font.render("Panel", True, (10, 10, 10))
        self.screen.blit(title, (x, y))
        y += 30
        gen_txt = self.font.render(f"Generación: {self.generation}", True, (10, 10, 10))
        self.screen.blit(gen_txt, (x, y))
        y += 24

        # Mostrar promedio o del mejor
        if self.population:
            best = max(self.population, key=lambda p: p.fitness)
            stats = [
                f"V: {best.genes['V']:.2f}",
                f"B: {best.genes['B']:.2f}",
                f"S: {best.genes['S']:.2f}",
                f"F: {best.genes['F']:.2f}",
                f"Fitness: {best.fitness:.2f}"
            ]
        else:
            stats = ["V: -", "B: -", "S: -", "F: -", "Fitness: -"]

        for s in stats:
            txt = self.font.render(s, True, (10, 10, 10))
            self.screen.blit(txt, (x, y))
            y += 22

    def set_population(self, population):
        """Recibe lista de ParIndividual para mostrar en panel y preview."""
        self.population = population

    def render_population_preview(self, population):
        """
        Dibuja una vista previa pequeña de algunos individuos como puntos en la parte media.
        No es la simulación completa, solo un preview estético.
        """
        if not population:
            return
        base_y = 120
        start_x = 80
        gap = 26
        for i, ind in enumerate(population[:10]):
            gx = start_x + i * gap
            # map genes a posición de muestra
            vy = int(14 + (ind.genes["V"] - 1.5) * 6)
            bx = int( gx + ind.genes["B"] * 4)
            color = (40, 40, 200) if ind.fitness > 0.8 else (180, 40, 40)
            #pygame.draw.circle(self.screen, color, (bx, base_y + vy), 6)
