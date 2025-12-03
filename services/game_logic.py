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
