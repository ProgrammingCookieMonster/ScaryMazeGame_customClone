# main - the game loop and state handling.
import random
import sys
import pygame
from settings import *
from assets import load_image, load_sounds
from level import Level
from menu import Menu, draw_text


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # SCALED makes the 1280x720 game stretch to fit any screen size.
        flags = pygame.SCALED | (pygame.FULLSCREEN if FULLSCREEN else 0)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        # Fonts, Nne -- inbuilt in pygame
        self.font_title = pygame.font.Font(None, 90)
        self.font_menu = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        # Assets
        self.menu_image = load_image("menu.png", (WIDTH, HEIGHT), (40, 10, 50))
        self.win_image = load_image("win.png", (WIDTH, HEIGHT), (20, 90, 40))
        self.death_sounds = load_sounds("death_*.*")
        win_sounds = load_sounds("win.*")
        self.win_sound = win_sounds[0] if win_sounds else None

        self.level = Level()

        # Menus
        self.main_menu = Menu(["Play", "Quit"], self.font_menu,
                              WIDTH // 2, HEIGHT - 170)
        self.popup_menu = Menu(["Restart", "Main menu"], self.font_menu,
                               WIDTH // 2, HEIGHT // 2 + 20)

        self.state = "menu"          # menu / playing / popup / win
        self.popup_title = ""
        self.win_end_time = 0
        self.player_pos = pygame.math.Vector2(self.level.start)

    # ---------- state changes ----------
    def start_game(self):
        pygame.mixer.stop()
        self.player_pos = pygame.math.Vector2(self.level.start)
        self.state = "playing"

    def open_popup(self, title):
        self.popup_title = title
        self.popup_menu.selected = 0
        self.state = "popup"

    def die(self):
        if self.death_sounds:
            random.choice(self.death_sounds).play()   # random pick from list
        self.open_popup("You died!")

    def win(self):
                # the image for the win is either sussy or scarry, so it plays only for the duration of the sound
        self.state = "win"
        if self.win_sound:
            self.win_sound.play()
            duration_ms = int(self.win_sound.get_length() * 1000)
        else:
            duration_ms = DEFAULT_WIN_MS
        self.win_end_time = pygame.time.get_ticks() + duration_ms - 300

    def quit(self):
        pygame.quit()
        sys.exit()

    # ---------- the loop ----------
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000   # seconds since last frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                self.handle_event(event)
            self.update(dt)
            self.draw()
            pygame.display.flip()

    def handle_event(self, event):
        if self.state == "menu":
            choice = self.main_menu.handle_event(event)
            if choice == "Play":
                self.start_game()
            elif choice == "Quit":
                self.quit()

        elif self.state == "playing":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.open_popup("Paused")

        elif self.state == "popup":
            # Esc while paused = resume
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                    and self.popup_title == "Paused"):
                self.state = "playing"
                return
            choice = self.popup_menu.handle_event(event)
            if choice == "Restart":
                self.start_game()
            elif choice == "Main menu":
                pygame.mixer.stop()
                self.state = "menu"

    def update(self, dt):
        if self.state == "playing":
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - \
                 (keys[pygame.K_LEFT] or keys[pygame.K_a])
            dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - \
                 (keys[pygame.K_UP] or keys[pygame.K_w])

            move = pygame.math.Vector2(dx, dy)
            if move.length_squared() > 0:
                # normalize so diagonals aren't faster than straight lines
                self.player_pos += move.normalize() * PLAYER_SPEED * dt

            x, y = self.player_pos
            if not self.level.circle_is_safe(x, y, PLAYER_RADIUS):
                self.die()
            elif self.level.reached_finish(x, y):
                self.win()

        elif self.state == "win":
            if pygame.time.get_ticks() >= self.win_end_time:
                self.open_popup("You made it!")

    # ---------- drawing ----------
    def draw_game(self):
        self.level.draw(self.screen)
        pygame.draw.circle(self.screen, PLAYER_COLOR,
                           (int(self.player_pos.x), int(self.player_pos.y)),
                           PLAYER_RADIUS)

    def draw(self):
        if self.state == "menu":
            self.screen.blit(self.menu_image, (0, 0))
            # dark bar behind the text so it's readable on any picture
            bar = pygame.Surface((WIDTH, 150), pygame.SRCALPHA)
            bar.fill((0, 0, 0, 170))
            self.screen.blit(bar, (0, 0))
            draw_text(self.screen, TITLE, self.font_title, GREEN, (WIDTH // 2, 50))
            draw_text(self.screen, CREDITS_LINE_1, self.font_small, WHITE, (WIDTH // 2, 100))
            draw_text(self.screen, CREDITS_LINE_2, self.font_small, WHITE, (WIDTH // 2, 128))
            self.main_menu.draw(self.screen)

        elif self.state == "playing":
            self.draw_game()

        elif self.state == "popup":
            self.draw_game()                      # frozen game underneath
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            self.screen.blit(overlay, (0, 0))
            draw_text(self.screen, self.popup_title, self.font_title,
                      GREEN, (WIDTH // 2, HEIGHT // 2 - 90))
            if self.popup_title == "Paused":
                draw_text(self.screen, "Esc to resume", self.font_small,
                          WHITE, (WIDTH // 2, HEIGHT // 2 - 40))
            self.popup_menu.draw(self.screen)

        elif self.state == "win":
            self.screen.blit(self.win_image, (0, 0))


if __name__ == "__main__":
    Game().run()