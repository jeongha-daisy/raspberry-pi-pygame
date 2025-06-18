import pygame
import time
import socket
import threading
import settings
from player import Player
from monsters import MonsterManger
from items import ItemManager


#====================================================================== NETWORK


# GPIO 값은 이벤트가 생길 때만 보내주고, Joystick 값은 지속적으로 보내주어야하므로 다른 포트에서 값을 전달
SERVER_IP = 'your ip address'
PORT = 9000
JOYSTICK_PORT = 5000

# 기존 게임용 소켓
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen(1)
print(f"Server listening on {SERVER_IP}:{PORT}")

# 조이스틱 소켓
joystick_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
joystick_socket.bind((SERVER_IP, JOYSTICK_PORT))
joystick_socket.listen(1)
print(f"Joystick server listening on {SERVER_IP}:{JOYSTICK_PORT}")

#====================================================================== NETWORK

# 게임 기본 세팅들
pygame.init()
pygame.mixer.init()
backgroundMusic = pygame.mixer.Sound('Itty_Bitty.mp3')
backgroundMusic.play(-1)
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

STATE_TITLE = 0
STATE_TUTORIAL_1 = 1
STATE_TUTORIAL_2 = 2
STATE_TUTORIAL_3 = 3
STATE_PLAY = 4
STATE_GAMEOVER = 5

#====================================================================== NETWORK

# 조이스틱 값 저장용 전역 변수
joystick_updown = 127
joystick_leftright = 127

# 센서 메시지 클라이언트 연결 수락
client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")
# 조이스틱 클라이언트 연결 수락
joystick_client_socket, joystick_client_address = joystick_socket.accept()
print(f"Joystick connected from {joystick_client_address}")

# gpio 값 핸들 함수
def handle_client_message():
    global running
    while running:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received: {message}")
                handle_message(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


last_used = {"shock": 0, "button": 0, "light": 0, "sound": 0}
COOLDOWN = 1.5  # 아이템 사용 후 1.5초간 다른 아이템 사용 못함

# 받은 값에 따라 아이템을 처리할 함수
def handle_message(message):
    global game_state, items, player, start_ticks
    now = time.time()
    if now - last_used.get(message, 0) < COOLDOWN:
        print("아이템 사용 가능 시간 안됨")
        return
    last_used[message] = now

    # 게임 전
    if game_state == STATE_TITLE:
        if message == "button":
            game_state = STATE_TUTORIAL_1
    elif game_state == STATE_TUTORIAL_1:
        if message == "button":
            game_state = STATE_TUTORIAL_2
    elif game_state == STATE_TUTORIAL_2:
        if message == "button":
            game_state = STATE_TUTORIAL_3
    elif game_state == STATE_TUTORIAL_3:
        if message == "button":
            start_ticks = pygame.time.get_ticks()
            game_state = STATE_PLAY

    # 게임 중 (아이템 처리)
    elif game_state == STATE_PLAY:
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
    elif game_state == STATE_GAMEOVER:
        if message == "button":
            # 게임 재시작 함수
            reset_game()
            game_state = STATE_PLAY
    else:
        pass

# joystick 값 핸들 함수
def handle_joystick_message():
    global running, joystick_updown, joystick_leftright
    while running:
        try:
            message = joystick_client_socket.recv(1024).decode('utf-8').strip()
            if message:
                # value1,value2로 넘겨줌
                parts = message.split(',')
                if len(parts) == 2:
                    value1_str, value2_str = parts
                    joystick_updown = int(value1_str)
                    joystick_leftright = int(value2_str)
                else:
                    print(f"Invalid joystick message format: {message}")
        except Exception as e:
            print(f"Error receiving joystick data: {e}")
            break

# 메시지 수신을 위한 스레드 실행
# 게임 중엔 while loop를 돌기 때문에 다중 스레드로 연결
threading.Thread(target=handle_client_message, daemon=True).start()
threading.Thread(target=handle_joystick_message, daemon=True).start()

#====================================================================== NETWORK

def reset_game():
    global player, monsters, items, score, level, start_ticks
    player = Player("assets/Swim.png", "assets/Swim2.png")
    monsters = MonsterManger()
    items = ItemManager()
    score = 0
    level = 0
    start_ticks = pygame.time.get_ticks()
    settings.SPEED_VALUE = 1


# 간단한 줄바꿈 출력 함수
def render_multiline(textFile, font, color, surface, center_y, line_height):
    with open(textFile, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()

    total_height = len(lines) * line_height
    start_y = center_y - total_height // 2

    for i, line in enumerate(lines):
        msg = font.render(line, True, color)
        msg_rect = msg.get_rect(center=(settings.CENTER[0], start_y + i * line_height))
        surface.blit(msg, msg_rect)

# 게임 시작
while running:
    screen.blit(bg_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 타이틀 화면
    if game_state == STATE_TITLE:
        title = titleFont.render("DODGE GAME", True, (255, 255, 255))
        line1 = textFont.render("PRESS BUTTON TO START", True, (255, 255, 255))

        title_rect = title.get_rect(center=(settings.CENTER[0], settings.CENTER[1] - 60))
        line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.CENTER[1] + 30))

        screen.blit(title, title_rect)
        screen.blit(line1, line1_rect)

    # 튜토리얼 1
    elif game_state == STATE_TUTORIAL_1:
        render_multiline("tutorial_text.txt", tutoFont, (255, 255, 255), screen, settings.CENTER[1], 60)
        line1 = textFont.render("PRESS BUTTON TO CONTINUE", True, (0, 0, 0))
        line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.SCREEN_HEIGHT - 100))
        screen.blit(line1, line1_rect)

    # 튜토리얼 2
    elif game_state == STATE_TUTORIAL_2:
        render_multiline("tutorial_text2.txt", tutoFont2, (255, 255, 255), screen, settings.CENTER[1], 60)
        line1 = textFont.render("PRESS BUTTON TO CONTINUE", True, (0, 0, 0))
        line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.SCREEN_HEIGHT - 100))
        screen.blit(line1, line1_rect)

    # 튜토리얼 3
    elif game_state == STATE_TUTORIAL_3:
        render_multiline("tutorial_text3.txt", tutoFont, (255, 255, 255), screen, settings.CENTER[1], 60)
        line1 = textFont.render("PRESS BUTTON TO START", True, (0, 0, 0))
        line1_rect = line1.get_rect(center=(settings.CENTER[0], settings.SCREEN_HEIGHT - 100))
        screen.blit(line1, line1_rect)

    # 게임 중
    elif game_state == STATE_PLAY:
        score = int((pygame.time.get_ticks() - start_ticks) / 1000)

        # 점수가 10의 배수가 될 때마다 속도를 올린다.
        if score // 10 > level:
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
        player.move(clock.get_time() / 1000, joystick=[joystick_updown, joystick_leftright])
        player.draw(screen)

        # 충돌 검사 시 쉴드 반영
        if monsters.check_collision(player.get_collider(), shield_active=(player.shield_timer > 0)):
            game_state = STATE_GAMEOVER
        if items.check_collision(player.get_collider()):
            print("아이템 먹음")

        # 센서 인식 UI 그리기 (사용 중인 아이템으로 구분)
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

    # 게임오버
    elif game_state == STATE_GAMEOVER:
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

# 소켓 연결 종료
client_socket.close()
server_socket.close()
joystick_client_socket.close()
joystick_socket.close()

pygame.mixer.quit()
pygame.quit()