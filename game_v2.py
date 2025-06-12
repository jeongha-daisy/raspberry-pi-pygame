import pygame
import socket
import pygame
import threading

from settings import *
from player import Player
from monsters import MonsterManger
from items import ItemManager

SERVER_IP = '10.125.126.208'
PORT = 9000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((SERVER_IP, PORT))
server_socket.listen(1)
print(f"Server listening on {SERVER_IP}:{PORT}")

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

# 서버 연결 수락
client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

# got message from sensor
def handle_client_message():
    # 딕셔너리로 수정하면 좋을 것 같음
    # message = {
    #   "type": "button"
    #   "value": true
    # }

    # message = {
    #   "type": "joystick"
    #   "value": [110, 220]
    # }

    while running:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received: {message}")
                #if message.type == "joystick":
                    # player.move(dt=clock.get_time() / 1000, joystick=joystick_data)
                handle_message(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# handle a message from sensor (button, sound, light, shock)
def handle_message(message):
    global game_state, items, arrows, player

    # message에 해당하는 item을 가지고 있어야만 item을 사용할 수 있다.
    # use_item은 message에 해당하는 item을 가지고 있는지 확인한다.
    used_item = items.use_item(message)

    if used_item == "button":
        print("press_detected: Freeze obstacle")
        monsters.freeze(2)
    elif used_item == "sound":
        monsters.slow_down(2.0)
    elif used_item == "light":
        print("dark_detected: Shield")
        player.activate_shield(3.0)
    elif used_item == "shock":
        print("shock_detected: Destroy obstacle (Clear All)")
        monsters.clear_all()

# 메시지 수신을 위한 스레드 실행
threading.Thread(target=handle_client_message, daemon=True).start()

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
        player.move(clock.get_time() / 1000, keys=keys)
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

# 소켓 연결 종료
client_socket.close()
server_socket.close()
pygame.quit()
