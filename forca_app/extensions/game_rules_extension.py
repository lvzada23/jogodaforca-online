# Extensão para regras do jogo da forca
# Gerencia chances, pontuação, rodada, derrota, etc.

MAX_ERRORS = 6

class GameRules:
    def __init__(self):
        self.max_errors = MAX_ERRORS

    def check_loss(self, errors):
        """Verifica se o jogador perdeu a rodada."""
        return errors >= self.max_errors

    def update_score(self, current_score, won_round):
        """Atualiza a pontuação do jogador conforme vitória ou derrota na rodada."""
        if won_round:
            return current_score + 1
        else:
            return current_score - 1

    def check_game_over(self, score):
        """Verifica se o jogador perdeu o jogo (score < 0)."""
        return score < 0
