from forca_app.seed import seed_app
from forca_app.extensions import db
from forca_app.models.user import User
from forca_app.services.word_service import WORDS


def test_seed_app_creates_users_and_words(app):
    seed_app(app)

    # check users
    with app.app_context():
        u1 = User.query.filter_by(email='alice@example.com').first()
        u2 = User.query.filter_by(email='bob@example.com').first()

        assert u1 is not None
        assert u2 is not None

    # check words were added
    assert 'sol' in WORDS['easy']
    assert 'criptografia' in WORDS['hard']