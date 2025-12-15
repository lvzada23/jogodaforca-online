from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from forca_app.models.user import User
from forca_app.extensions import db  # uses extensions.db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ----------------------------------------------------------
# Página de cadastro
# ----------------------------------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Verifica campos vazios
        if not name or not email or not password:
            flash("Preencha todos os campos!", "error")
            return redirect(url_for("auth.register"))

        # Verifica se o e-mail já existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("E-mail já registrado!", "error")
            return redirect(url_for("auth.register"))

        # Cria o novo usuário
        new_user = User(name=name, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Conta criada com sucesso! Faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ----------------------------------------------------------
# Página de login
# ----------------------------------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        # compatibilidade com templates: login.html usa name="senha"
        password = request.form.get("password") or request.form.get("senha")

        # validação básica
        if not email or not password:
            flash("Preencha e-mail e senha!", "error")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(email=email).first()

        # Usuário ou senha inválidos
        if not user or not user.check_password(password):
            flash("E-mail ou senha incorretos!", "error")
            return redirect(url_for("auth.login"))

        # Salva usuário na sessão
        session["user_id"] = user.id
        session["user_name"] = user.name
        session["user_email"] = user.email
        session["user_level"] = getattr(user, 'level', 10)
        session["user_points"] = getattr(user, 'points', 0)

        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("menu.index"))  # redireciona para o menu do jogo

    return render_template("login.html")


# ----------------------------------------------------------
# Logout
# ----------------------------------------------------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("auth.login"))
