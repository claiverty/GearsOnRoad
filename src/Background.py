import pygame
from src.Const import (
    HEIGHT, GREEN, GRAY, WHITE, YELLOW,
    ROAD_X, ROAD_WIDTH, LANE_WIDTH, LINE_HEIGHT, LINE_GAP
)

class Background:
    def __init__(self):
        self.line_offset = 0

    def update(self, speed):
        self.line_offset += speed
        if self.line_offset >= LINE_HEIGHT + LINE_GAP:
            self.line_offset = 0

    def draw(self, screen):
        screen.fill(GREEN)

        pygame.draw.rect(screen, GRAY, (ROAD_X, 0, ROAD_WIDTH, HEIGHT))

        pygame.draw.line(screen, WHITE, (ROAD_X, 0), (ROAD_X, HEIGHT), 5)
        pygame.draw.line(screen, WHITE, (ROAD_X + ROAD_WIDTH, 0), (ROAD_X + ROAD_WIDTH, HEIGHT), 5)

        divisors = [ROAD_X + LANE_WIDTH, ROAD_X + 2 * LANE_WIDTH]

        for divisor in divisors:
            y = -LINE_HEIGHT
            while y < HEIGHT:
                pygame.draw.rect(
                    screen,
                    YELLOW,
                    (divisor - 5, y + self.line_offset, 10, LINE_HEIGHT)
                )
                y += LINE_HEIGHT + LINE_GAP