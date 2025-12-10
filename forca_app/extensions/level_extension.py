# Extensão para níveis e dificuldades do jogo

LEVEL_MIN = 10
LEVEL_MAX = 100
LEVEL_STEP = 10

class Difficulty:
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

class LevelManager:
    def __init__(self, initial_level=LEVEL_MIN):
        self.level = initial_level
        self.difficulty = Difficulty.EASY

    def set_difficulty(self, difficulty):
        if difficulty in (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD):
            self.difficulty = difficulty

    def increase_level(self):
        if self.level + LEVEL_STEP <= LEVEL_MAX:
            self.level += LEVEL_STEP

    def decrease_level(self):
        if self.level - LEVEL_STEP >= LEVEL_MIN:
            self.level -= LEVEL_STEP

    def is_max_level(self):
        return self.level == LEVEL_MAX

    def is_min_level(self):
        return self.level == LEVEL_MIN
