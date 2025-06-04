import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ARROW_MIN_SPEED, ARROW_MAX_SPEED, LIMITED_ARROWS

class ArrowManager:
    def __init__(self, image_path):
        self.arrows = []
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))

    def update(self, dt):
        self.arrows = [a for a in self.arrows if not self._is_out(a)]

        while len(self.arrows) < LIMITED_ARROWS:
            direction = random.randint(0, 3)
            speed = random.randint(ARROW_MIN_SPEED, ARROW_MAX_SPEED)
            if direction == 0:  # top
                pos = pygame.Vector2(random.randint(0, SCREEN_WIDTH), 0)
            elif direction == 1:  # right
                pos = pygame.Vector2(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT))
            elif direction == 2:  # bottom
                pos = pygame.Vector2(random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT)
            else:  # left
                pos = pygame.Vector2(0, random.randint(0, SCREEN_HEIGHT))
            self.arrows.append([pos, speed, direction])

        for arrow in self.arrows:
            if arrow[2] == 0: arrow[0].y += arrow[1] * dt
            elif arrow[2] == 1: arrow[0].x -= arrow[1] * dt
            elif arrow[2] == 2: arrow[0].y -= arrow[1] * dt
            else: arrow[0].x += arrow[1] * dt

    def draw(self, screen):
        for arrow in self.arrows:
            screen.blit(self.image, arrow[0])

    # 부딪혔는지 확인하는 메서드
    def check_collision(self, collider):
        left, right, top, bottom = collider
        for arrow in self.arrows:
            if left < arrow[0].x < right and top < arrow[0].y < bottom:
                return True
        return False

    def _is_out(self, arrow):
        x, y = arrow[0].x, arrow[0].y
        return x < 0 or x > SCREEN_WIDTH or y < 0 or y > SCREEN_HEIGHT
