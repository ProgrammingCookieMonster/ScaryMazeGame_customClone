# level -- define playspace, danger areas etc

# path player follows is made out of squares
# as player does progress, that shrinks from start to finish so the game has some actual difficulty
# collision does not keep track of geometry for walls, it checks if all pixels are white on the collision canvas
#       non-white pixels would mean player passed wall bound and looses

import math
import pygame
from settings import *


class Level:
    def __init__(self):
        self.start = WAYPOINTS[0]
        self.end = WAYPOINTS[-1]

        self.finish_rect = pygame.Rect(0, 0, FINISH_SIZE, FINISH_SIZE)
        self.finish_rect.center = self.end

        # 2 layers: canvas image, collision
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.collision = pygame.Surface((WIDTH, HEIGHT))
        self._build()

    def _build(self):
        self.image.fill(WALL_COLOR)
        self.collision.fill(BLACK)

        # length of each straight piece and whole path
        pairs = list(zip(WAYPOINTS, WAYPOINTS[1:]))
        lengths = [math.dist(a, b) for a, b in pairs]
        total = sum(lengths)

        travelled = 0               # distance covered by earlier pieces
        for (a, b), length in zip(pairs, lengths):
            steps = int(length / STEP)
            for i in range(steps + 1):
                t = i / steps
                x = a[0] + (b[0] - a[0]) * t        # linear interpolation
                y = a[1] + (b[1] - a[1]) * t

                # calculate progress on path
                progress = (travelled + length * t) / total
                width = PATH_WIDTH_START + (PATH_WIDTH_END - PATH_WIDTH_START) * progress

                size = int(width)
                square = pygame.Rect(0, 0, size, size)
                square.center = (round(x), round(y))
                pygame.draw.rect(self.image, PATH_COLOR, square)
                pygame.draw.rect(self.collision, WHITE, square)
            travelled += length

        # finished pad
        pygame.draw.rect(self.image, FINISH_COLOR, self.finish_rect)
        pygame.draw.rect(self.collision, WHITE, self.finish_rect)

    def _is_safe(self, x, y):
        px, py = int(x), int(y)
        if not (0 <= px < WIDTH and 0 <= py < HEIGHT):
            return False                    # off screen is also wall
        return self.collision.get_at((px, py))[0] == 255

    def circle_is_safe(self, x, y, radius):
        for k in range(16):
            angle = 2 * math.pi * k / 16
            if not self._is_safe(x + radius * math.cos(angle), y + radius * math.sin(angle)):
                return False
        return True

    def reached_finish(self, x, y):
        return self.finish_rect.collidepoint(x, y)

    def draw(self, surface):
        surface.blit(self.image, (0, 0))