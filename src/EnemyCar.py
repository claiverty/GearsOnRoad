import pygame
import random
from src.Const import LANES, ENEMY_WIDTH, ENEMY_HEIGHT, RED, BLACK, HEIGHT

class EnemyCar:
    def __init__(self):
        lane = random.randint(0, 2)
        self.rect = pygame.Rect(
            LANES[lane] - ENEMY_WIDTH // 2,
            -ENEMY_HEIGHT,
            ENEMY_WIDTH,
            ENEMY_HEIGHT
        )

    def update(self, speed):
        self.rect.y += speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, (self.rect.x + 8, self.rect.y + 10, 34, 20), border_radius=5)
        pygame.draw.rect(screen, BLACK, (self.rect.x + 8, self.rect.y + 60, 12, 20), border_radius=4)
        pygame.draw.rect(screen, BLACK, (self.rect.x + 30, self.rect.y + 60, 12, 20), border_radius=4)

    def off_screen(self):
        return self.rect.y > HEIGHT