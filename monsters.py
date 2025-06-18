import pygame
import random
import math
import settings

class MonsterManger:
    def __init__(self):
        self.monsters = []
        self.size = settings.MONSTER_SIZE

        self.images = []
        # 프레임 나누기
        for i in range(1, 4):
            sheet = pygame.image.load(f"assets/monster{i}.png").convert_alpha()
            sheet_width = sheet.get_width()
            frame_width = sheet_width // 6
            height = sheet.get_height()
            frames = []
            for i in range(6):
                frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, height))
                frame = pygame.transform.scale(frame, (self.size, self.size))
                frames.append(frame)
            self.images.append(frames)

        # 모든 몬스터를 없애는 아이템에 사용할 값
        self.respawn_delay = 0
        # 모든 몬스터를 멈추하는 아이템에 사용할 값
        self.freeze_timer = 0
        # 몬스터를 천천히 움직이는 아이템에 사용할 값
        self.slow_timer = 0
        self.frame_delay = 0.5

    def update(self, dt):
        if self.respawn_delay > 0:
            self.respawn_delay -= dt
            return

        # 멈추거나 천천히 움직이는 중인지 확인
        is_frozen = self.freeze_timer > 0
        is_slown = self.slow_timer > 0

        if is_frozen:
            self.freeze_timer -= dt
        if is_slown:
            self.slow_timer -=dt

        self.monsters = [monster for monster in self.monsters if not self._is_out(monster)]

        while len(self.monsters) < settings.LIMITED_MONSTERS:
            # start direction
            direction = random.randint(0, 3)

            # north
            if direction == 0:
                dir = "north"
                x = random.randrange(0, settings.SCREEN_WIDTH)
                y = 0

            # east (오른쪽에서 왼쪽으로)
            elif direction == 1:
                dir = "east"
                x = settings.SCREEN_WIDTH
                y = random.randrange(0, settings.SCREEN_HEIGHT)

            # west (왼쪽에서 오른쪽으로)
            elif direction == 2:
                dir = "west"
                x = 0
                y = random.randrange(0, settings.SCREEN_HEIGHT)

            # south
            else:
                dir = "south"
                x = random.randrange(0, settings.SCREEN_WIDTH)
                y = settings.SCREEN_HEIGHT

            pos = pygame.Vector2(x, y)
            speed = random.randint(settings.MONSTER_MIN_SPEED, settings.MONSTER_MAX_SPEED)

            monsters = {
                "pos": pos,
                "dir": dir,
                "speed": speed,
                "frames": random.choice(self.images),
                "frame_index": 0,
                "frame_timer": 0
            }

            self.monsters.append(monsters)

        if not is_frozen:
            for monsters in self.monsters:
                # 난이도 반영된 기본 속도 계산
                actual_speed = monsters["speed"] * settings.SPEED_VALUE

                # 아이템 효과 반영
                if is_slown:
                    actual_speed *= 0.3

                if monsters["dir"] == "north":
                    monsters["pos"].y += actual_speed* dt

                elif monsters["dir"] == "east":
                    monsters["pos"].x -= actual_speed * dt

                elif monsters["dir"] == "west":
                    monsters["pos"].x += actual_speed * dt

                else:  # south
                    monsters["pos"].y -= actual_speed * dt


    def draw(self, screen):
        for monster in self.monsters:
            monster["frame_timer"] += 1
            if monster["frame_timer"] >= self.frame_delay * 60:
                monster["frame_timer"] = 0
                monster["frame_index"] = (monster["frame_index"] + 1) % len(monster["frames"])

            image = monster["frames"][monster["frame_index"]]

            if monster["dir"] == "east":
                image = pygame.transform.flip(image, True, False)

            screen.blit(image, image.get_rect(center=monster["pos"]))

    def check_collision(self, collider, shield_active=False):
        if shield_active:
            return False
        left, right, top, bottom = collider
        for monster in self.monsters:
            if left < monster["pos"].x < right and top < monster["pos"].y < bottom:
                return True
        return False

    def _is_out(self, monster):
        return (
                (monster["dir"] == "north" and monster["pos"].y > settings.SCREEN_HEIGHT) or
                (monster["dir"] == "south" and monster["pos"].y < 0) or
                (monster["dir"] == "east" and monster["pos"].x < 0) or
                (monster["dir"] == "west" and monster["pos"].x > settings.SCREEN_WIDTH)
        )

    def clear_all(self):
        self.monsters = []
        self.respawn_delay = 2.0

    def freeze(self, seconds):
        self.freeze_timer = seconds
    def slow_down(self, seconds):
        self.slow_timer = seconds