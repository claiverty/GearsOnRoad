import os
import sys
import math
import pygame

from src.Const import (
    WIDTH,
    HEIGHT,
    TITLE,
    FPS,
    WHITE,
    YELLOW,
    INITIAL_ENEMY_SPEED,
    LINE_SPEED,
    ROAD_X,
    ROAD_WIDTH,
    ASSETS_DIR
)
from src.Player import Player
from src.EnemyCar import EnemyCar
from src.Background import Background
from src.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 22)

        self.menu = Menu()
        self.high_score = self.load_high_score()

        self.crash_sound = self.load_crash_sound()
        self.reset()

    def load_crash_sound(self):
        sound_path = os.path.join(ASSETS_DIR, "sounds", "crash.wav")
        try:
            return pygame.mixer.Sound(sound_path)
        except (pygame.error, FileNotFoundError):
            return None

    def play_crash_sound(self):
        if self.crash_sound is not None:
            self.crash_sound.play()

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

    def trigger_crash(self, crash_x, crash_y):
        self.play_crash_sound()
        self.show_explosion(crash_x, crash_y)
        self.running = False

    def show_explosion(self, center_x, center_y):
        explosion_duration = 500
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < explosion_duration:
            dt = self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            elapsed = pygame.time.get_ticks() - start_time
            progress = elapsed / explosion_duration

            self.background.update(LINE_SPEED)
            for enemy in self.enemies:
                enemy.update(self.enemy_speed * 0.3)

            self.background.draw(self.screen)

            for enemy in self.enemies:
                enemy.draw(self.screen)

            self.player.draw(self.screen)
            self.draw_hud()

            self.draw_explosion_frame(center_x, center_y, progress)

            pygame.display.update()

    def draw_explosion_frame(self, x, y, progress):
        max_radius = 55
        radius = int(max_radius * progress)

        colors = [
            (255, 230, 120),
            (255, 180, 50),
            (255, 90, 0),
            (180, 180, 180)
        ]

        for i, color in enumerate(colors):
            current_radius = max(8, radius - i * 10)
            if current_radius > 0:
                pygame.draw.circle(self.screen, color, (x, y), current_radius)

        for angle in range(0, 360, 30):
            spark_length = int(25 + 20 * math.sin(progress * math.pi))
            end_x = x + int(math.cos(math.radians(angle)) * spark_length)
            end_y = y + int(math.sin(math.radians(angle)) * spark_length)
            pygame.draw.line(self.screen, (255, 220, 120), (x, y), (end_x, end_y), 3)

    def update(self, dt):
        self.spawn_timer += dt
        self.player.update()

        player_hitbox = self.player.get_hitbox()

        if player_hitbox.left <= ROAD_X or player_hitbox.right >= ROAD_X + ROAD_WIDTH:
            self.trigger_crash(self.player.rect.centerx, self.player.rect.centery)
            return

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
                crash_x = (enemy.rect.centerx + self.player.rect.centerx) // 2
                crash_y = (enemy.rect.centery + self.player.rect.centery) // 2
                self.trigger_crash(crash_x, crash_y)
                return

    def draw_hud(self):
        hud_width = 320
        hud_height = 70
        hud_x = (WIDTH - hud_width) // 2
        hud_y = 10

        hud_surface = pygame.Surface((hud_width, hud_height), pygame.SRCALPHA)
        pygame.draw.rect(hud_surface, (0, 0, 0, 170), (0, 0, hud_width, hud_height), border_radius=12)
        pygame.draw.rect(hud_surface, WHITE, (0, 0, hud_width, hud_height), 2, border_radius=12)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        high_score_text = self.small_font.render(f"Recorde: {self.high_score}", True, WHITE)
        speed_text = self.small_font.render(f"Velocidade: {self.enemy_speed:.1f}", True, YELLOW)

        hud_surface.blit(score_text, (18, 8))
        hud_surface.blit(high_score_text, (18, 38))
        hud_surface.blit(speed_text, (175, 38))

        self.screen.blit(hud_surface, (hud_x, hud_y))

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