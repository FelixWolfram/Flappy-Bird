class Info:
    WIN_WIDTH = 600
    WIN_HEIGHT = 800
    FPS = 60
    BOTTOM_HEIGHT = WIN_WIDTH // 5
    GRAVITY = 45


class GameContext:
    score = 0
    game_start = True
    game_over = False
    bird_widht = None