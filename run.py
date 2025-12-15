from flask import Flask, redirect, url_for
import os
from types import SimpleNamespace

from forca_app.extensions import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    # Config básica
    app.config['SECRET_KEY'] = os.environ.get('FORCA_SECRET', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///forca.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # inicializa extensões
    db.init_app(app)
    from forca_app.extensions import migrate
    migrate.init_app(app, db)

    # registrar blueprints
    from forca_app.routes.auth_routes import auth_bp
    from forca_app.routes.menu_routes import menu_bp
    from forca_app.routes.game_routes import game_bp
    from forca_app.routes.user_routes import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(user_bp)

    # Rota raiz: redireciona para o menu do jogo
    from flask import redirect, url_for, session
    from forca_app.models.user import User

    @app.route('/')
    def home():
        return redirect(url_for('menu.index'))

    # Context processor: expõe `current_user` para templates usando sessão
    @app.context_processor
    def inject_current_user():
        try:
            user_id = session.get('user_id')
            if user_id:
                try:
                    user = db.session.get(User, user_id)
                except Exception:
                    user = None

                # If the DB lookup failed but we still have session info, return a lightweight object
                if not user:
                    name = session.get('user_name') or ''
                    email = session.get('user_email') or ''
                    level = session.get('user_level') or None
                    points = session.get('user_points') or 0
                    if name or email or level or points:
                        user = SimpleNamespace(
                            id=user_id,
                            name=name,
                            nome=name,
                            email=email,
                            level=level,
                            nivel=level,
                            points=points,
                            pontos=points,
                            total_vitórias=0,
                            taxa_vitória=0,
                            sequencia_vitórias=0,
                        )

                return {"current_user": user}
            return {"current_user": None}
        except Exception:
            return {"current_user": None}

    @app.cli.command('create-db')
    def create_db():
        """Cria o banco de dados (SQLite)"""
        with app.app_context():
            db.create_all()
            print('Banco criado')

    @app.cli.command('seed-db')
    def seed_db():
        """Insere dados iniciais de exemplo: usuários e palavras."""
        from forca_app.seed import seed_app

        seed_app(app)
        print('Seed concluído')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
