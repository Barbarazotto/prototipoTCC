
const form = document.getElementById("redefinirForm");

const novaSenha = document.getElementById("novaSenha");
const confirmarSenha = document.getElementById("confirmarSenha");

const mensagem = document.getElementById("mensagem");
const botao = document.getElementById("botaoRedefinir");

const token = new URLSearchParams(window.location.search).get("token");


/* MOSTRAR / ESCONDER SENHA */

function configurarOlho(campo, botaoOlho) {

    const imagem = botaoOlho.querySelector("img");

    const iconeOlhoFechado =
        "https://img.icons8.com/?size=100&id=987&format=png&color=000000";

    const iconeOlhoAberto =
        "https://img.icons8.com/?size=100&id=986&format=png&color=000000";

    botaoOlho.addEventListener("click", () => {

        if (campo.type === "password") {

            campo.type = "text";

            imagem.src = iconeOlhoAberto;
            imagem.alt = "Senha visível";

            botaoOlho.setAttribute(
                "aria-label",
                "Esconder senha"
            );

        } else {

            campo.type = "password";

            imagem.src = iconeOlhoFechado;
            imagem.alt = "Senha oculta";

            botaoOlho.setAttribute(
                "aria-label",
                "Mostrar senha"
            );

        }

    });

}


/* VERIFICAR TOKEN */

if (!token) {

    mensagem.innerText =
        "Link de recuperação inválido ou incompleto.";

    mensagem.style.color = "red";

    botao.disabled = true;

}


/* REDEFINIR SENHA */

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    if (!token) {
        return;
    }

    const senha = novaSenha.value;
    const confirmacao = confirmarSenha.value;


    if (senha !== confirmacao) {

        mensagem.innerText =
            "As senhas não são iguais.";

        mensagem.style.color = "red";

        return;

    }


    if (senha.length < 8) {

        mensagem.innerText =
            "A senha precisa ter pelo menos 8 caracteres.";

        mensagem.style.color = "red";

        return;

    }


    botao.disabled = true;
    botao.innerText = "Salvando...";

    mensagem.innerText = "";


    try {

        const resposta = await fetch(
            "http://127.0.0.1:8000/redefinir-senha",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    token: token,
                    nova_senha: senha
                })
            }
        );


        const dados = await resposta.json();


        if (resposta.ok) {

            mensagem.innerText =
                dados.mensagem || "Senha redefinida com sucesso!";

            mensagem.style.color = "green";

            form.reset();

            botao.innerText = "Senha alterada";


            setTimeout(() => {

                window.location.href = "login.html";

            }, 2500);


        } else {

            mensagem.innerText =
                dados.detail ||
                "Não foi possível redefinir sua senha.";

            mensagem.style.color = "red";

            botao.disabled = false;
            botao.innerText = "Salvar nova senha";

        }


    } catch (erro) {

        console.error(erro);

        mensagem.innerText =
            "Não foi possível conectar ao servidor.";

        mensagem.style.color = "red";

        botao.disabled = false;
        botao.innerText = "Salvar nova senha";

    }

});
