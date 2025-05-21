# Example file showing a circle moving on screen
import pygame
import random

pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

dt = 0
ground_height = 40
player_size = 50
arrow_size = 20
arrow_list = []
running = True

# 중앙에서 시작하는 플레이어
player_pos = pygame.Vector2(width / 2, height - (ground_height + player_size))

# 이미지 불러오기
arrow_image = pygame.image.load("assets/pearl.png").convert_alpha()
arrow_image = pygame.transform.scale(arrow_image, (arrow_size, arrow_size))

player_image = pygame.image.load("assets/dave_front.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (player_size, player_size))

while running:
    # 종료 조건
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경 색
    screen.fill("#c9c9c9")

    # 플레이어 그리기
    screen.blit(player_image, player_pos)


    # ========
    # 화살 그리기
    for arrow in arrow_list:
        # 바닥에 닿았으면 리스트에서 제거하기
        if arrow[0].y > height - ground_height:
            arrow_list.remove(arrow)

    # 10개 이하라면 또 추가
    if len(arrow_list) < 10:
        # 랜덤한 위치와 속도를 arrow 리스트에 넣는다.
        arrowX = random.randrange(0, width)
        speed = random.randrange(100, 300)
        arrow_list.append([pygame.Vector2(arrowX, 0), speed])


    # 화살 그리기 및 이동
    for arrow in arrow_list:
        screen.blit(arrow_image, arrow[0])
        arrow[0].y += arrow[1] * dt
    # ========


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
