from flask import Blueprint, render_template, request, session, redirect, url_for, flash

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