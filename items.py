import pygame
import random
import math
from settings import *

class ItemManager:
    def __init__(self):
        self.items = []
        self.collected_items = []
        self.size = ITEM_SIZE

        self.item_types = ["button", "sound", "shock", "light"]
        self.images = {}
        for name in self.item_types:
            image = pygame.image.load(f"assets/{name}.PNG").convert_alpha()
            image = pygame.transform.scale(image, (self.size, self.size))
            self.images[name] = image

    def update(self, dt):
        self.items = [item for item in self.items if not self._is_out(item) and not item["collected"]]

        while len(self.items) < LIMITED_ITEMS:
            # start side
            # 1: left, -1: right
            start_side = random.choice([-1, 1])
            if start_side == 1:
                x = 0
                y = random.uniform(0, SCREEN_HEIGHT)
            else:
                x = SCREEN_WIDTH
                y = random.uniform(0, SCREEN_HEIGHT)

            pos = pygame.Vector2(x, y)
            speed = random.randint(MONSTER_MIN_SPEED, MONSTER_MAX_SPEED)
            item_type = random.choice(self.item_types)

            item = {
                "pos": pos,
                "side": start_side,
                "speed": speed,
                "type": item_type,
                "collected": False
            }

            self.items.append(item)

        for item in self.items:
            item["pos"].x += item["side"] * item["speed"] * dt

    def draw(self, screen):
        for item in self.items:
            screen.blit(self.images[item["type"]], item["pos"])

    def check_collision(self, collider):
        left, right, top, bottom = collider
        for item in self.items:
            if left < item["pos"].x < right and top < item["pos"].y < bottom and len(self.collected_items) < 3:
                item["collected"] = True
                self.collected_items.append(item)
                print("아이템 먹음", len(self.collected_items))
                return True
        return False

    def _is_out(self, item):
        return item["pos"].x < 0 or item["pos"].x > SCREEN_WIDTH

    def use_item(self, key):
        key_map = {
            pygame.K_1: "button",
            pygame.K_2: "sound",
            pygame.K_3: "shock",
            pygame.K_4: "light",
        }

        if key in key_map:
            target_type = key_map[key]
            for item in self.collected_items:
                if item["type"] == target_type:
                    print(f"아이템 {target_type} 사용")
                    self.collected_items.remove(item)
                    return target_type

    def draw_collection(self, screen):
        x = 20
        y = SCREEN_HEIGHT - 20
        gap = self.size + 10

        for i, item in enumerate(self.collected_items):
            pos = pygame.Vector2(x + i * gap, y)
            screen.blit(self.images[item["type"]], pos)
