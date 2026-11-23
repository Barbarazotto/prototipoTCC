const usuario = JSON.parse(localStorage.getItem("usuario"));

const modalEdicao = document.getElementById("modalEdicao");
const abrirEdicao = document.getElementById("abrirEdicao");
const fecharEdicao = document.getElementById("fecharEdicao");
const cancelarEdicao = document.getElementById("cancelarEdicao");

const nomeEdicao = document.getElementById("nomeEdicao");
const emailEdicao = document.getElementById("emailEdicao");

const fotoPerfil = document.getElementById("fotoPerfil");
const previewFoto = document.getElementById("previewFoto");
const inicialEdicao = document.getElementById("inicialEdicao");

const removerFoto = document.getElementById("removerFoto");
const salvarEdicao = document.getElementById("salvarEdicao");

const mensagemEdicao = document.getElementById("mensagemEdicao");

const fotoUsuario = document.getElementById("fotoUsuario");
const inicialUsuario = document.getElementById("inicialUsuario");

const nomeUsuario = document.getElementById("nomeUsuario");
const emailUsuario = document.getElementById("emailUsuario");

const nomePerfil = document.getElementById("nomePerfil");
const emailPerfil = document.getElementById("emailPerfil");


// CONTROLAR SE A FOTO DEVE SER REMOVIDA

let fotoDeveSerRemovida = false;


/* VERIFICAÇÃO DO USUÁRIO */

if (!usuario) {

    window.location.href = "login.html";

} else {

    mostrarDadosUsuario();

}


/* MOSTRAR DADOS DO USUÁRIO */

function mostrarDadosUsuario() {

    nomeUsuario.innerText = usuario.nome;

    emailUsuario.innerText = usuario.email;

    nomePerfil.innerText = usuario.nome;

    emailPerfil.innerText = usuario.email;

    inicialUsuario.innerText =
        usuario.nome.charAt(0).toUpperCase();


    if (usuario.foto_perfil) {

        fotoUsuario.src =
            "http://127.0.0.1:8000/" + usuario.foto_perfil;

        fotoUsuario.style.display = "block";

        inicialUsuario.style.display = "none";

    } else {

        fotoUsuario.src = "";

        fotoUsuario.style.display = "none";

        inicialUsuario.style.display = "block";

    }

}


/* ABRIR MODAL */

abrirEdicao.addEventListener("click", () => {

    nomeEdicao.value = usuario.nome;

    emailEdicao.value = usuario.email;

    mensagemEdicao.style.display = "none";

    fotoDeveSerRemovida = false;

    fotoPerfil.value = "";


    if (usuario.foto_perfil) {

        previewFoto.src =
            "http://127.0.0.1:8000/" + usuario.foto_perfil;

        previewFoto.style.display = "block";

        inicialEdicao.style.display = "none";

    } else {

        previewFoto.src = "";

        previewFoto.style.display = "none";

        inicialEdicao.innerText =
            usuario.nome.charAt(0).toUpperCase();

        inicialEdicao.style.display = "block";

    }

    modalEdicao.classList.add("aberto");

});


/* FECHAR MODAL */

function fecharModal() {

    modalEdicao.classList.remove("aberto");

    fotoPerfil.value = "";

    fotoDeveSerRemovida = false;

}


fecharEdicao.addEventListener("click", fecharModal);

cancelarEdicao.addEventListener("click", fecharModal);


/* FECHAR CLICANDO FORA */

modalEdicao.addEventListener("click", (event) => {

    if (event.target === modalEdicao) {

        fecharModal();

    }

});


/* PREVISUALIZAÇÃO DA FOTO */

fotoPerfil.addEventListener("change", () => {

    const arquivo = fotoPerfil.files[0];

    if (!arquivo) {

        return;

    }


    const tiposPermitidos = [

        "image/jpeg",

        "image/png",

        "image/webp"

    ];


    if (!tiposPermitidos.includes(arquivo.type)) {

        mostrarMensagem(
            "Escolha uma imagem JPG, PNG ou WEBP.",
            "erro"
        );

        fotoPerfil.value = "";

        return;

    }


    // Se o usuário escolher uma nova foto,
    // não queremos mais remover a foto.

    fotoDeveSerRemovida = false;


    const leitor = new FileReader();


    leitor.onload = function (event) {

        previewFoto.src = event.target.result;

        previewFoto.style.display = "block";

        inicialEdicao.style.display = "none";

    };


    leitor.readAsDataURL(arquivo);

});


/* REMOVER FOTO */

removerFoto.addEventListener("click", () => {

    fotoPerfil.value = "";

    fotoDeveSerRemovida = true;

    previewFoto.src = "";

    previewFoto.style.display = "none";

    inicialEdicao.innerText =
        nomeEdicao.value.charAt(0).toUpperCase() || "U";

    inicialEdicao.style.display = "block";

});


/* SALVAR ALTERAÇÕES */

salvarEdicao.addEventListener("click", async () => {

    const novoNome = nomeEdicao.value.trim();
    const novoEmail = emailEdicao.value.trim();


    if (!novoNome || !novoEmail) {

        mostrarMensagem(
            "Preencha todos os campos.",
            "erro"
        );

        return;

    }


    salvarEdicao.disabled = true;

    salvarEdicao.innerText = "Salvando...";


    try {

        /* ATUALIZAR NOME E E-MAIL */

        const dados = new FormData();

        dados.append("nome", novoNome);

        dados.append("email", novoEmail);


        const respostaUsuario = await fetch(
            `http://127.0.0.1:8000/usuarios/${usuario.id}`,
            {
                method: "PUT",
                body: dados
            }
        );


        const resultadoUsuario =
            await respostaUsuario.json();


        if (!respostaUsuario.ok) {

            throw new Error(
                resultadoUsuario.detail ||
                "Não foi possível atualizar o perfil."
            );

        }


        /* REMOVER FOTO */

        if (
            fotoDeveSerRemovida &&
            !fotoPerfil.files.length &&
            usuario.foto_perfil
        ) {

            const respostaRemover = await fetch(
                `http://127.0.0.1:8000/usuarios/${usuario.id}/foto`,
                {
                    method: "DELETE"
                }
            );


            const resultadoRemover =
                await respostaRemover.json();


            if (!respostaRemover.ok) {

                throw new Error(
                    resultadoRemover.detail ||
                    "Não foi possível remover a foto."
                );

            }


            usuario.foto_perfil = null;

        }


        /* ATUALIZAR FOTO */

        if (fotoPerfil.files.length > 0) {

            const dadosFoto = new FormData();

            dadosFoto.append(
                "foto",
                fotoPerfil.files[0]
            );


            const respostaFoto = await fetch(
                `http://127.0.0.1:8000/usuarios/${usuario.id}/foto`,
                {
                    method: "POST",
                    body: dadosFoto
                }
            );


            const resultadoFoto =
                await respostaFoto.json();


            if (!respostaFoto.ok) {

                throw new Error(
                    resultadoFoto.detail ||
                    "Não foi possível atualizar a foto."
                );

            }


            usuario.foto_perfil =
                resultadoFoto.foto_perfil;

        }


        /* ATUALIZAR LOCALSTORAGE */

        usuario.nome = novoNome;

        usuario.email = novoEmail;


        localStorage.setItem(
            "usuario",
            JSON.stringify(usuario)
        );


        /* ATUALIZAR A PÁGINA */

        mostrarDadosUsuario();


        mostrarMensagem(
            "Perfil atualizado com sucesso!",
            "sucesso"
        );


        setTimeout(() => {

            fecharModal();

        }, 1200);


    } catch (erro) {

        console.error(erro);

        mostrarMensagem(
            erro.message ||
            "Ocorreu um erro ao atualizar o perfil.",
            "erro"
        );

    } finally {

        salvarEdicao.disabled = false;

        salvarEdicao.innerText =
            "Salvar alterações";

    }

});


/* MENSAGENS */

function mostrarMensagem(texto, tipo) {

    mensagemEdicao.innerText = texto;

    mensagemEdicao.style.display = "block";


    if (tipo === "erro") {

        mensagemEdicao.style.background =
            "#fff1f1";

        mensagemEdicao.style.color =
            "#dc2626";

    } else {

        mensagemEdicao.style.background =
            "#ecfdf3";

        mensagemEdicao.style.color =
            "#16a34a";

    }

}


/* SAIR */

document.getElementById("sair").addEventListener("click", () => {

    localStorage.removeItem("usuario");

    window.location.href = "login.html";

});