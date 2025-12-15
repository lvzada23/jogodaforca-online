import random
import string

# ----------------------------------------------------------
# Letras mais frequentes na língua portuguesa
# (para o BOT parecer mais inteligente)
# ----------------------------------------------------------

LETTER_FREQUENCY = [
    'a', 'e', 'o', 's', 'r', 'i', 'n', 'd', 'm', 'u',
    't', 'c', 'l', 'p', 'v', 'g', 'h', 'q', 'b', 'f',
    'z', 'j', 'x', 'k', 'w', 'y'
]

# ----------------------------------------------------------
# Função principal para o BOT escolher uma letra
# ----------------------------------------------------------

def bot_choose_letter(word, revealed_letters, bot_attempts, difficulty="easy"):
    """
    word: palavra secreta
    revealed_letters: lista de letras já reveladas (ex: ['a', '_', '_', 'o'])
    bot_attempts: conjunto with letters already guessed by the bot
    difficulty: "easy", "medium", "hard"
    """

    # Normaliza dificuldade
    difficulty = difficulty.lower()

    # Converte para conjunto de letras já tentadas
    tried = set(bot_attempts or [])

    # Se houver letras na palavra que ainda não foram tentadas, tentamos primeiras
    for letra in LETTER_FREQUENCY:
        if letra in tried:
            continue
        if letra in word.lower():
            return letra

    # Senão, escolhe uma letra aleatória não tentada
    remaining = [c for c in string.ascii_lowercase if c not in tried]
    if not remaining:
        return random.choice(string.ascii_lowercase)
    return random.choice(remaining)
