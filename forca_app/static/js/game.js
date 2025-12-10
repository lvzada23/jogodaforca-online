//-------------------------------------------------------------
// Atualiza a imagem do boneco da forca conforme erros
//-------------------------------------------------------------
function updateHangmanImage(errors) {
    const img = document.getElementById("hangman-image");
    if (!img) return;

    const maxImg = 6; // hangman0.png até hangman6.png
    const index = Math.min(errors, maxImg);

    img.src = `/static/img/hangman${index}.png`;
}


//-------------------------------------------------------------
// Valida input antes de enviar
//-------------------------------------------------------------
function validateGuess() {
    const input = document.getElementById("guess");
    if (!input) return true;

    const value = input.value.trim().toLowerCase();

    if (value.length !== 1 || !/[a-zç]/.test(value)) {
        alert("Digite apenas UMA letra válida.");
        return false;
    }

    return true;
}


//-------------------------------------------------------------
// Evita que o jogador envie múltiplas vezes
//-------------------------------------------------------------
function disableButton() {
    const button = document.getElementById("btn-guess");
    if (button) {
        button.disabled = true;
        button.innerText = "Enviando...";
    }
}


//-------------------------------------------------------------
// Função principal acionada no submit
//-------------------------------------------------------------
function handleGuess() {
    if (validateGuess()) {
        disableButton();
        return true; // permite enviar o formulário
    }
    return false;
}


//-------------------------------------------------------------
// Atualiza a palavra revelada no frontend (opcional)
// Usado se quiser criar dinâmica em tempo real via JS
//-------------------------------------------------------------
function updateWordDisplay(revealedLetters) {
    const wordContainer = document.getElementById("word-display");
    if (!wordContainer) return;

    wordContainer.innerText = revealedLetters.join(" ");
}


//-------------------------------------------------------------
// Exibir mensagens no topo (sucesso / erro)
//-------------------------------------------------------------
function showMessage(text, type = "info") {
    const msg = document.getElementById("game-message");
    if (!msg) return;

    msg.innerText = text;
    msg.className = "";

    if (type === "error") msg.classList.add("alert-error");
    if (type === "success") msg.classList.add("alert-success");
    if (type === "info") msg.classList.add("alert-info");
}


//-------------------------------------------------------------
// Executa ao carregar a página
//-------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    // Se um template passar variáveis para o JS, atualizamos tudo
    const errors = parseInt(document.body.dataset.errors || "0");
    updateHangmanImage(errors);
});
