"""
parachutist.py
Clase Parachutist con genes y simulación visual usando sprites.
"""
import math
import pygame
import random
import os


class Parachutist:
    """
    Parachutist representa un individuo físico que cae.
    Genes: V (velocidad de caída), B (balanceo lateral), S (estabilidad)
    """

    WIDTH = 32 * 3
    HEIGHT = 48 * 2
    parachute_img = None
    dust_img = None

    def __init__(self, genes: dict, x: int, y: int = -40):
        self.genes = genes
        self.x = float(x)
        self.y = float(y)
        self.vy = 0.0
        self.vx = 0.0
        self.angle = 0.0
        self.landed = False

        # Cargar imágenes solo una vez
        if Parachutist.parachute_img is None:
            assets_path = os.path.join("assets", "parachute.png")
            if os.path.exists(assets_path):
                img = pygame.image.load(assets_path).convert_alpha()
                Parachutist.parachute_img = pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
            else:
                Parachutist.parachute_img = None

        if Parachutist.dust_img is None:
            dust_path = os.path.join("assets", "dust.png")
            if os.path.exists(dust_path):
                img = pygame.image.load(dust_path).convert_alpha()
                Parachutist.dust_img = pygame.transform.scale(img, (100, 80))
            else:
                Parachutist.dust_img = None

    @classmethod
    def from_genes(cls, genes: dict, start_x: int):
        """Crear instancia a partir de genes y posición inicial X."""
        return cls(genes=genes.copy(), x=start_x, y=-40)

    def step_physics(self, dt=1.0):
        """Actualiza la física sencilla del paracaidista."""
        g_base = self.genes["V"]
        self.vy += g_base * 0.6 * dt
        drift = self.genes["B"] * (0.6 + 0.4 * random.random())
        self.vx += drift * dt
        ang_speed = (1.2 - self.genes["S"]) * (random.random() - 0.5)
        self.angle += ang_speed * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def render(self, screen):
        """Dibuja el paracaidista en pantalla."""
        if Parachutist.parachute_img:
            rotated = pygame.transform.rotate(Parachutist.parachute_img, math.degrees(self.angle))
            rect = rotated.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated, rect.topleft)
        else:
            # fallback: rectángulo azul
            rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
            rect.center = (int(self.x), int(self.y))
            pygame.draw.rect(screen, (30, 144, 255), rect)

    def render_dust(self, screen):
        """Renderiza la nube de polvo al fallar."""
        if Parachutist.dust_img:
            rect = Parachutist.dust_img.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(Parachutist.dust_img, rect.topleft)
        else:
            pygame.draw.circle(screen, (150, 150, 150), (int(self.x), int(self.y)), 20)

    def simulate(self, screen=None, ground_y=520, render=False, ui=None):
        """
        Simula la caída hasta tocar suelo.
        Si 'render' es True y se pasa 'screen', dibuja la caída en pantalla.
        Retorna dict con fitness (mayor es mejor) y survived: bool.
        """
        clock = pygame.time.Clock()
        max_steps = 1000
        steps = 0
        target_x = screen.get_width() // 2 if screen else 400

        while self.y < ground_y and steps < max_steps:
            # 🔥 Actualizar solo la física vertical
            self.step_physics(dt=1.0)
            self.x = target_x   # 🔥 Mantener X fijo en el centro
            steps += 1

            if render and screen:
                if ui:
                    ui.render_background()
                    ui.render_panel()
                else:
                    screen.fill((200, 220, 255))
                    pygame.draw.rect(screen, (50, 160, 70),
                                    (0, ground_y, screen.get_width(), screen.get_height() - ground_y))
                self.render(screen)
                pygame.display.flip()
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        raise SystemExit
                clock.tick(60)

        # Evaluación al aterrizar (solo se mide ángulo)
        dist_x = 0   # 🔥 Como ya no hay movimiento lateral, siempre centrado
        angle_penalty = abs(self.angle)

        fitness = max(0.0, (0.6 - angle_penalty))
        fitness += 0.5 * self.genes.get("S", 0.0)
        fitness += 0.3 * self.genes.get("F", 0.0)

        if render and screen:
            if fitness <= 0.95:  # No aterrizaje correcto
                self.render_dust(screen)
            pygame.display.flip()
            pygame.time.delay(700)

        return {"fitness": fitness, "x": self.x, "angle": self.angle, "solution_found": fitness > 0.95}
