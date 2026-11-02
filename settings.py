# settings.py - every "tweakable" number lives here.

# --- Window ---
WIDTH, HEIGHT = 1920, 1080
FPS = 60
FULLSCREEN = False          # True for running game on booth
TITLE = "Spooky Smurf"

# Main Menu extras
CREDITS_LINE_1 = "Made by TORRENT 2026"
CREDITS_LINE_2 = "WYSIWYG  -  v0.3.5"

# --- Colours in RGB ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK = (30, 20, 40)
WALL_COLOR = (25, 15, 35)
PATH_COLOR = (235, 225, 200)
PLAYER_COLOR = (40, 120, 255)
FINISH_COLOR = (60, 200, 90)

# --- Player ---
PLAYER_RADIUS = 13
PLAYER_SPEED = 300          # pixels per second

# --- Path ---
# The centre line of the serpentine. Corners of the "S" shape.
LEFT, RIGHT = 150, 1770
ROWS = [165, 405, 645, 885]
WAYPOINTS = [
    (LEFT, ROWS[0]), (RIGHT, ROWS[0]),    # row 1: go right
    (RIGHT, ROWS[1]), (LEFT, ROWS[1]),    # down, row 2: go left
    (LEFT, ROWS[2]), (RIGHT, ROWS[2]),    # down, row 3: go right
    (RIGHT, ROWS[3]), (LEFT, ROWS[3]),    # down, row 4: go left -> finish
]
PATH_WIDTH_START = 135       # width path at start, should look promising and duable
PATH_WIDTH_END = 32         # controls difficulty for the end -- cannot make this too short if prizes are involved
FINISH_SIZE = 32
STEP = 2                    # drawing precision (pixels between "stamps")

# --- Win screen ---
DEFAULT_WIN_MS = 3000       # used if there is no win sound file