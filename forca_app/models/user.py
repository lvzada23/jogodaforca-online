from forca_app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    level = db.Column(db.Integer, default=10)
    points = db.Column(db.Integer, default=0)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # Backwards compatible properties (if other code uses Portuguese names)
    @property
    def nome(self):
        return self.name

    @property
    def senha_hash(self):
        return self.password_hash

    @property
    def nivel(self):
        return self.level

    @property
    def pontos(self):
        return self.points

    def __repr__(self):
        return f"<User {self.name} - Level {self.level}>"
