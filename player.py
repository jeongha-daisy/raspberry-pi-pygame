import pygame
from settings import PLAYER_SIZE, PLAYER_SPEED, CENTER, RADIUS

class Player:
    # 이니셜라이즈
    def __init__(self, image_path):
        self.pos = pygame.Vector2(CENTER[0], CENTER[1])
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    # 움직임 메서드
    def move(self, keys, dt):
        delta = pygame.Vector2(0, 0)
        if keys[pygame.K_w]: delta.y -= self.speed * dt
        if keys[pygame.K_s]: delta.y += self.speed * dt
        if keys[pygame.K_a]: delta.x -= self.speed * dt
        if keys[pygame.K_d]: delta.x += self.speed * dt

        new_pos = self.pos + delta
        if new_pos.distance_to(CENTER) <= RADIUS:
            self.pos = new_pos

    # 화면에 그리기
    def draw(self, screen):
        draw_pos = self.pos - pygame.Vector2(self.size / 2, self.size / 2)
        screen.blit(self.image, draw_pos)

    # 콜라이더 각 좌표 반환 (네모 상자)
    def get_collider(self):
        return (
            self.pos.x - self.size / 2, self.pos.x + self.size / 2,
            self.pos.y - self.size / 2, self.pos.y + self.size / 2
        )
