from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from forca_app.extensions import db
from forca_app.models.game import Game
from forca_app.models.user import User
from forca_app.services.word_service import get_random_word
from forca_app.services.game_logic import mascarar_palavra, processar_tentativa, estado_atual


game_bp = Blueprint("game", __name__, url_prefix="/game")


# ------------------------------------------------------------
# Rotas do jogo
# ------------------------------------------------------------


@game_bp.route('/play/<int:game_id>')
def play(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('game.html', game=game)


@game_bp.route('/guess', methods=['POST'])
def guess_letter():
    game_id = request.form.get('game_id') or request.form.get('id')
    letra = request.form.get('letra')

    if not game_id or not letra:
        flash('Parâmetros inválidos.', 'error')
        return redirect(url_for('menu.index'))

    game = Game.query.get(game_id)
    if not game:
        flash('Jogo não encontrado.', 'error')
        return redirect(url_for('menu.index'))

    result = processar_tentativa(game, letra)
    db.session.commit()

    if result.get('status') in ['vitoria', 'derrota']:
        return redirect(url_for('game.result', game_id=game.id, status=result.get('status')))

    return redirect(url_for('game.play', game_id=game.id))


@game_bp.route('/abandon', methods=['POST'])
def abandon_game():
    game_id = request.form.get('game_id')
    if not game_id:
        flash('Jogo inválido.', 'error')
        return redirect(url_for('menu.index'))

    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()

    flash('Você desistiu da partida.', 'info')
    return redirect(url_for('menu.index'))


@game_bp.route('/result/<int:game_id>')
def result(game_id):
    status = request.args.get('status')
    game = Game.query.get_or_404(game_id)
    return render_template('game_result.html', game=game, result=status)


@game_bp.route('/message', methods=['POST'])
def send_message():
    # Implementação mínima: apenas descarta a mensagem por agora
    game_id = request.form.get('game_id')
    mensagem = request.form.get('mensagem')
    flash('Mensagem enviada (simulada).', 'success')
    return redirect(url_for('game.play', game_id=game_id))
