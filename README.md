# TripInsight

**Plataforma web para planejamento e compartilhamento de experiências de viagem.**

O TripInsight é um projeto desenvolvido como Trabalho de Conclusão de Curso (TCC) do curso de Desenvolvimento de Sistemas do SENAI.

A plataforma tem como objetivo auxiliar usuários no planejamento de viagens, permitindo organizar informações, conhecer experiências compartilhadas e acompanhar aspectos financeiros.

---

## Sobre o projeto

O TripInsight foi desenvolvido para oferecer um ambiente digital no qual os usuários possam consultar e compartilhar experiências relacionadas a viagens.

O sistema reúne funcionalidades como:

- Cadastro e autenticação de usuários.
- Recuperação e redefinição de senha por e-mail.
- Edição de informações do perfil.
- Gerenciamento de foto de perfil.
- Visualização e compartilhamento de experiências de viagem.
- Sistema de favoritos.
- Comentários em experiências.
- Controle financeiro de viagens.
- Área de dicas e informações.

## Tecnologias utilizadas

### Frontend
- HTML5: estrutura das páginas.
- CSS3: estilização e responsividade.
- JavaScript: interatividade e comunicação com a API.
- Fetch API: requisições ao backend.

### Backend
- Python: linguagem utilizada no desenvolvimento do servidor.
- FastAPI: criação das rotas e serviços da API.
- SQLAlchemy: comunicação e manipulação dos dados.
- PyMySQL: conexão com o banco de dados MySQL.

### Banco de dados
- MySQL: armazenamento das informações dos usuários e demais registros do sistema.

### Outras ferramentas
- Visual Studio Code.
- Git e GitHub.
- Swagger UI: documentação e testes das rotas da API.

---

**Observação:** O arquivo `.env` deve ser criado individualmente no computador de cada desenvolvedor e não deve ser enviado ao GitHub.

---

# Como executar o projeto

## 1. Pré-requisitos

Antes de iniciar, é necessário ter instalado:

- Python.
- MySQL Server.
- Visual Studio Code.
- Git.
- Extensão Live Server do Visual Studio Code.

## 2. Clonar o repositório

Abra o terminal e execute:

```bash
git clone https://github.com/Barbarazotto/prototipoTCC.git
```

Entre na pasta do projeto:

```bash
cd prototipoTCC
```

## 3. Configurar o ambiente virtual

Entre na pasta do backend:

```bash
cd backend
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```bash
.venv\Scripts\activate
```

No Git Bash, caso necessário:

```bash
source .venv/Scripts/activate
```

## 4. Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt
```

Esse comando instala as bibliotecas necessárias para executar o backend.

## 5. Configurar o banco de dados

O projeto utiliza MySQL.

Primeiro, inicie o MySQL e crie o banco de dados:

```sql
CREATE DATABASE tripinsight;
```

Depois, configure a conexão no arquivo `.env`, localizado dentro da pasta `backend`.

Exemplo de configuração:

```env
DATABASE_URL=mysql+pymysql://USUARIO:SENHA@localhost/tripinsight

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_de_aplicativo
EMAIL_FROM=seu_email@gmail.com

FRONTEND_URL=http://127.0.0.1:5500/frontend
```

Substitua os valores de exemplo pelas configurações do ambiente local.

**Importante:** Nunca compartilhe ou publique suas senhas do banco de dados ou do e-mail.

O envio de e-mails para recuperação de senha depende da configuração correta do serviço SMTP.

## 6. Executar o backend (FastAPI)

Certifique-se de estar dentro da pasta `backend` e com o ambiente virtual ativado.

Execute:

```bash
python -m uvicorn main:app --reload
```

Se tudo estiver configurado corretamente, o servidor ficará disponível em:

**API:**

http://127.0.0.1:8000

**Documentação interativa do FastAPI (Swagger):**

http://127.0.0.1:8000/docs

**Documentação alternativa:**

http://127.0.0.1:8000/redoc

O Swagger permite visualizar as rotas disponíveis, consultar os parâmetros e realizar testes diretamente pela interface do navegador.

Para interromper o servidor, utilize:

```bash
CTRL + C
```

## 7. Executar o frontend

Com o backend funcionando:

1. Abra a pasta do projeto no Visual Studio Code.
2. Localize a pasta `frontend`.
3. Abra o arquivo `login.html`.
4. Clique com o botão direito.
5. Selecione **Open with Live Server**.

O frontend ficará disponível, normalmente, em:

http://127.0.0.1:5500/frontend/login.html

A página inicial também pode ser acessada por:

http://127.0.0.1:5500/frontend/index.html

O endereço e a porta podem variar conforme a configuração do Live Server.

**Atenção:** Para utilizar as funcionalidades que dependem do banco de dados, o backend e o MySQL também precisam estar em execução.

---

## Endpoints da API

As rotas do sistema são desenvolvidas no arquivo `backend/main.py`.

Entre as rotas de autenticação e recuperação de senha estão:

| Método | Rota | Finalidade |
|---|---|---|
| POST | `/usuarios` | Cadastrar usuário. |
| POST | `/login` | Realizar autenticação. |
| POST | `/recuperar-senha` | Solicitar recuperação de senha. |
| POST | `/redefinir-senha` | Cadastrar uma nova senha. |
| PUT | `/usuarios/{id}` | Atualizar informações do usuário. |

A lista completa e os parâmetros das rotas podem ser consultados em:

http://127.0.0.1:8000/docs

---

## Segurança

Algumas medidas adotadas no projeto:

- Armazenamento de configurações privadas no arquivo `.env`.
- Proteção de arquivos sensíveis por meio do `.gitignore`.
- Utilização de hash para armazenamento das senhas.
- Utilização de tokens temporários na recuperação de senha.
- Validação das informações recebidas pela API.

Os arquivos de configuração individuais não devem ser compartilhados publicamente.

---

## Desenvolvedores

Projeto desenvolvido como Trabalho de Conclusão de Curso do curso de Desenvolvimento de Sistemas do SENAI.

**Integrantes:**
- Bárbara Santana
- Bruna Luise
- Bruna Veloso

**Instituição:** SENAI

**Repositório:** https://github.com/Barbarazotto/prototipoTCC

---

## Considerações finais

O TripInsight representa a aplicação prática dos conhecimentos adquiridos durante o curso de Desenvolvimento de Sistemas, integrando desenvolvimento frontend, backend, banco de dados, APIs e controle de versão.

O projeto busca oferecer uma solução funcional e organizada para auxiliar no planejamento e compartilhamento de experiências de viagem.
