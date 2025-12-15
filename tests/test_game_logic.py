import pytest

from forca_app.services.game_logic import mascarar_palavra, processar_tentativa, finalizar_rodada
from forca_app.models.game import Game
from forca_app.models.user import User


def test_mascarar_palavra():
    assert mascarar_palavra('casa', 'a') == '_a_a'


def test_processar_tentativa_acerto_e_vitoria():
    game = Game(palavra='casa', letras_certas='', letras_erradas='', tentativas_restantes=6)
    res = processar_tentativa(game, 'c')
    assert res['status'] == 'acerto'

    # completar a palavra (evita marcar a letra como já usada)
    game.letras_certas = 'cs'
    res2 = processar_tentativa(game, 'a')
    assert res2['status'] == 'vitoria'


def test_processar_tentativa_repetida():
    game = Game(palavra='bola', letras_certas='b', letras_erradas='o', tentativas_restantes=6)
    res = processar_tentativa(game, 'b')
    assert res['status'] == 'repetida'


def test_processar_tentativa_derrota():
    game = Game(palavra='x', letras_certas='', letras_erradas='', tentativas_restantes=1)
    res = processar_tentativa(game, 'z')
    assert res['status'] == 'derrota'


def test_finalizar_rodada_updates(app):
    # cria dois usuários e um jogo no DB para verificar updates
    from forca_app.extensions import db

    with app.app_context():
        u1 = User(name='P1', email='p1@example.com')
        u1.set_password('x')
        u2 = User(name='P2', email='p2@example.com')
        u2.set_password('x')

        db.session.add_all([u1, u2])
        db.session.commit()

        game = Game(player1_id=u1.id, player2_id=u2.id, modo='multiplayer', dificuldade='easy', palavra='casa')
        db.session.add(game)
        db.session.commit()

        # rodada 1: p1 vence
        game.rodada_atual = 1
        finalizar_rodada(game, 'vitoria')
        db.session.commit()

        assert game.wins_p1 == 1
        assert game.rounds_completed == 1

        # rodada 2: p2 vence
        game.rodada_atual = 2
        finalizar_rodada(game, 'vitoria')
        db.session.commit()

        assert game.wins_p2 == 1
        assert game.rounds_completed == 2

        # jogo deve terminar e ter vencedor por desempate de nível/pontos
        assert game.data_fim is not None
        assert game.vencedor_id is not None
