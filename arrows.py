import pygame
import random
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ARROW_MIN_SPEED, ARROW_MAX_SPEED, LIMITED_ARROWS, CENTER, RADIUS, ARROW_SIZE

class ArrowManager:
    def __init__(self, image_path):
        self.arrows = []
        self.size = ARROW_SIZE
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.respawn_delay = 0
        self.freeze_timer = 0

    def update(self, dt):
        if self.respawn_delay > 0:
            self.respawn_delay -= dt
            return

        is_frozen = self.freeze_timer > 0
        if is_frozen:
            self.freeze_timer -= dt

        self.arrows = [arrow for arrow in self.arrows if not self._is_out(arrow)]

        while len(self.arrows) < LIMITED_ARROWS:
            angle = random.uniform(0, 2 * math.pi)
            x = CENTER[0] + RADIUS * math.cos(angle)
            y = CENTER[1] + RADIUS * math.sin(angle)
            pos = pygame.Vector2(x, y)

            direction = (pygame.Vector2(CENTER) - pos).normalize()
            speed = random.randint(ARROW_MIN_SPEED, ARROW_MAX_SPEED)

            arrow = {
                "pos": pos,
                "dir": direction,
                "speed": speed
            }

            self.arrows.append(arrow)

        if not is_frozen:
            for arrow in self.arrows:
                arrow["pos"] += arrow["dir"] * arrow["speed"] * dt

    def draw(self, screen):
        for arrow in self.arrows:
            pygame.draw.circle(screen, (127, 127, 255), arrow["pos"], self.size / 2)
            # screen.blit(self.image, arrow["pos"])

    def check_collision(self, collider, shield_active=False):
        if shield_active:
            return False
        left, right, top, bottom = collider
        for arrow in self.arrows:
            if left < arrow["pos"].x < right and top < arrow["pos"].y < bottom:
                return True
        return False

    def _is_out(self, arrow):
        return arrow["pos"].distance_to(CENTER) > RADIUS

    def clear_all(self):
        self.arrows = []
        self.respawn_delay = 1.0

    def freeze(self, seconds):
        self.freeze_timer = seconds
