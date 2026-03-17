import os
import pygame
from src.Const import (
    LANES,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_Y,
    IMAGES_DIR
)


class Player:
    def __init__(self):
        self.current_lane = 1
        self.target_lane = 1
        self.move_speed = 12

        self.image = self.load_sprite("player_car.png", PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect = self.image.get_rect(
            center=(LANES[self.current_lane], PLAYER_Y + PLAYER_HEIGHT // 2)
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
        if self.target_lane > 0:
            self.target_lane -= 1

    def move_right(self):
        if self.target_lane < 2:
            self.target_lane += 1

    def update(self):
        target_x = LANES[self.target_lane]

        if self.rect.centerx < target_x:
            self.rect.centerx += self.move_speed
            if self.rect.centerx > target_x:
                self.rect.centerx = target_x

        elif self.rect.centerx > target_x:
            self.rect.centerx -= self.move_speed
            if self.rect.centerx < target_x:
                self.rect.centerx = target_x

        if self.rect.centerx == target_x:
            self.current_lane = self.target_lane

    def draw(self, screen):
        screen.blit(self.image, self.rect)