
const API_URL = "http://127.0.0.1:8000";

const usuario = JSON.parse(localStorage.getItem("usuario"));

const formExperiencia = document.getElementById("formExperiencia");
const areaFormulario = document.getElementById("areaFormulario");

const abrirFormulario = document.getElementById("abrirFormulario");
const fecharFormulario = document.getElementById("fecharFormulario");
const cancelarFormulario = document.getElementById("cancelarFormulario");

const listaExperiencias = document.getElementById("listaExperiencias");
const contadorExperiencias = document.getElementById("contadorExperiencias");

const mensagemFormulario = document.getElementById("mensagemFormulario");
const botaoEnviar = document.getElementById("botaoEnviar");


/* VERIFICAR USUÁRIO */

if (!usuario) {
    window.location.href = "login.html";
}


/* ABRIR FORMULÁRIO */

function abrirAreaFormulario() {
    areaFormulario.classList.add("aberto");

    areaFormulario.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

abrirFormulario.addEventListener("click", abrirAreaFormulario);


/* FECHAR FORMULÁRIO */

function fecharAreaFormulario() {
    areaFormulario.classList.remove("aberto");
    formExperiencia.reset();

    mensagemFormulario.innerText = "";
    mensagemFormulario.className = "mensagem";
}

fecharFormulario.addEventListener("click", fecharAreaFormulario);
cancelarFormulario.addEventListener("click", fecharAreaFormulario);


/* ABRIR FORMULÁRIO PELO LINK */

if (window.location.hash === "#publicar") {
    abrirAreaFormulario();
}


/* CARREGAR EXPERIÊNCIAS */

async function carregarExperiencias() {
    try {
        listaExperiencias.innerHTML = `
            <div class="carregando">
                <i class="fa-solid fa-spinner fa-spin"></i>
                Carregando experiências...
            </div>
        `;

        const resposta = await fetch(`${API_URL}/experiencias`);

        if (!resposta.ok) {
            throw new Error("Não foi possível carregar as experiências.");
        }

        const experiencias = await resposta.json();

        listaExperiencias.innerHTML = "";

        atualizarContador(experiencias.length);

        if (experiencias.length === 0) {
            listaExperiencias.innerHTML = `
                <div class="vazio">
                    <i class="fa-solid fa-plane"></i>

                    <h3>Nenhuma experiência publicada</h3>

                    <p>
                        Seja a primeira pessoa a compartilhar
                        uma história com a comunidade!
                    </p>
                </div>
            `;

            return;
        }

        experiencias.forEach((experiencia) => {
            const card = criarCardExperiencia(experiencia);
            listaExperiencias.appendChild(card);
        });

    } catch (erro) {
        console.error("Erro ao carregar experiências:", erro);

        listaExperiencias.innerHTML = `
            <div class="erro-listagem">
                Não foi possível carregar as experiências.
                Verifique se o servidor está funcionando.
            </div>
        `;
    }
}


/* ATUALIZAR CONTADOR */

function atualizarContador(total) {
    contadorExperiencias.innerText =
        total === 1
            ? "1 experiência"
            : `${total} experiências`;
}


/* CRIAR CARD */

function criarCardExperiencia(experiencia) {
    const card = document.createElement("article");

    card.className = "card-experiencia";

    const nomeUsuario = escaparHTML(
        experiencia.nome_usuario || "Viajante"
    );

    const destino = escaparHTML(
        experiencia.destino || "Destino não informado"
    );

    const titulo = escaparHTML(
        experiencia.titulo || "Sem título"
    );

    const relato = escaparHTML(
        experiencia.relato || ""
    );

    const inicial = nomeUsuario.charAt(0).toUpperCase();

    const data = experiencia.data_publicacao
        ? new Date(experiencia.data_publicacao).toLocaleDateString("pt-BR")
        : "";

    const foto = experiencia.foto_perfil_usuario
        ? `${API_URL}/${experiencia.foto_perfil_usuario}`
        : null;

    const gasto = experiencia.gasto_total !== null &&
                  experiencia.gasto_total !== undefined
        ? Number(experiencia.gasto_total).toLocaleString("pt-BR", {
            style: "currency",
            currency: "BRL"
        })
        : null;

    const avaliacao = Number(experiencia.avaliacao) || 0;

    const estrelas = "★".repeat(avaliacao) +
                     "☆".repeat(5 - avaliacao);

    card.innerHTML = `
        <div class="card-topo">

            <div class="avatar-usuario">
                ${
                    foto
                        ? `<img src="${escaparHTML(foto)}" alt="Foto de ${nomeUsuario}">`
                        : inicial
                }
            </div>

            <div class="informacoes-usuario">
                <h3>${nomeUsuario}</h3>
                <span>${data}</span>
            </div>

        </div>

        <p class="destino-card">
            <i class="fa-solid fa-location-dot"></i>
            ${destino}
        </p>

        <h2 class="titulo-card">
            ${titulo}
        </h2>

        <p class="relato-card">
            ${relato}
        </p>

        <div class="informacoes-card">

            ${
                gasto
                    ? `
                        <span>
                            <i class="fa-solid fa-wallet"></i>
                            ${gasto}
                        </span>
                    `
                    : ""
            }

            ${
                avaliacao
                    ? `
                        <span class="estrelas">
                            ${estrelas}
                        </span>
                    `
                    : ""
            }

        </div>
    `;

    return card;
}


/* PROTEGER TEXTOS */

function escaparHTML(texto) {
    return String(texto).replace(/[&<>"']/g, (caractere) => {
        const caracteres = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;"
        };

        return caracteres[caractere];
    });
}


/* PUBLICAR EXPERIÊNCIA */

formExperiencia.addEventListener("submit", async (event) => {
    event.preventDefault();

    const destino = document.getElementById("destino").value.trim();
    const titulo = document.getElementById("titulo").value.trim();
    const relato = document.getElementById("relato").value.trim();

    const gastoTotal = document.getElementById("gastoTotal").value;
    const avaliacao = document.getElementById("avaliacao").value;

    if (!destino || !titulo || !relato) {
        mostrarMensagem(
            "Preencha os campos obrigatórios.",
            "erro"
        );

        return;
    }

    botaoEnviar.disabled = true;
    botaoEnviar.innerText = "Publicando...";

    try {
        const dados = new FormData();

        dados.append("destino", destino);
        dados.append("titulo", titulo);
        dados.append("relato", relato);

        if (gastoTotal !== "") {
            dados.append("gasto_total", gastoTotal);
        }

        if (avaliacao !== "") {
            dados.append("avaliacao", avaliacao);
        }

        const resposta = await fetch(
            `${API_URL}/usuarios/${usuario.id}/experiencias`,
            {
                method: "POST",
                body: dados
            }
        );

        const resultado = await resposta.json();

        if (!resposta.ok) {
            throw new Error(
                resultado.detail ||
                "Não foi possível publicar sua experiência."
            );
        }

        mostrarMensagem(
            "Experiência publicada com sucesso!",
            "sucesso"
        );

        formExperiencia.reset();

        await carregarExperiencias();

        setTimeout(() => {
            fecharAreaFormulario();

            window.scrollTo({
                top: document.querySelector(".secao-experiencias").offsetTop - 30,
                behavior: "smooth"
            });
        }, 1200);

    } catch (erro) {
        console.error("Erro ao publicar experiência:", erro);

        mostrarMensagem(
            erro.message ||
            "Ocorreu um erro ao publicar sua experiência.",
            "erro"
        );

    } finally {
        botaoEnviar.disabled = false;
        botaoEnviar.innerText = "Publicar experiência";
    }
});


/* MENSAGENS DO FORMULÁRIO */

function mostrarMensagem(texto, tipo) {
    mensagemFormulario.innerText = texto;
    mensagemFormulario.className = `mensagem ${tipo}`;
}


/* INICIAR PÁGINA */

carregarExperiencias();
