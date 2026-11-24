
const form = document.getElementById("cadastroForm");

const senha = document.getElementById("senha");
const confirmarSenha = document.getElementById("confirmarSenha");
const toggleSenha = document.getElementById("toggleSenha");
const mensagem = document.getElementById("mensagem");

let visivel = false;

// Mostrar ou esconder senha
toggleSenha.addEventListener("click", () => {
    visivel = !visivel;

    if (visivel) {
        senha.type = "text";
        toggleSenha.src =
            "https://img.icons8.com/ios-glyphs/30/000000/invisible.png";
    } else {
        senha.type = "password";
        toggleSenha.src =
            "https://img.icons8.com/ios-glyphs/30/000000/visible.png";
    }
});

// Realizar cadastro
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();

    if (senha.value !== confirmarSenha.value) {
        mensagem.innerText = "As senhas não coincidem!";
        mensagem.style.color = "red";
        return;
    }

    try {
        const resposta = await fetch(
            "http://127.0.0.1:8000/usuarios",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    nome,
                    email,
                    senha: senha.value
                })
            }
        );

        const dados = await resposta.json();

        if (resposta.ok) {
            mensagem.innerText =
                "Cadastro realizado com sucesso! Redirecionando para o login...";

            mensagem.style.color = "green";

            form.reset();

            setTimeout(() => {
                window.location.href = "login.html";
            }, 1500);

        } else {
            mensagem.innerText =
                dados.detail || dados.mensagem || "Não foi possível realizar o cadastro.";

            mensagem.style.color = "red";
        }

    } catch (erro) {
        console.error(erro);

        mensagem.innerText =
            "Não foi possível conectar ao servidor.";

        mensagem.style.color = "red";
    }
});
