const categorias = document.querySelectorAll(".categoria");
const cards = document.querySelectorAll(".card-dica");

const pesquisa = document.getElementById("pesquisaDica");
const buscar = document.getElementById("buscarDica");

const nenhumaDica = document.getElementById("nenhumaDica");


function filtrarDicas() {

    const texto = pesquisa.value.toLowerCase().trim();

    const categoriaAtiva =
        document.querySelector(".categoria.ativo").dataset.categoria;

    let encontrou = false;


    cards.forEach((card) => {

        const categoria = card.dataset.categoria;

        const titulo =
            card.dataset.titulo.toLowerCase();

        const conteudo =
            card.innerText.toLowerCase();


        const correspondeCategoria =
            categoriaAtiva === "todas" ||
            categoria === categoriaAtiva;


        const correspondePesquisa =
            texto === "" ||
            titulo.includes(texto) ||
            conteudo.includes(texto);


        if (correspondeCategoria && correspondePesquisa) {

            card.style.display = "block";

            encontrou = true;

        } else {

            card.style.display = "none";

        }

    });


    if (encontrou) {

        nenhumaDica.style.display = "none";

    } else {

        nenhumaDica.style.display = "block";

    }

}


/* CATEGORIAS */

categorias.forEach((botao) => {

    botao.addEventListener("click", () => {

        categorias.forEach((item) => {
            item.classList.remove("ativo");
        });


        botao.classList.add("ativo");


        filtrarDicas();

    });

});


/* PESQUISA */

buscar.addEventListener("click", () => {

    filtrarDicas();

});


pesquisa.addEventListener("keyup", (event) => {

    if (event.key === "Enter") {

        filtrarDicas();

    }

});