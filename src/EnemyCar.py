import os
import random
import pygame
from src.Const import (
    LANES,
    ENEMY_WIDTH,
    ENEMY_HEIGHT,
    HEIGHT,
    IMAGES_DIR
)


class EnemyCar:
    def __init__(self):
        self.lane = random.randint(0, 2)

        self.sprite_options = [
            ("enemy_car.png", ENEMY_WIDTH, ENEMY_HEIGHT),
            ("enemy_taxi.png", ENEMY_WIDTH, ENEMY_HEIGHT),
            ("enemy_police.png", ENEMY_WIDTH, ENEMY_HEIGHT),
            ("enemy_blackcar.png", ENEMY_WIDTH, ENEMY_HEIGHT),
            ("enemy_pickup.png", ENEMY_WIDTH, ENEMY_HEIGHT + 8),
        ]

        filename, width, height = random.choice(self.sprite_options)
        self.image = self.load_sprite(filename, width, height)

        self.rect = self.image.get_rect(
            center=(LANES[self.lane], -height // 2)
        )

    def load_sprite(self, filename, width, height):
        path = os.path.join(IMAGES_DIR, filename)
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.smoothscale(image, (width, height))
        return image

    def get_hitbox(self):
        hitbox_width = int(self.rect.width * 0.60)
        hitbox_height = int(self.rect.height * 0.82)

        return pygame.Rect(
            self.rect.centerx - hitbox_width // 2,
            self.rect.centery - hitbox_height // 2,
            hitbox_width,
            hitbox_height
        )

    def update(self, speed):
        self.rect.y += speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.top > HEIGHT