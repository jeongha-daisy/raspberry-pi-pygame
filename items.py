import pygame
import random
import math
from settings import *

class ItemManager:
    # 이니셜라이즈
    def __init__(self):
        self.items = []
        self.collected_items = []
        self.size = ARROW_SIZE
        # self.image = pygame.image.load(image_path).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def update(self, dt):
        # 원 안에 있는 화살만 다시 만든다.
        self.items = [a for a in self.items if not self._is_out(a) and not a[4]]

        while len(self.items) < LIMITED_ITEMS:
            # RADIUS를 반지름으로 갖는 원 테투리 위의 랜덤한 좌표 생성
            # 랜덤한 각도 생성
            angle = random.uniform(0, 2 * math.pi)
            # 그 각도에서의 x, y 좌표 구하기
            x = CENTER[0] + RADIUS * math.cos(angle)
            y = CENTER[1] + RADIUS * math.sin(angle)
            pos = pygame.Vector2(x, y)

            # 센터를 중심으로 벡터 구한다.
            direction = (pygame.Vector2(CENTER) - pos).normalize()      # 방향만 기억하면 되므로 normalize한다.

            # 최대 속도와 최저 속도 내에서 랜덤한 속도
            speed = random.randint(ARROW_MIN_SPEED, ARROW_MAX_SPEED)

            index = random.randrange(1, 7)

            self.items.append([pos, direction, speed, index, False])

        # 상하좌우가 아닌 생성된 방향으로 이동한다.
        for item in self.items:
            item[0] += item[1] * item[2] * dt  # pos += direction * speed * dt

    # 화면에 그리는 메서드
    def draw(self, screen):
        for item in self.items:
            # screen.blit(self.image, arrow[0])
            if item[3] == 1:
                pygame.draw.circle(screen, (255, 127, 127), item[0], self.size / 2)
            elif item[3] == 2:
                pygame.draw.circle(screen, (255, 185, 127), item[0], self.size / 2)
            elif item[3] == 3:
                pygame.draw.circle(screen, (255, 255, 127), item[0], self.size / 2)
            elif item[3] == 4:
                pygame.draw.circle(screen, (127, 255, 127), item[0], self.size / 2)
            elif item[3] == 5:
                pygame.draw.circle(screen, (255, 127, 255), item[0], self.size / 2)
            elif item[3] == 6:
                pygame.draw.circle(screen, (127, 127, 127), item[0], self.size / 2)

    # 부딪혔는지 확인하는 메서드
    def check_collision(self, collider):
        left, right, top, bottom = collider
        for item in self.items:
            if left < item[0].x < right and top < item[0].y < bottom and len(self.collected_items) < 3:
                item[4] = True
                self.collected_items.append(item)
                print("아이템 먹음", len(self.collected_items))
                return True
        return False

    # 화면 밖으로 나갔는지 확인하는 메서드
    def _is_out(self, item):
        # 중심으로부터 거리가 반지름 이상인지
        return item[0].distance_to(CENTER) > RADIUS

    def use_item(self, key):
        key_to_index = {
            pygame.K_1: 1,
            pygame.K_2: 2,
            pygame.K_3: 3,
            pygame.K_4: 4,
            pygame.K_5: 5,
            pygame.K_6: 6,
        }

        if key in key_to_index:
            item_num = key_to_index[key]
            for item in self.collected_items:
                if item[3] == item_num:
                    print(f"아이템 {item_num} 사용")
                    self.collected_items.remove(item)
                    return item_num # 하나만 사용하고 종료

    def draw_collection(self, screen):
        x = 20
        y = SCREEN_HEIGHT - 20

        gap = self.size + 10  # 아이템 간 간격

        for i, item in enumerate(self.collected_items):
            pos = pygame.Vector2(x + i * gap, y)

            color = (255, 255, 255)
            if item[3] == 1:
                color = (255, 127, 127)
            elif item[3] == 2:
                color = (255, 185, 127)
            elif item[3] == 3:
                color = (255, 255, 127)
            elif item[3] == 4:
                color = (127, 255, 127)
            elif item[3] == 5:
                color = (255, 127, 255)
            elif item[3] == 6:
                color = (127, 127, 127)

            pygame.draw.circle(screen, color, pos, self.size / 2)