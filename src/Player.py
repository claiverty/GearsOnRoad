import os
import pygame
from src.Const import (
    LANES,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_Y,
    IMAGES_DIR,
    BLACK
)


class Player:
    def __init__(self):
        self.lane = 1
        self.image = self.load_sprite("player_car.png", PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect = self.image.get_rect(
            center=(LANES[self.lane], PLAYER_Y + PLAYER_HEIGHT // 2)
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

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.update_position()

    def move_right(self):
        if self.lane < 2:
            self.lane += 1
            self.update_position()

    def update_position(self):
        self.rect.centerx = LANES[self.lane]

    def draw(self, screen):
        screen.blit(self.image, self.rect)