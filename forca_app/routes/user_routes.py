from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from forca_app.extensions import db
from forca_app.models.user import User
from forca_app.models.game import Game

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    games = Game.query.filter((Game.player1_id == user_id) | (Game.player2_id == user_id)).order_by(Game.data_fim.desc()).all()

    return render_template('profile.html', games=games)


@user_bp.route('/change-password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('auth.login'))

    user = db.session.get(User, session.get('user_id'))
    current = request.form.get('current_password')
    new = request.form.get('new_password')
    confirm = request.form.get('confirm_new_password')

    if not user or not user.check_password(current):
        flash('Senha atual incorreta.', 'error')
        return redirect(url_for('user.profile'))

    if new != confirm:
        flash('As senhas não coincidem.', 'error')
        return redirect(url_for('user.profile'))

    user.set_password(new)
    db.session.commit()
    flash('Senha atualizada.', 'success')
    return redirect(url_for('user.profile'))


@user_bp.route('/delete', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('auth.login'))

    user = db.session.get(User, session.get('user_id'))
    if user:
        # Remover jogos relacionados (opcional)
        Game.query.filter((Game.player1_id == user.id) | (Game.player2_id == user.id)).delete()
        db.session.delete(user)
        db.session.commit()

    session.clear()
    flash('Conta excluída com sucesso.', 'success')
    return redirect(url_for('auth.register'))
