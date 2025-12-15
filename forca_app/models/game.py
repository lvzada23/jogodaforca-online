from . import db
from datetime import datetime

class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)

    # Jogadores
    player1_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    player2_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # pode ser BOT

    modo = db.Column(db.String(20), nullable=False)  # singleplayer ou multiplayer
    dificuldade = db.Column(db.String(20), nullable=False)  # easy, medium, hard

    palavra = db.Column(db.String(100), nullable=False)
    letras_erradas = db.Column(db.String(20), default="")
    letras_certas = db.Column(db.String(20), default="")
    tentativas_restantes = db.Column(db.Integer, default=6)

    rodada_atual = db.Column(db.Integer, default=1)  # alterna player1/player2

    # Suporte a jogo multi-rodada
    rounds_total = db.Column(db.Integer, default=2)  # número de rodadas (ex: 2 -> cada jogador joga 1)
    rounds_completed = db.Column(db.Integer, default=0)
    wins_p1 = db.Column(db.Integer, default=0)
    wins_p2 = db.Column(db.Integer, default=0)

    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime, nullable=True)

    vencedor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    

    def __repr__(self):
        return f"<Game {self.id} - {self.modo} - Palavra: {self.palavra}>"
