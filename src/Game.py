import os
import sys
import math
import random
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
        duration = 700
        start_time = pygame.time.get_ticks()

        sparks = []
        smoke_particles = []
        fire_particles = []

        for _ in range(30):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(2.5, 8.5)
            sparks.append({
                "x": center_x,
                "y": center_y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(16, 32)
            })

        for _ in range(22):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(0.8, 2.8)
            smoke_particles.append({
                "x": center_x + random.randint(-12, 12),
                "y": center_y + random.randint(-12, 12),
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "radius": random.randint(10, 20),
                "life": random.randint(28, 50)
            })

        for _ in range(20):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(1.0, 4.0)
            fire_particles.append({
                "x": center_x + random.randint(-8, 8),
                "y": center_y + random.randint(-8, 8),
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "radius": random.randint(8, 16),
                "life": random.randint(14, 26),
                "color": random.choice([
                    (255, 220, 120),
                    (255, 170, 50),
                    (255, 110, 20),
                    (255, 80, 0)
                ])
            })

        while pygame.time.get_ticks() - start_time < duration:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            elapsed = pygame.time.get_ticks() - start_time
            progress = elapsed / duration

            shake_x = random.randint(-5, 5) if progress < 0.35 else random.randint(-2, 2)
            shake_y = random.randint(-5, 5) if progress < 0.35 else random.randint(-2, 2)

            self.background.draw(self.screen)

            for enemy in self.enemies:
                enemy.draw(self.screen)

            self.player.draw(self.screen)
            self.draw_hud()

            self.draw_explosion_flash(progress)
            self.update_and_draw_fire(fire_particles, shake_x, shake_y)
            self.update_and_draw_sparks(sparks, shake_x, shake_y)
            self.update_and_draw_smoke(smoke_particles, shake_x, shake_y)

            pygame.display.update()

    def draw_explosion_flash(self, progress):
        if progress < 0.10:
            flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            alpha = int(140 * (1 - progress / 0.10))
            flash.fill((255, 245, 210, alpha))
            self.screen.blit(flash, (0, 0))

    def update_and_draw_fire(self, fire_particles, shake_x, shake_y):
        for fire in fire_particles[:]:
            fire["x"] += fire["vx"]
            fire["y"] += fire["vy"]
            fire["life"] -= 1
            fire["radius"] += 0.25
            fire["vx"] *= 0.97
            fire["vy"] *= 0.97

            if fire["life"] <= 0:
                fire_particles.remove(fire)
                continue

            alpha = max(30, min(180, fire["life"] * 8))

            blob_size = int(fire["radius"] * 2.4)
            blob = pygame.Surface((blob_size, blob_size), pygame.SRCALPHA)

            for _ in range(4):
                offset_x = random.randint(-4, 4)
                offset_y = random.randint(-4, 4)
                radius = max(4, int(fire["radius"] + random.randint(-2, 3)))
                pygame.draw.circle(
                    blob,
                    (*fire["color"], alpha),
                    (blob_size // 2 + offset_x, blob_size // 2 + offset_y),
                    radius
                )

            self.screen.blit(
                blob,
                (
                    fire["x"] - blob_size // 2 + shake_x,
                    fire["y"] - blob_size // 2 + shake_y
                )
            )

    def update_and_draw_sparks(self, sparks, shake_x, shake_y):
        for spark in sparks[:]:
            spark["x"] += spark["vx"]
            spark["y"] += spark["vy"]
            spark["life"] -= 1
            spark["vx"] *= 0.99
            spark["vy"] *= 0.99

            if spark["life"] <= 0:
                sparks.remove(spark)
                continue

            end_x = spark["x"] - spark["vx"] * random.uniform(1.5, 3.0)
            end_y = spark["y"] - spark["vy"] * random.uniform(1.5, 3.0)

            color = random.choice([
                (255, 220, 100),
                (255, 190, 70),
                (255, 150, 40)
            ])

            pygame.draw.line(
                self.screen,
                color,
                (int(spark["x"] + shake_x), int(spark["y"] + shake_y)),
                (int(end_x + shake_x), int(end_y + shake_y)),
                random.randint(2, 3)
            )

    def update_and_draw_smoke(self, smoke_particles, shake_x, shake_y):
        for smoke in smoke_particles[:]:
            smoke["x"] += smoke["vx"]
            smoke["y"] += smoke["vy"]
            smoke["life"] -= 1
            smoke["radius"] += 0.45
            smoke["vx"] *= 0.985
            smoke["vy"] *= 0.985

            if smoke["life"] <= 0:
                smoke_particles.remove(smoke)
                continue

            alpha = max(15, min(110, smoke["life"] * 2))

            cloud_size = int(smoke["radius"] * 3)
            cloud = pygame.Surface((cloud_size, cloud_size), pygame.SRCALPHA)

            smoke_colors = [
                (50, 50, 50, alpha),
                (70, 70, 70, alpha - 10 if alpha > 10 else alpha),
                (90, 90, 90, alpha - 20 if alpha > 20 else alpha),
            ]

            for _ in range(5):
                offset_x = random.randint(-8, 8)
                offset_y = random.randint(-8, 8)
                radius = max(6, int(smoke["radius"] + random.randint(-3, 4)))
                color = random.choice(smoke_colors)
                pygame.draw.circle(
                    cloud,
                    color,
                    (cloud_size // 2 + offset_x, cloud_size // 2 + offset_y),
                    radius
                )

            self.screen.blit(
                cloud,
                (
                    smoke["x"] - cloud_size // 2 + shake_x,
                    smoke["y"] - cloud_size // 2 + shake_y
                )
            )

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