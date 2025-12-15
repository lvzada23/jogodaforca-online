from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from run import create_app
from forca_app.extensions import db

app = create_app()
with app.app_context():
    db.create_all()
    print('DB tables created')
