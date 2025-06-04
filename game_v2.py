import pygame
from settings import *
from player import Player
from arrows import ArrowManager

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
textFont = pygame.font.SysFont(None, 50)

player = Player("assets/dave_front.png")
arrows = ArrowManager("assets/pearl.png")

running = True
game_state = 1
score = 0
start_time = pygame.time.get_ticks()

while running:
    screen.fill("#ffe8f2")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_state == 0:
        startText = textFont.render("PRESS K TO START", True, (255, 255, 255))
        text_rect = startText.get_rect(center=(CENTER[0],CENTER[1]))
        screen.blit(startText, text_rect)

        if keys[pygame.K_k]:
            game_state = 1
            start_ticks = pygame.time.get_ticks()

    elif game_state == 1:
        score = int((pygame.time.get_ticks() - start_time) / 1000)

        # 화살 그리기
        arrows.update(clock.get_time() / 1000)
        arrows.draw(screen)

        # 플레이어 그리기
        player.move(keys, clock.get_time() / 1000)
        player.draw(screen)

        # 맵 그리기
        pygame.draw.circle(screen, (200, 200, 200), (int(CENTER[0]), int(CENTER[1])), int(RADIUS), 2)

        if arrows.check_collision(player.get_collider()):
            print("닿음")
            # game_state = 2

        # 점수 그리기
        startText = textFont.render(str(score), True, (255, 255, 255))
        text_rect = startText.get_rect(center=(CENTER[0], CENTER[1]))
        screen.blit(startText, text_rect)

    elif game_state == 2:
        endText = textFont.render(f"GAME OVER SCORE: {score} press K to restart", True, (255, 255, 255))
        text_rect = endText.get_rect(center=(CENTER[0], CENTER[1]))
        screen.blit(endText, text_rect)

    else:
        pass

    # 다시 그리기
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
