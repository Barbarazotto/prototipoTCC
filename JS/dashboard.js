
/* USUÁRIO LOGADO */

const usuario = JSON.parse(
    localStorage.getItem("usuario")
);


/* VERIFICAÇÃO */

if (!usuario) {
    window.location.href = "login.html";
} else {
    mostrarUsuario();
    carregarEstatisticas();
}


/* MOSTRAR USUÁRIO */

function mostrarUsuario() {

    const nomeUsuario = document.getElementById("nomeUsuario");
    const inicialUsuario = document.getElementById("inicialUsuario");
    const fotoUsuario = document.getElementById("fotoUsuario");

    nomeUsuario.innerText = usuario.nome;

    if (usuario.nome) {
        inicialUsuario.innerText =
            usuario.nome.charAt(0).toUpperCase();
    }

    if (usuario.foto_perfil) {

        fotoUsuario.src =
            "http://127.0.0.1:8000/" + usuario.foto_perfil;

        fotoUsuario.style.display = "block";
        inicialUsuario.style.display = "none";

    } else {

        fotoUsuario.style.display = "none";
        inicialUsuario.style.display = "flex";

    }

}


/* CARREGAR ESTATÍSTICAS */

async function carregarEstatisticas() {

    try {

        const resposta = await fetch(
            `http://127.0.0.1:8000/usuarios/${usuario.id}/dashboard`
        );

        if (!resposta.ok) {
            throw new Error("Não foi possível carregar as estatísticas.");
        }

        const dados = await resposta.json();

        document.getElementById("totalViagens").innerText =
            dados.viagens ?? 0;

        document.getElementById("orcamentoTotal").innerText =
            Number(dados.orcamento_total ?? 0).toLocaleString(
                "pt-BR",
                {
                    style: "currency",
                    currency: "BRL"
                }
            );

        document.getElementById("totalFavoritos").innerText =
            dados.favoritos ?? 0;

        document.getElementById("totalExperiencias").innerText =
            dados.experiencias ?? 0;

    } catch (erro) {

        console.error("Erro ao carregar estatísticas:", erro);

    }

}


/* PLANEJAR VIAGEM */

const planejarViagem =
    document.getElementById("planejarViagem");

const planejarViagemVazio =
    document.getElementById("planejarViagemVazio");


function abrirPlanejamento() {

    alert(
        "A área de planejamento de viagens será adicionada em breve."
    );

}


if (planejarViagem) {
    planejarViagem.addEventListener("click", abrirPlanejamento);
}

if (planejarViagemVazio) {
    planejarViagemVazio.addEventListener("click", abrirPlanejamento);
}


/* SAIR DA CONTA */

function sair() {

    localStorage.removeItem("usuario");

    window.location.href = "login.html";

}
