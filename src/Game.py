import sys
import pygame

from src.Const import WIDTH, HEIGHT, TITLE, FPS, WHITE, YELLOW, INITIAL_ENEMY_SPEED, LINE_SPEED
from src.Player import Player
from src.EnemyCar import EnemyCar
from src.Background import Background
from src.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 22)

        self.menu = Menu()
        self.high_score = self.load_high_score()
        self.reset()

    def load_high_score(self):
        try:
            with open("highscore.txt", "r", encoding="utf-8") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        with open("highscore.txt", "w", encoding="utf-8") as file:
            file.write(str(self.high_score))

    def reset(self):
        self.background = Background()
        self.player = Player()
        self.enemies = []
        self.enemy_speed = INITIAL_ENEMY_SPEED
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = 900
        self.running = True

    def spawn_enemy(self):
        self.enemies.append(EnemyCar())

    def show_start_screen(self):
        while True:
            self.menu.draw_start(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def show_game_over_screen(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        while True:
            self.menu.draw_game_over(self.screen, self.score, self.high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.reset()
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

    def update(self, dt):
        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_enemy()
            self.spawn_timer = 0

        self.background.update(LINE_SPEED)

        for enemy in self.enemies[:]:
            enemy.update(self.enemy_speed)

            if enemy.off_screen():
                self.enemies.remove(enemy)
                self.score += 1

                if self.score > self.high_score:
                    self.high_score = self.score

                if self.score % 5 == 0:
                    self.enemy_speed += 0.5
                    if self.spawn_interval > 350:
                        self.spawn_interval -= 40


            elif enemy.get_hitbox().colliderect(self.player.get_hitbox()):

                self.running = False

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        high_score_text = self.small_font.render(f"Recorde: {self.high_score}", True, WHITE)
        speed_text = self.small_font.render(f"Velocidade: {self.enemy_speed:.1f}", True, YELLOW)

        self.screen.blit(score_text, (20, 20))
        self.screen.blit(high_score_text, (20, 55))
        self.screen.blit(speed_text, (20, 85))

    def draw(self):
        self.background.draw(self.screen)
        self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.draw_hud()
        pygame.display.update()

    def game_loop(self):
        self.running = True

        while self.running:
            dt = self.clock.tick(FPS)
            self.handle_events()
            self.update(dt)
            self.draw()

    def run(self):
        self.show_start_screen()

        while True:
            self.game_loop()
            self.show_game_over_screen()