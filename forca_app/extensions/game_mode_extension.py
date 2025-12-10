# Extensão para modos de jogo (singleplayer, multiplayer, bot)

class GameMode:
    SINGLEPLAYER = 'singleplayer'
    MULTIPLAYER = 'multiplayer'

class GameSession:
    def __init__(self, mode, player1, player2=None, bot=None):
        self.mode = mode
        self.player1 = player1
        self.player2 = player2
        self.bot = bot

    def is_singleplayer(self):
        return self.mode == GameMode.SINGLEPLAYER

    def is_multiplayer(self):
        return self.mode == GameMode.MULTIPLAYER

    def get_opponent(self):
        if self.is_singleplayer():
            return self.bot
        return self.player2
