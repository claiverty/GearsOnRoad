import pygame
from src.Const import WIDTH, HEIGHT, BLACK, WHITE, RED, YELLOW


class Menu:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 54, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 24)
        self.text_font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 22)

    def draw_start(self, screen):
        screen.fill(BLACK)

        title = self.title_font.render("Gears on Road", True, RED)
        subtitle = self.subtitle_font.render("Endless Runner 2D", True, YELLOW)

        start = self.text_font.render("Pressione ENTER para jogar", True, WHITE)
        exit_text = self.text_font.render("Pressione ESC para sair", True, WHITE)

        control_1 = self.small_font.render("Controles:", True, WHITE)
        control_2 = self.small_font.render("Seta Esquerda - mover para a esquerda", True, WHITE)
        control_3 = self.small_font.render("Seta Direita - mover para a direita", True, WHITE)
        objective = self.small_font.render("Objetivo: desviar dos carros e sobreviver", True, WHITE)

        screen.blit(title, title.get_rect(center=(WIDTH // 2, 110)))
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 160)))

        screen.blit(start, start.get_rect(center=(WIDTH // 2, 260)))
        screen.blit(exit_text, exit_text.get_rect(center=(WIDTH // 2, 305)))

        screen.blit(control_1, control_1.get_rect(center=(WIDTH // 2, 420)))
        screen.blit(control_2, control_2.get_rect(center=(WIDTH // 2, 465)))
        screen.blit(control_3, control_3.get_rect(center=(WIDTH // 2, 505)))
        screen.blit(objective, objective.get_rect(center=(WIDTH // 2, 560)))

    def draw_game_over(self, screen, score, high_score):
        screen.fill(BLACK)

        title = self.title_font.render("GAME OVER", True, RED)
        score_text = self.text_font.render(f"Pontuação final: {score}", True, WHITE)
        high_score_text = self.text_font.render(f"Recorde: {high_score}", True, YELLOW)
        restart = self.text_font.render("Pressione ENTER para reiniciar", True, WHITE)
        exit_text = self.text_font.render("Pressione ESC para sair", True, WHITE)

        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 130)))
        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        screen.blit(high_score_text, high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10)))
        screen.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
        screen.blit(exit_text, exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 95)))