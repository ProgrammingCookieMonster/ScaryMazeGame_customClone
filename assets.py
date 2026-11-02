# loading assets
# should handle game without crushing even if asset files are missing / are not named correctly

import glob
import os
import pygame

# define folder this file lives in, path should name no difference where game is launched from then
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(filename, size, fallback_color):
    # loads assets/image/filename scaled to size param
    # returns a plan base color in case something is wrong
    path = os.path.join(BASE_DIR, "assets", "images", filename)
    try:
        image = pygame.image.load(path).convert()
        return pygame.transform.smoothscale(image, size)
    except (FileNotFoundError, pygame.error):
        print(f"[assets] missing image: {path}")
        surface = pygame.Surface(size)
        surface.fill(fallback_color)
        return surface

def load_sounds(pattern):
    # loads sounds
    # death sounds load in a list
    # returns list empty if nothing found, game can run without sounds its just boring
    folder = os.path.join(BASE_DIR, "assets", "sounds")
    sounds = []
    for path in sorted(glob.glob(os.path.join(folder, pattern))):
        try:
            sounds.append(pygame.mixer.Sound(path))
        except pygame.error:
            print(f"[assets] could not be load sound: {path}")
    return sounds