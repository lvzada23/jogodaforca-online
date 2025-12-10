from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from extensions import db

from services.word_service import get_random_word
from services.game_logic import (
    create_game_state,
    process_player_guess,
    is_game_over,
    is_word_complete,
)
from services.bot_ai import bot_choose_letter

from models.user import User
from models.game import Game

game_bp = Blueprint("game", __name__, url_prefix="/game")


# ------------------------------------------------------------
# Tela inicial do jogo (escolha modo / dificuldade)
# ----------------------------------------------
