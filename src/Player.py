import pygame
from src.Const import LANES, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_Y, BLUE, BLACK

class Player:
    def __init__(self):
        self.lane = 1
        self.rect = pygame.Rect(
            LANES[self.lane] - PLAYER_WIDTH // 2,
            PLAYER_Y,
            PLAYER_WIDTH,
            PLAYER_HEIGHT
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
        self.rect.x = LANES[self.lane] - PLAYER_WIDTH // 2

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, (self.rect.x + 8, self.rect.y + 10, 34, 20), border_radius=5)
        pygame.draw.rect(screen, BLACK, (self.rect.x + 8, self.rect.y + 60, 12, 20), border_radius=4)
        pygame.draw.rect(screen, BLACK, (self.rect.x + 30, self.rect.y + 60, 12, 20), border_radius=4)