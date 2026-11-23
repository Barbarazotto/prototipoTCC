const form = document.getElementById("cadastroForm");

const senha = document.getElementById("senha");
const confirmarSenha = document.getElementById("confirmarSenha");
const toggleSenha = document.getElementById("toggleSenha");

let visivel = false;

toggleSenha.addEventListener("click", () => {
    visivel = !visivel;

    if (visivel) {
        senha.type = "text";
        toggleSenha.src = "https://img.icons8.com/ios-glyphs/30/000000/invisible.png";
    } else {
        senha.type = "password";
        toggleSenha.src = "https://img.icons8.com/ios-glyphs/30/000000/visible.png";
    }
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;

    if (senha.value !== confirmarSenha.value) {
        document.getElementById("mensagem").innerText =
            "As senhas não coincidem!";
        document.getElementById("mensagem").style.color = "red";
        return;
    }

    const resposta = await fetch("http://127.0.0.1:8000/usuarios", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome,
            email,
            senha: senha.value
        })
    });

    const dados = await resposta.json();

    document.getElementById("mensagem").innerText =
        dados.mensagem;

    document.getElementById("mensagem").style.color = "green";

    form.reset();
});