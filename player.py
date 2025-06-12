import pygame
# import smbus
from settings import PLAYER_SIZE, PLAYER_SPEED, CENTER, SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    # 이니셜라이즈
    def __init__(self, image_path, image_path2):
        self.pos = pygame.Vector2(CENTER[0], CENTER[1])
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED

        # self.image = pygame.transform.scale(self.image, (self.size, self.size))

        # 프레임 나누기
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image2 = pygame.image.load(image_path2).convert_alpha()

        self.direction = "right"
        sheet_width = self.image.get_width()
        sheet_height = self.image.get_height()
        frame_count = 6
        frame_width = sheet_width // frame_count

        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 0.5

        self.frames_horizontal = []
        self.frames_vertical = []

        for i in range(frame_count):
            frame = self.image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, sheet_height))
            frame = pygame.transform.scale(frame, (self.size, self.size))
            self.frames_horizontal.append(frame)
        for i in range(frame_count):
            frame = self.image2.subsurface(pygame.Rect(i * frame_width, 0, frame_width, sheet_height))
            frame = pygame.transform.scale(frame, (self.size, self.size))
            self.frames_vertical.append(frame)

        self.shield_timer = 0
        self.shield_radius = self.size * 2  # 시각적 쉴드 반지름
        self.shield_image = pygame.image.load("assets/shield.png").convert_alpha()
        self.shield_image = pygame.transform.scale(self.shield_image, (self.shield_radius, self.shield_radius))

        self.address = 0x48
        self.A0 = 0x40
        self.A1 = 0x41
        # self.bus = smbus.SMBus(1)

    # 움직임 메서드
    def move(self, keys, dt):
        if self.shield_timer > 0:
            self.shield_timer -= dt
        delta = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            delta.y -= self.speed * dt
            self.direction = "up"
        if keys[pygame.K_s]:
            delta.y += self.speed * dt
            self.direction = "down"
        if keys[pygame.K_a]:
            delta.x -= self.speed * dt
            self.direction = "left"
        if keys[pygame.K_d]:
            delta.x += self.speed * dt
            self.direction = "right"

        new_pos = self.pos + delta
        # 화면 밖으로 못나가게 clamp
        new_x = max(0, min(SCREEN_WIDTH, new_pos.x))
        new_y = max(0, min(SCREEN_HEIGHT, new_pos.y))
        self.pos = pygame.Vector2(new_x, new_y)

        """
        bus.write_byte(address, A0)
        time.sleep(0.01)
        value1 = bus.read_byte(address)

        bus.write_byte(address, A1)
        time.sleep(0.01)
        value2 = bus.read_byte(address)
        
        delta = pygame.Vector2(0, 0)

        if value1 < 100 and player_pos.x > (0 - player_size / 2):
            print("left")
            delta.x -= self.speed * dt
        if value1 > 220 and player_pos.x < (width - player_size / 2):
            print("right")
            delta.x += self.speed * dt
        if value2 < 100 and player_pos.y > (0 - player_size / 2):
            print("up")
            delta.y -= self.speed * dt
        if value2 > 220 and player_pos.y < (height - player_size / 2):
            print("down")
            delta.y += self.speed * dt
        
        new_pos = self.pos + delta
        if new_pos.distance_to(CENTER) <= RADIUS:
            self.pos = new_pos
        """
        self.update_animation(dt)

    def update_animation(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames_horizontal)

    # 화면에 그리기
    def draw(self, screen):
        draw_pos = self.pos - pygame.Vector2(self.size / 2, self.size / 2)

        # pygame.draw.circle(screen, (127, 127, 127), draw_pos, self.size / 2)

        if self.shield_timer > 0:
            draw_shield_pos = self.pos - pygame.Vector2(self.shield_radius / 2, self.shield_radius / 2)
            screen.blit(self.shield_image, draw_shield_pos)
        if self.direction in ["left", "right"]:
            image = self.frames_horizontal[self.current_frame]
            if self.direction == "left":
                image = pygame.transform.flip(image, True, False)
        else:
            image = self.frames_vertical[self.current_frame]
            if self.direction == "down":
                image = pygame.transform.flip(image, False, True)

        screen.blit(image, draw_pos)

    # 콜라이더 각 좌표 반환 (네모 상자)
    def get_collider(self):
        return (
            self.pos.x - self.size / 2, self.pos.x + self.size / 2,
            self.pos.y - self.size / 2, self.pos.y + self.size / 2
        )

    def activate_shield(self, duration):
        self.shield_timer = duration  # 예: 2.0초