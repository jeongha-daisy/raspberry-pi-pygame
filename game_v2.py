import pygame
from settings import *
from player import Player
from monsters import MonsterManger
from items import ItemManager

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
textFont = pygame.font.SysFont(None, 50)

player = Player("assets/Swim.png", "assets/Swim2.png")
monsters = MonsterManger()
items = ItemManager()
bg_image = pygame.image.load("assets/background.png")
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

running = True
game_state = 1
score = 0
start_time = pygame.time.get_ticks()

while running:
    screen.blit(bg_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            used_item = items.use_item(event.key)
            if used_item == "button":
                print("장애물 파괴")
                monsters.clear_all()
            elif used_item == "sound":
                print("장애물 멈춤")
                monsters.freeze(2)
            elif used_item == "shock" or used_item == "light":
                print("쉴드 생성")
                player.activate_shield(3.0)

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
        monsters.update(clock.get_time() / 1000)
        monsters.draw(screen)

        # 아이템 그리기
        items.update(clock.get_time() / 1000)
        items.draw(screen)

        # 가지고 있는 아이템 그리기
        items.draw_collection(screen)

        # 플레이어 그리기
        player.move(keys, clock.get_time() / 1000)
        player.draw(screen)

        # 맵 그리기
        pygame.draw.circle(screen, (0, 0, 0), (int(CENTER[0]), int(CENTER[1])), int(RADIUS), 2)

        # 충돌 검사 시 쉴드 반영
        if monsters.check_collision(player.get_collider(), shield_active=(player.shield_timer > 0)):
            print("닿음")
            # game_state = 2
        if items.check_collision(player.get_collider()):
            print("아이템 먹음")

        # 점수 그리기
        startText = textFont.render(str(score), True, (0, 0, 0))
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
