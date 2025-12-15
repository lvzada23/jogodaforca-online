from forca_app.extensions import db


def seed_app(app):
    """Popula o banco com dados iniciais (usuários e palavras).

    Usa `app` para criar contexto e garantir que as tabelas existem antes de inserir.
    """
    from forca_app.models.user import User
    from forca_app.services.word_service import add_word

    with app.app_context():
        db.create_all()

        if not User.query.filter_by(email="alice@example.com").first():
            u1 = User(name="Alice", email="alice@example.com")
            u1.set_password("password")
            db.session.add(u1)

        if not User.query.filter_by(email="bob@example.com").first():
            u2 = User(name="Bob", email="bob@example.com")
            u2.set_password("password")
            db.session.add(u2)

        extras = {
            "easy": ["sol", "lua", "mar"],
            "medium": ["janela", "viagem"],
            "hard": ["criptografia", "microprocessador"],
        }

        for diff, words in extras.items():
            for w in words:
                try:
                    add_word(diff, w)
                except Exception:
                    pass

        db.session.commit()
