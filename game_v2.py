# Example file showing a circle moving on screen
import pygame

pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

dt = 0
ground_height = 40
player_size = 20
running = True

# 중앙에서 시작하는 플레이어
player_pos = pygame.Vector2(width / 2, height - (ground_height + player_size))

while running:
    # 종료 조건
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경 색
    screen.fill("#c9c9c9")

    # 플레이어 그리기
    pygame.draw.circle(screen, "black", player_pos, player_size)

    # 땅 그리기
    pygame.draw.rect(screen, (255, 255, 255), (0, height - ground_height, width, ground_height))

    # 움직임 제어
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_pos.x > 0:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d] and player_pos.x < width:
        player_pos.x += 300 * dt

    # 다시 그리기
    pygame.display.flip()

    # 프레임 속도
    dt = clock.tick(60) / 1000

pygame.quit()
