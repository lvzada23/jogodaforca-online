from . import db

class LevelHistory(db.Model):
    __tablename__ = "level_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    nivel_anterior = db.Column(db.Integer, nullable=False)
    nivel_novo = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(50), nullable=False)  # vitória, derrota, penalidade...

    def __repr__(self):
        return f"<LevelChange User {self.user_id}: {self.nivel_anterior} -> {self.nivel_novo}>"
