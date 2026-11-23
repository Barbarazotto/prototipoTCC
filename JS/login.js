const form = document.getElementById("loginForm");

const senha = document.getElementById("senha");

const mostrarSenha = document.getElementById("mostrarSenha");


/* MOSTRAR / ESCONDER SENHA */

mostrarSenha.addEventListener("click", () => {

    if (senha.type === "password") {

        senha.type = "text";

        mostrarSenha.setAttribute(
            "aria-label",
            "Esconder senha"
        );

    } else {

        senha.type = "password";

        mostrarSenha.setAttribute(
            "aria-label",
            "Mostrar senha"
        );

    }

});


/* LOGIN */

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const email =
        document.getElementById("email").value;

    const senhaValor =
        document.getElementById("senha").value;

    const msg =
        document.getElementById("mensagem");


    try {

        const resposta = await fetch(
            "http://127.0.0.1:8000/login",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    senha: senhaValor
                })
            }
        );


        const dados = await resposta.json();


        if (resposta.ok) {

            msg.innerText =
                "Login realizado com sucesso!";

            msg.style.color = "green";


            localStorage.setItem(
                "usuario",
                JSON.stringify(dados.usuario)
            );


            setTimeout(() => {

                window.location.href = "perfil.html";

            }, 500);


        } else {

            msg.innerText =
                dados.detail ||
                "Email ou senha incorretos!";

            msg.style.color = "red";

        }


    } catch (erro) {

        console.error(erro);

        msg.innerText =
            "Não foi possível conectar ao servidor.";

        msg.style.color = "red";

    }

});
