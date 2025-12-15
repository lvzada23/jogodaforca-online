from flask import Flask, redirect, url_for
import os

from forca_app.extensions import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    # Config básica
    app.config['SECRET_KEY'] = os.environ.get('FORCA_SECRET', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///forca.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # inicializa extensões
    db.init_app(app)

    # registrar blueprints
    from forca_app.routes.auth_routes import auth_bp
    from forca_app.routes.menu_routes import menu_bp
    from forca_app.routes.game_routes import game_bp
    from forca_app.routes.user_routes import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(user_bp)

    # Rota raiz: redireciona para o menu (evita 404 em /)
    @app.route('/')
    def root():
        return redirect(url_for('menu.index'))

    # Disponibiliza `current_user` nos templates com base na sessão
    @app.context_processor
    def inject_current_user():
        from flask import session
        if 'user_id' in session:
            # import local para evitar import cycles
            from forca_app.models.user import User
            user = User.query.get(session.get('user_id'))
            return {'current_user': user}
        return {'current_user': None}

    @app.cli.command('create-db')
    def create_db():
        """Cria o banco de dados (SQLite)"""
        with app.app_context():
            db.create_all()
            print('Banco criado')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
