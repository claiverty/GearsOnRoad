import os
import pygame
from src.Const import (
    WIDTH,
    HEIGHT,
    ROAD_X,
    ROAD_WIDTH,
    LANE_WIDTH,
    LINE_HEIGHT,
    LINE_GAP,
    IMAGES_DIR
)


class Background:
    def __init__(self):
        self.line_offset = 0
        self.side_offset = 0

        self.left_width = ROAD_X
        self.right_width = WIDTH - (ROAD_X + ROAD_WIDTH)

        self.left_forest = self.load_zoomed_side_image("forest_left.png", self.left_width, HEIGHT, side="left")
        self.right_forest = self.load_zoomed_side_image("forest_right.png", self.right_width, HEIGHT, side="right")

    def load_zoomed_side_image(self, filename, target_width, target_height, side="left"):
        path = os.path.join(IMAGES_DIR, filename)
        image = pygame.image.load(path).convert()

        zoom = 1.55
        new_width = int(target_width * zoom)
        new_height = int(target_height * zoom)

        image = pygame.transform.smoothscale(image, (new_width, new_height))

        if side == "left":
            crop_x = 0
        else:
            crop_x = new_width - target_width

        crop_y = (new_height - target_height) // 2

        cropped = pygame.Surface((target_width, target_height))
        cropped.blit(image, (0, 0), (crop_x, crop_y, target_width, target_height))
        return cropped

    def update(self, speed):
        self.line_offset += speed
        self.side_offset += speed * 0.10

        if self.line_offset >= LINE_HEIGHT + LINE_GAP:
            self.line_offset = 0

        if self.side_offset >= HEIGHT:
            self.side_offset = 0

    def draw_forest_sides(self, screen):
        right_x = ROAD_X + ROAD_WIDTH

        screen.blit(self.left_forest, (0, self.side_offset - HEIGHT))
        screen.blit(self.left_forest, (0, self.side_offset))

        screen.blit(self.right_forest, (right_x, self.side_offset - HEIGHT))
        screen.blit(self.right_forest, (right_x, self.side_offset))

    def draw_road_base(self, screen):
        shoulder_width = 8

        pygame.draw.rect(screen, (175, 175, 175), (ROAD_X - shoulder_width, 0, shoulder_width, HEIGHT))
        pygame.draw.rect(screen, (175, 175, 175), (ROAD_X + ROAD_WIDTH, 0, shoulder_width, HEIGHT))

        pygame.draw.rect(screen, (92, 92, 96), (ROAD_X, 0, ROAD_WIDTH, HEIGHT))

        subtle_overlay = pygame.Surface((ROAD_WIDTH, HEIGHT), pygame.SRCALPHA)
        subtle_overlay.fill((255, 255, 255, 6))
        screen.blit(subtle_overlay, (ROAD_X, 0))

    def draw_edges(self, screen):
        edge_color = (242, 242, 242)
        pygame.draw.line(screen, edge_color, (ROAD_X, 0), (ROAD_X, HEIGHT), 4)
        pygame.draw.line(screen, edge_color, (ROAD_X + ROAD_WIDTH, 0), (ROAD_X + ROAD_WIDTH, HEIGHT), 4)

    def draw_lane_lines(self, screen):
        divisors = [ROAD_X + LANE_WIDTH, ROAD_X + 2 * LANE_WIDTH]

        for divisor in divisors:
            y = -LINE_HEIGHT
            while y < HEIGHT:
                pygame.draw.rect(
                    screen,
                    (255, 238, 0),
                    (divisor - 4, y + self.line_offset, 8, LINE_HEIGHT),
                    border_radius=2
                )
                y += LINE_HEIGHT + LINE_GAP

    def draw(self, screen):
        self.draw_forest_sides(screen)
        self.draw_road_base(screen)
        self.draw_edges(screen)
        self.draw_lane_lines(screen)