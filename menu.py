# menu -- loads the image of the event this game is used for && simple play button

import pygame
from settings import *

def draw_text(surface, text, font, color, center):
    # render text
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(center=center))

class Menu:
    def __init__(self, options, font, center_x, start_y, spacing=70):
        self.stick_ready = True
        self.options = options
        self.font = font
        self.selected = 0
        self.rects = []
        for i in range(len(options)):
            # add more options if decides later, for now it will just have a play rect button
            rect = pygame.Rect(0, 0, 320, 56)
            rect.center = (center_x, start_y + i * spacing)
            self.rects.append(rect)
    def _move(self, step):
        self.selected = (self.selected + step) % len(self.options)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self._move(-1)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self._move(1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.options[self.selected]

        # ---- controller ----
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == BTN_CONFIRM:
                return self.options[self.selected]
            elif event.button == BTN_DPAD_UP:
                self._move(-1)
            elif event.button == BTN_DPAD_DOWN:
                self._move(1)

        elif event.type == pygame.JOYHATMOTION:     # D-pad, when reported as a "hat"
            if event.value[1] == 1:                 # value is (x, y); y=1 means up
                self._move(-1)
            elif event.value[1] == -1:
                self._move(1)

        elif event.type == pygame.JOYAXISMOTION and event.axis == 1:   # left stick, vertical
            if abs(event.value) < 0.3:
                self.stick_ready = True             # stick is back near the middle
            elif self.stick_ready and abs(event.value) > 0.6:
                self._move(1 if event.value > 0 else -1)
                self.stick_ready = False            # wait until it returns to the middle

        # ---- mouse / touch (unchanged) ----
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    self.selected = i

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    return self.options[i]
        return None

    def draw(self, surface):
        for i, (text, rect) in enumerate(zip(self.options, self.rects)):
            is_selected = (i == self.selected)
            fill = GREEN if is_selected else DARK
            pygame.draw.rect(surface, fill, rect, border_radius=10)
            pygame.draw.rect(surface, GREEN, rect, width=3, border_radius=10)
            draw_text(surface, text, self.font, BLACK if is_selected else WHITE, rect.center)