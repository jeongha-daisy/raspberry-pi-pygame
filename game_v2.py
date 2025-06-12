import pygame
from pygame.examples.grid import TITLE

import settings
from player import Player
from monsters import MonsterManger
from items import ItemManager

pygame.init()
pygame.mixer.init()
shootSound = pygame.mixer.Sound('Itty_Bitty.mp3')
shootSound.play()
global player, monsters, items, score, start_ticks, level

screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
clock = pygame.time.Clock()
textFont = pygame.font.Font("assets/editundo.ttf", 30)
tutoFont = pygame.font.Font("assets/neodgm.ttf", 30)
tutoFont2 = pygame.font.Font("assets/neodgm.ttf", 20)
titleFont = pygame.font.Font("assets/editundo.ttf", 70)

player = Player("assets/Swim.png", "assets/Swim2.png")
monsters = MonsterManger()
items = ItemManager()
bg_image = pygame.image.load("assets/background_img.png")
bg_image = pygame.transform.scale(bg_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

running = True
game_state = 0
score = 0
level = 0
start_ticks = pygame.time.get_ticks()


# 간단한 줄바꿈 출력 함수
def render_multiline(textFile, font, color, surface, center_y, line_height):
    with open(textFile, "r") as file:
        lines = file.read().splitlines()

    total_height = len(lines) * line_height
    start_y = center_y - total_height // 2

    for i, line in enumerate(lines):
        msg = font.render(line, True, color)
        msg_rect = msg.get_rect(center=(settings.CENTER[0], start_y + i * line_height))
        surface.blit(msg, msg_rect)

while running:
    screen.blit(bg_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            used_item = items.use_item(event.key)
            if used_item == "button":
                monsters.freeze(2)
            elif used_item == "sound":
                monsters.slow_down(2.0)
            elif used_item == "light":
                player.activate_shield(3.0)
            elif used_item == "shock" :
                monsters.clear_all()

            if event.key == pygame.K_k:
                if game_state == 0:
                    game_state = 1
                elif game_state == 1:
                    game_state = 2
                elif game_state == 2:
                    game_state = 3
                elif game_state == 3:
                    start_ticks = pygame.time.get_ticks()
                    game_state = 4
                elif game_state == 4:
                    game_state = 5
                elif game_state == 5:
                    score = 0
                    level = 0
                    start_ticks = pygame.time.get_ticks()
                    player = Player("assets/Swim.png", "assets/Swim2.png")
                    monsters = MonsterManger()
                    items = ItemManager()
                    settings.SPEED_VALUE = 1

                    game_state = 4
                    pass


    keys = pygame.key.get_pressed()

    if game_state == 0:
        title = titleFont.render("DODGE GAME", True, (255, 255, 255))
        line1 = textFont.render("PRESS BUTTON TO START", True, (255, 255, 255))

        title_rect = title.get_rect(center=(settings.CENTER[0], settings.CENTER[1] - 60))
        line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.CENTER[1] + 30))

        screen.blit(title, title_rect)
        screen.blit(line1, line1_rect)


    elif game_state == 1:
        render_multiline("tutorial_text.txt", tutoFont, (255, 255, 255), screen, settings.CENTER[1], 60)
        line1 = textFont.render("PRESS BUTTON TO CONTINUE", True, (0, 0, 0))
        line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.SCREEN_HEIGHT - 100))
        screen.blit(line1, line1_rect)

    elif game_state == 2:
        render_multiline("tutorial_text2.txt", tutoFont2, (255, 255, 255), screen, settings.CENTER[1], 60)
        line1 = textFont.render("PRESS BUTTON TO CONTINUE", True, (0, 0, 0))
        line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.SCREEN_HEIGHT - 100))
        screen.blit(line1, line1_rect)

    elif game_state == 3:
        render_multiline("tutorial_text3.txt", tutoFont, (255, 255, 255), screen, settings.CENTER[1], 60)
        line1 = textFont.render("PRESS BUTTON TO START", True, (0, 0, 0))
        line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.SCREEN_HEIGHT - 100))
        screen.blit(line1, line1_rect)

    elif game_state == 4:
        score = int((pygame.time.get_ticks() - start_ticks) / 1000)

        if score // 10 > level:
            print("속도 올리기", settings.SPEED_VALUE, settings.MONSTER_MIN_SPEED, settings.MONSTER_MAX_SPEED)
            settings.SPEED_VALUE += 0.1
            settings.SPEED_VALUE = round(settings.SPEED_VALUE, 1)
            level = score // 10

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

        # 충돌 검사 시 쉴드 반영
        if monsters.check_collision(player.get_collider(), shield_active=(player.shield_timer > 0)):
            game_state = 5
        if items.check_collision(player.get_collider()):
            print("아이템 먹음")

        if monsters.freeze_timer > 0:
            line1 = textFont.render("button detected!", True, (255, 255, 255))
            line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.CENTER[1]))
            screen.blit(line1, line1_rect)
        if monsters.slow_timer > 0:
            line1 = textFont.render("sound sensor detected!", True, (255, 255, 255))
            line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.CENTER[1]))
            screen.blit(line1, line1_rect)
        if player.shield_timer > 0:
            line1 = textFont.render("light sensor detected!", True, (255, 255, 255))
            line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.CENTER[1]))
            screen.blit(line1, line1_rect)
        if monsters.respawn_delay > 0:
            line1 = textFont.render("shock sensor detected!", True, (255, 255, 255))
            line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.CENTER[1]))
            screen.blit(line1, line1_rect)

        # 점수 그리기
        startText = textFont.render(str(score), True, (0, 0, 0))
        text_rect = startText.get_rect()

        # 왼쪽 하단으로 위치 지정
        padding = 20
        text_rect.topleft = (settings.SCREEN_WIDTH - text_rect.width - padding, settings.SCREEN_HEIGHT - text_rect.height - padding)

        screen.blit(startText, text_rect)

    elif game_state == 5:
        line1 = textFont.render(f"GAME OVER SCORE: {score}", True, (255, 255, 255))
        line2 = textFont.render("PRESS BUTTON TO RESTART", True, (255, 255, 255))

        line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.CENTER[1] - 30))
        line2_rect = line2.get_rect(center=(settings.CENTER[0], settings.CENTER[1] + 30))

        screen.blit(line1, line1_rect)
        screen.blit(line2, line2_rect)

    else:
        pass

    # 다시 그리기
    pygame.display.flip()
    clock.tick(60)

pygame.mixer.quit()
pygame.quit()
