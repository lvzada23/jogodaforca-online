import traceback
import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from run import create_app
from forca_app.extensions import db
from forca_app.models.user import User

app = create_app()

with app.app_context():
    email = 'debug_user@example.com'
    try:
        existing = User.query.filter_by(email=email).first()
        print('existing:', existing)
    except Exception as e:
        print('Error during query:')
        traceback.print_exc()

    try:
        u = User(name='Debug User', email=email)
        u.set_password('Debug123')
        db.session.add(u)
        db.session.commit()
        print('User created:', u.id)
    except Exception as e:
        print('Error during create:')
        traceback.print_exc()
