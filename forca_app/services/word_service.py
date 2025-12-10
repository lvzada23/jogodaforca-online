import random
# ----------------------------------------------------------
# Dicionário de palavras separadas por dificuldade
# ----------------------------------------------------------

WORDS = {
    "easy": [
        "casa", "bola", "gato", "pato", "mesa", "carro", "manga",
        "fogo", "arroz", "peixe", "vento", "luz", "cama"
    ],
    "medium": [
        "montanha", "brasil", "computador", "janela", "girassol",
        "cadeira", "escola", "secretaria", "viagem", "telefone"
    ],
    "hard": [
        "paralelepipedo", "otorrinolaringologista", "criptografia",
        "hidrocarboneto", "ressignificar", "inconstitucional",
        "termodinâmica", "microprocessador"
    ]
}

# ----------------------------------------------------------
# Retorna todas as palavras de uma dificuldade específica
# ----------------------------------------------------------

def get_words_by_difficulty(difficulty: str):
    difficulty = difficulty.lower()

    if difficulty not in WORDS:
        raise ValueError(f"Dificuldade desconhecida: {difficulty}")

    return WORDS[difficulty]


# ----------------------------------------------------------
# Retorna uma palavra aleatória da dificuldade selecionada
# ----------------------------------------------------------

def get_random_word(difficulty: str) -> str:
    words = get_words_by_difficulty(difficulty)
    return random.choice(words)


# ----------------------------------------------------------
# Função para adicionar palavras (opcional)
# Pode ser usada caso queira cadastrar novas palavras
# ----------------------------------------------------------

def add_word(difficulty: str, word: str):
    difficulty = difficulty.lower()

    if difficulty not in WORDS:
        raise ValueError(f"Dificuldade desconhecida: {difficulty}")

    if word not in WORDS[difficulty]:
        WORDS[difficulty].append(word.lower())

