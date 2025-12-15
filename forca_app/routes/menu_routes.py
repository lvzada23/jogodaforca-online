from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from forca_app.extensions import db
from forca_app.models.game import Game
from forca_app.services.word_service import get_random_word


menu_bp = Blueprint("menu", __name__, url_prefix="/menu")


# ------------------------------------------------------------
# Tela principal do menu do jogo
# ------------------------------------------------------------
@menu_bp.route("/", methods=["GET", "POST"])
def index():
    # Exige login para acessar o menu
    if "user_id" not in session:
        flash("Você precisa estar logado para jogar.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        mode = request.form.get("mode")
        difficulty = request.form.get("difficulty")

        # Validação simples
        if mode not in ["singleplayer", "multiplayer"]:
            flash("Modo de jogo inválido!", "error")
            return redirect(url_for("menu.index"))

        # Cria uma nova partida
        palavra = get_random_word(difficulty or "easy")
        new_game = Game(player1_id=session.get("user_id"), modo=mode, dificuldade=difficulty or "easy", palavra=palavra)
        db.session.add(new_game)
        db.session.commit()

        return redirect(url_for('game.play', game_id=new_game.id))

    # Renderiza a página do menu
    return render_template("index.html")