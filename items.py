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
            # start direction
            direction = random.randint(0, 3)

            # north
            if direction == 0:
                dir = "north"
                x = random.randrange(0, SCREEN_WIDTH)
                y = 0

            # east (오른쪽에서 왼쪽으로)
            elif direction == 1:
                dir = "east"
                x = SCREEN_WIDTH
                y = random.randrange(0, SCREEN_HEIGHT)

            # west (왼쪽에서 오른쪽으로)
            elif direction == 2:
                dir = "west"
                x = 0
                y = random.randrange(0, SCREEN_HEIGHT)

            # south
            else:
                dir = "south"
                x = random.randrange(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT

            pos = pygame.Vector2(x, y)
            speed = random.randint(MONSTER_MIN_SPEED, MONSTER_MAX_SPEED)
            item_type = random.choice(self.item_types)

            item = {
                "pos": pos,
                "dir": dir,
                "speed": speed,
                "type": item_type,
                "collected": False
            }

            self.items.append(item)

        for item in self.items:
            if item["dir"] == "north":
                item["pos"].y += item["speed"] * dt

            elif item["dir"] == "east":
                item["pos"].x -= item["speed"] * dt

            elif item["dir"] == "west":
                item["pos"].x += item["speed"] * dt

            else:
                item["pos"].y -= item["speed"] * dt

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
        return (
                (item["dir"] == "north" and item["pos"].y > SCREEN_HEIGHT) or
                (item["dir"] == "south" and item["pos"].y < 0) or
                (item["dir"] == "east" and item["pos"].x < 0) or
                (item["dir"] == "west" and item["pos"].x > SCREEN_WIDTH)
        )

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
