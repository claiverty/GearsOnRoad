import os
import pygame
from src.Const import WIDTH, HEIGHT, BLACK, WHITE, RED, YELLOW, IMAGES_DIR


class Menu:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 54, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 22)

        self.menu_bg = self.load_background("menu_bg.png")

    def load_background(self, filename):
        path = os.path.join(IMAGES_DIR, filename)
        image = pygame.image.load(path).convert()
        image = pygame.transform.smoothscale(image, (WIDTH, HEIGHT))
        return image

    def draw_start(self, screen):
        screen.blit(self.menu_bg, (0, 0))

    def draw_game_over(self, screen, score, high_score):
        screen.fill(BLACK)

        title = self.title_font.render("GAME OVER", True, RED)
        score_text = self.text_font.render(f"Pontuação final: {score}", True, WHITE)
        high_score_text = self.text_font.render(f"Recorde: {high_score}", True, YELLOW)
        restart = self.text_font.render("Pressione ENTER para reiniciar", True, WHITE)
        exit_text = self.text_font.render("Pressione ESC para sair", True, WHITE)

        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120)))
        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        screen.blit(high_score_text, high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        screen.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60)))
        screen.blit(exit_text, exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100)))