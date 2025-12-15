from forca_app.extensions import db

def mascarar_palavra(palavra, letras_certas):
    """Gera a palavra com caracteres ocultos."""
    return "".join([letra if letra in letras_certas else "_" for letra in palavra])


def processar_tentativa(game, letra):
    """
    Processa o chute de letra para o jogo.
    Atualiza tentativas, letras certas/erradas e verifica fim de jogo.
    """

    letra = letra.lower()

    # 1. Letra já usada
    if letra in game.letras_certas or letra in game.letras_erradas:
        return {
            "status": "repetida",
            "message": "Letra já foi usada!"
        }

    # 2. Acertou
    if letra in game.palavra.lower():
        game.letras_certas += letra

        # Verificar vitória
        palavra_mascarada = mascarar_palavra(game.palavra.lower(), game.letras_certas)

        if "_" not in palavra_mascarada:
            return {
                "status": "vitoria",
                "message": "Parabéns! A palavra foi completada.",
                "palavra": game.palavra
            }

        return {
            "status": "acerto",
            "message": "Boa! Você acertou uma letra.",
        }

    # 3. Errou
    game.letras_erradas += letra
    game.tentativas_restantes -= 1

    if game.tentativas_restantes <= 0:
        return {
            "status": "derrota",
            "message": "Tentativas esgotadas. O boneco foi enforcado!",
            "palavra": game.palavra
        }

    return {
        "status": "erro",
        "message": "Letra errada!"
    }


def alternar_rodada(game):
    """
    Alterna turno entre Player 1 e Player 2.
    """
    if game.rodada_atual == 1:
        game.rodada_atual = 2
    else:
        game.rodada_atual = 1


def estado_atual(game):
    """
    Retorna o estado atual do jogo para renderização no template.
    """
    palavra_mascarada = mascarar_palavra(
        game.palavra.lower(),
        game.letras_certas
    )

    return {
        "palavra_mascarada": palavra_mascarada,
        "letras_erradas": ", ".join(game.letras_erradas),
        "tentativas": game.tentativas_restantes,
        "rodada": game.rodada_atual
    }


def finalizar_rodada(game, status):
    """Finaliza a rodada atual: atualiza vencedor, pontos e níveis dos jogadores."""
    # constants
    LEVEL_STEP = 10
    LEVEL_MIN = 10

    # define qual jogador estava jogando no momento
    current_player = 1 if game.rodada_atual == 1 else 2

    if status == "vitoria":
        # jogador atual venceu
        winner_id = game.player1_id if current_player == 1 else game.player2_id
        loser_id = game.player2_id if current_player == 1 else game.player1_id
    else:
        # derrota por tentativas: jogador atual perdeu
        loser_id = game.player1_id if current_player == 1 else game.player2_id
        winner_id = game.player2_id if current_player == 1 else game.player1_id

    # aplica pontuação/níveis e conta vitórias por rodada
    from forca_app.models.user import User

    # incrementa vitória por rodada
    if winner_id and loser_id:
        if winner_id == game.player1_id:
            game.wins_p1 = (game.wins_p1 or 0) + 1
        elif winner_id == game.player2_id:
            game.wins_p2 = (game.wins_p2 or 0) + 1

    # registra vencedor da rodada no jogo (campo temporário)
    game.vencedor_id = winner_id

    # aplica pontos e níveis
    if winner_id:
        winner = db.session.get(User, winner_id)
        if winner:
            winner.points = (winner.points or 0) + 1

    if loser_id:
        loser = db.session.get(User, loser_id)
        if loser:
            loser.points = (loser.points or 0) - 1
            new_level = (loser.level or LEVEL_MIN) - LEVEL_STEP
            loser.level = new_level if new_level >= LEVEL_MIN else LEVEL_MIN

            if loser.points < 0:
                loser.level = LEVEL_MIN

    # atualizar contador de rodadas completadas
    game.rounds_completed = (game.rounds_completed or 0) + 1

    # se já completou todas as rodadas, decide o vencedor do jogo
    if game.rounds_completed >= (game.rounds_total or 2):
        # determina vencedor por número de vitórias em rodadas
        if game.wins_p1 > game.wins_p2:
            overall_winner = game.player1_id
            overall_loser = game.player2_id
        elif game.wins_p2 > game.wins_p1:
            overall_winner = game.player2_id
            overall_loser = game.player1_id
        else:
            # empate: decide por nível atual dos jogadores
            p1 = db.session.get(User, game.player1_id) if game.player1_id else None
            p2 = db.session.get(User, game.player2_id) if game.player2_id else None
            level1 = p1.level if p1 else 0
            level2 = p2.level if p2 else 0
            if level1 >= level2:
                overall_winner = game.player1_id
                overall_loser = game.player2_id
            else:
                overall_winner = game.player2_id
                overall_loser = game.player1_id

        # aplica ganho de nível ao vencedor
        if overall_winner:
            w = db.session.get(User, overall_winner)
            if w:
                w.level = min(100, (w.level or 10) + LEVEL_STEP) 

        # marca fim de jogo
        from datetime import datetime
        game.data_fim = datetime.utcnow()
        game.vencedor_id = overall_winner

    return {
        "winner_id": winner_id,
        "loser_id": loser_id
    }
