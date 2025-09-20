"""
menu.py
Pantalla de selección principal con diseño moderno y UX mejorada.
Permite elegir entre simulación del paracaidista y planificador de ahorro.
"""
import pygame
import sys
import math
import os

class MenuButton:
    """Botón moderno con efectos hover y animaciones."""

    def __init__(self, rect, text, font, color, hover_color, callback=None, image_path=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.callback = callback
        self.is_hovered = False
        self.animation_progress = 0.0
        self.pulse_timer = 0.0
        self.image = None
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
            except pygame.error:
                print(f"Error al cargar imagen: {image_path}")

    def update(self, dt):
        """Actualiza animaciones del botón."""
        if self.is_hovered:
            self.animation_progress = min(1.0, self.animation_progress + dt * 5)
            self.pulse_timer += dt
        else:
            self.animation_progress = max(0.0, self.animation_progress - dt * 5)
            self.pulse_timer = 0.0

    def draw(self, screen):
        """Dibuja el botón con efectos visuales."""
        # Color base con interpolación
        current_color = self._lerp_color(self.color, self.hover_color, self.animation_progress)

        # Efecto de pulso cuando está en hover
        if self.is_hovered:
            pulse = (math.sin(self.pulse_timer * 8) + 1) * 0.1 + 0.9
            current_color = self._multiply_color(current_color, pulse)

        # Dibujar sombra
        shadow_offset = 3
        shadow_color = (0, 0, 0, 100)
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=15)

        # Dibujar rectángulo principal con esquinas redondeadas (simulado)
        pygame.draw.rect(screen, current_color, self.rect, border_radius=15)

        # Borde sutil con glow en hover
        border_color = self._adjust_brightness(current_color, 0.8)
        border_width = 3 if self.is_hovered else 2
        pygame.draw.rect(screen, border_color, self.rect, border_width, border_radius=15)

        # Dibujar imagen si existe
        image_offset = 0
        if self.image:
            image_rect = self.image.get_rect(center=(self.rect.centerx - 60, self.rect.centery))
            screen.blit(self.image, image_rect)
            image_offset = 40  # Desplazar texto a la derecha

        # Texto centrado con sombra sutil
        text_color = (255, 255, 255) if self._is_dark(current_color) else (20, 20, 20)

        # Sombra del texto
        shadow_txt = self.font.render(self.text, True, (0, 0, 0))
        shadow_rect = shadow_txt.get_rect(center=(self.rect.centerx + image_offset + 1, self.rect.centery + 1))
        screen.blit(shadow_txt, shadow_rect)

        # Texto principal
        txt = self.font.render(self.text, True, text_color)
        txt_rect = txt.get_rect(center=(self.rect.centerx + image_offset, self.rect.centery))
        screen.blit(txt, txt_rect)

    def handle_event(self, event):
        """Maneja eventos del mouse."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.callback:
                self.callback()

    def _lerp_color(self, color1, color2, t):
        """Interpolación lineal entre dos colores."""
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t)
        )

    def _multiply_color(self, color, factor):
        """Multiplica un color por un factor."""
        return (
            min(255, int(color[0] * factor)),
            min(255, int(color[1] * factor)),
            min(255, int(color[2] * factor))
        )

    def _adjust_brightness(self, color, factor):
        """Ajusta el brillo de un color."""
        return self._multiply_color(color, factor)

    def _is_dark(self, color):
        """Determina si un color es oscuro."""
        return (color[0] + color[1] + color[2]) / 3 < 128

class MainMenu:
    """Pantalla principal de selección con diseño moderno."""

    def __init__(self, screen_size=(900, 600)):
        self.screen_size = screen_size
        self.screen = None
        self.clock = None
        self.running = True
        self.selected_option = None

        # Colores del tema moderno
        self.colors = {
            'background': [(15, 32, 39), (32, 58, 67), (26, 83, 92)],
            'primary': (100, 181, 246),
            'secondary': (77, 182, 172),
            'accent': (255, 193, 7),
            'text': (255, 255, 255),
            'text_dark': (33, 33, 33)
        }

        # Fuentes
        self.title_font = None
        self.button_font = None
        self.subtitle_font = None

        # Botones
        self.buttons = []
        self.animation_timer = 0.0

    def init_pygame(self, screen):
        """Inicializa elementos de Pygame."""
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Fuentes
        self.title_font = pygame.font.SysFont("Segoe UI", 48, bold=True)
        self.button_font = pygame.font.SysFont("Segoe UI", 24, bold=True)
        self.subtitle_font = pygame.font.SysFont("Segoe UI", 18)

        # Crear botones
        self._create_buttons()

    def _create_buttons(self):
        """Crea los botones del menú."""
        center_x = self.screen_size[0] // 2
        button_width = 300
        button_height = 60
        spacing = 100

        # Botón Paracaidista
        parachute_image = os.path.join("assets", "parachute.png")
        btn_parachute = MenuButton(
            (center_x - button_width // 2, 250, button_width, button_height),
            "Simulación Paracaidista",
            self.button_font,
            self.colors['primary'],
            self.colors['secondary'],
            callback=self._select_parachutist
        )

        # Botón Ahorro Genético
        btn_savings = MenuButton(
            (center_x - button_width // 2, 250 + spacing, button_width, button_height),
            "Planificador de Ahorro",
            self.button_font,
            self.colors['secondary'],
            self.colors['primary'],
            callback=self._select_savings
        )

        # Botón Salir
        btn_exit = MenuButton(
            (center_x - button_width // 2, 250 + spacing * 2, button_width, button_height),
            "Salir",
            self.button_font,
            (244, 67, 54),
            (211, 47, 47),
            callback=self._exit_app
        )

        self.buttons = [btn_parachute, btn_savings, btn_exit]

    def _select_parachutist(self):
        """Selecciona la simulación del paracaidista."""
        self.selected_option = "parachutist"
        self.running = False

    def _select_savings(self):
        """Selecciona el planificador de ahorro."""
        self.selected_option = "savings"
        self.running = False

    def _exit_app(self):
        """Sale de la aplicación."""
        self.selected_option = "exit"
        self.running = False

    def _draw_background(self):
        """Dibuja el fondo con gradiente animado y elementos decorativos."""
        # Gradiente animado base
        time_factor = self.animation_timer * 0.5
        for i, color in enumerate(self.colors['background']):
            alpha = 0.3 + 0.2 * math.sin(time_factor + i * math.pi / 3)
            alpha = max(0.1, min(1.0, alpha))

            # Crear superficie con alpha
            surface = pygame.Surface(self.screen_size)
            surface.set_alpha(int(alpha * 255))
            surface.fill(color)
            self.screen.blit(surface, (0, 0))

        # Patrón de puntos sutil con variación
        for x in range(0, self.screen_size[0], 50):
            for y in range(0, self.screen_size[1], 50):
                # Variar el tamaño y color de los puntos
                size = 1 + int(math.sin(time_factor + x * 0.01 + y * 0.01) * 0.5)
                alpha = 20 + int(math.sin(time_factor * 2 + x * 0.02) * 10)
                dot_color = (*self.colors['primary'][:3], alpha)
                pygame.draw.circle(self.screen, dot_color, (x, y), size)

        # Elementos decorativos: líneas diagonales sutiles
        for i in range(0, self.screen_size[0] + self.screen_size[1], 100):
            start_pos = (i, 0) if i < self.screen_size[0] else (self.screen_size[0], i - self.screen_size[0])
            end_pos = (i - self.screen_size[1], self.screen_size[1]) if i > self.screen_size[1] else (0, i)

            line_color = (*self.colors['accent'][:3], 15)
            pygame.draw.line(self.screen, line_color, start_pos, end_pos, 1)

    def _draw_title(self):
        """Dibuja el título principal."""
        title_text = "Algoritmos Genéticos"
        subtitle_text = "Selecciona una simulación"

        # Título principal
        title = self.title_font.render(title_text, True, self.colors['text'])
        title_rect = title.get_rect(center=(self.screen_size[0] // 2, 120))
        self.screen.blit(title, title_rect)

        # Subtítulo
        subtitle = self.subtitle_font.render(subtitle_text, True, self.colors['accent'])
        subtitle_rect = subtitle.get_rect(center=(self.screen_size[0] // 2, 170))
        self.screen.blit(subtitle, subtitle_rect)

    def _draw_buttons(self, dt):
        """Dibuja todos los botones."""
        for button in self.buttons:
            button.update(dt)
            button.draw(self.screen)

    def run(self, screen):
        """Ejecuta el menú principal."""
        self.init_pygame(screen)

        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.animation_timer += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.selected_option = "exit"
                    self.running = False
                else:
                    for button in self.buttons:
                        button.handle_event(event)

            # Dibujar
            self._draw_background()
            self._draw_title()
            self._draw_buttons(dt)

            pygame.display.flip()

        return self.selected_option

def show_main_menu(screen):
    """Función de conveniencia para mostrar el menú."""
    menu = MainMenu(screen.get_size())
    return menu.run(screen)