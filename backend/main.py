
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy import func

from pwdlib import PasswordHash
from dotenv import load_dotenv

from email.message import EmailMessage
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote
import smtplib
import hashlib
import secrets
import ssl
import os
import shutil

from database import Base, engine, SessionLocal
import models

from models import (
    Usuario,
    Experiencia,
    Favorito,
    Comentario,
    ControleFinanceiro,
    RecuperacaoSenha
)

from schemas import (
    UsuarioCreate,
    LoginSchema,
    RecuperarSenhaSchema,
    RedefinirSenhaSchema,
    ExperienciaCreate,
    FavoritoCreate,
    ComentarioCreate,
    ControleFinanceiroCreate
)


# CONFIGURAÇÕES

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

password_hash = PasswordHash.recommended()

app = FastAPI(title="TripInsight API")


# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PASTAS DE ARQUIVOS

PASTA_FOTOS = "uploads/perfil"

os.makedirs(PASTA_FOTOS, exist_ok=True)
os.makedirs("uploads", exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# BANCO DE DADOS

Base.metadata.create_all(bind=engine)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# FUNÇÕES AUXILIARES

def buscar_usuario(usuario_id, db):

    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return usuario


def buscar_experiencia(experiencia_id, db):

    experiencia = db.query(Experiencia).filter(
        Experiencia.id == experiencia_id
    ).first()

    if not experiencia:
        raise HTTPException(
            status_code=404,
            detail="Experiência não encontrada."
        )

    return experiencia


# FORMATAÇÃO DAS EXPERIÊNCIAS

def formatar_experiencia(experiencia):

    return {
        "id": experiencia.id,
        "usuario_id": experiencia.usuario_id,
        "nome_usuario": experiencia.usuario.nome,
        "foto_perfil_usuario": experiencia.usuario.foto_perfil,
        "destino": experiencia.destino,
        "titulo": experiencia.titulo,
        "relato": experiencia.relato,
        "gasto_total": experiencia.gasto_total,
        "avaliacao": experiencia.avaliacao,
        "data_publicacao": experiencia.data_publicacao
    }


# GERENCIAMENTO DE SENHAS

def gerar_hash_senha(senha):

    return password_hash.hash(senha)


def verificar_senha(senha_digitada, senha_salva):

    # Verifica senhas novas, armazenadas com Argon2.

    if senha_salva.startswith("$argon2"):

        try:
            senha_valida = password_hash.verify(
                senha_digitada,
                senha_salva
            )

            return senha_valida, False

        except Exception:
            return False, False

    # Compatibilidade temporária com contas antigas
    # que ainda possuem senha em texto puro.

    if senha_digitada == senha_salva:
        return True, True

    return False, False


# ENVIO DE E-MAIL

def enviar_email_recuperacao(destinatario, link):

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD", "").replace(" ", "")
    email_from = os.getenv("EMAIL_FROM", smtp_user)

    if not all([
        smtp_host,
        smtp_user,
        smtp_password,
        email_from
    ]):
        raise RuntimeError(
            "As configurações SMTP estão incompletas."
        )

    mensagem = EmailMessage()

    mensagem["Subject"] = "Recuperação de senha - TripInsight"
    mensagem["From"] = email_from
    mensagem["To"] = destinatario

    mensagem.set_content(
        f"""
Olá!

Recebemos uma solicitação para redefinir a senha
da sua conta no TripInsight.

Para criar uma nova senha, acesse o link abaixo:

{link}

Este link é válido por 15 minutos e só pode ser utilizado uma vez.

Se você não solicitou a recuperação de senha,
ignore este e-mail.

Equipe TripInsight
        """
    )

    contexto = ssl.create_default_context()

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as servidor:

        servidor.ehlo()
        servidor.starttls(context=contexto)
        servidor.ehlo()

        servidor.login(smtp_user, smtp_password)

        servidor.send_message(mensagem)


# ROTA PRINCIPAL

@app.get("/")
def home():

    return {
        "mensagem": "TripInsight API funcionando!"
    }


# CADASTRO

@app.post("/usuarios")
def cadastrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):

    email_existente = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()

    if email_existente:
        raise HTTPException(
            status_code=400,
            detail="Este e-mail já está cadastrado."
        )

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {
        "mensagem": "Usuário cadastrado com sucesso!"
    }


# LOGIN

@app.post("/login")
def login(
    usuario: LoginSchema,
    db: Session = Depends(get_db)
):

    usuario_encontrado = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()

    if not usuario_encontrado:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos."
        )

    senha_valida, senha_antiga = verificar_senha(
        usuario.senha,
        usuario_encontrado.senha
    )

    if not senha_valida:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos."
        )

    # Converte automaticamente senhas antigas para Argon2.

    if senha_antiga:
        usuario_encontrado.senha = gerar_hash_senha(
            usuario.senha
        )

        db.commit()

    return {
        "mensagem": "Login realizado com sucesso!",
        "usuario": {
            "id": usuario_encontrado.id,
            "nome": usuario_encontrado.nome,
            "email": usuario_encontrado.email,
            "foto_perfil": usuario_encontrado.foto_perfil
        }
    }


# SOLICITAR RECUPERAÇÃO DE SENHA

@app.post("/recuperar-senha")
def recuperar_senha(
    dados: RecuperarSenhaSchema,
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    mensagem_padrao = (
        "Se o e-mail estiver cadastrado, "
        "você receberá as instruções para recuperar sua senha."
    )

    # Não revela se o endereço está cadastrado.

    if not usuario:
        return {"mensagem": mensagem_padrao}

    agora = datetime.utcnow()

    # Invalida solicitações anteriores.

    db.query(RecuperacaoSenha).filter(
        RecuperacaoSenha.usuario_id == usuario.id,
        RecuperacaoSenha.usado_em.is_(None)
    ).update(
        {"usado_em": agora},
        synchronize_session=False
    )

    # Gera um token aleatório e guarda somente seu hash.

    token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    registro = RecuperacaoSenha(
        usuario_id=usuario.id,
        token_hash=token_hash,
        expira_em=agora + timedelta(minutes=15)
    )

    db.add(registro)
    db.commit()
    db.refresh(registro)

    frontend_url = os.getenv(
        "FRONTEND_URL",
        "http://127.0.0.1:5500/html"
    ).rstrip("/")

    link = (
        f"{frontend_url}/redefinir-senha.html"
        f"?token={quote(token)}"
    )

    try:

        enviar_email_recuperacao(
            usuario.email,
            link
        )

    except Exception as erro:

        db.delete(registro)
        db.commit()

        print(
            "Erro ao enviar e-mail de recuperação:",
            str(erro)
        )

        raise HTTPException(
            status_code=503,
            detail=(
                "Não foi possível enviar o e-mail "
                "de recuperação. Tente novamente mais tarde."
            )
        )

    return {"mensagem": mensagem_padrao}


# REDEFINIR SENHA

@app.post("/redefinir-senha")
def redefinir_senha(
    dados: RedefinirSenhaSchema,
    db: Session = Depends(get_db)
):

    token_hash = hashlib.sha256(
        dados.token.encode("utf-8")
    ).hexdigest()

    registro = db.query(RecuperacaoSenha).filter(
        RecuperacaoSenha.token_hash == token_hash
    ).first()

    agora = datetime.utcnow()

    if not registro:

        raise HTTPException(
            status_code=400,
            detail="Link de recuperação inválido ou expirado."
        )

    if registro.usado_em is not None:

        raise HTTPException(
            status_code=400,
            detail="Este link já foi utilizado."
        )

    if registro.expira_em <= agora:

        raise HTTPException(
            status_code=400,
            detail="Link de recuperação expirado."
        )

    usuario = buscar_usuario(
        registro.usuario_id,
        db
    )

    # Salva a nova senha protegida com Argon2.

    usuario.senha = gerar_hash_senha(
        dados.nova_senha
    )

    # Marca todos os tokens anteriores como utilizados.

    db.query(RecuperacaoSenha).filter(
        RecuperacaoSenha.usuario_id == usuario.id,
        RecuperacaoSenha.usado_em.is_(None)
    ).update(
        {"usado_em": agora},
        synchronize_session=False
    )

    db.commit()

    return {
        "mensagem": "Senha redefinida com sucesso! Você já pode fazer login."
    }


# ATUALIZAR PERFIL

@app.put("/usuarios/{usuario_id}")
def atualizar_usuario(
    usuario_id: int,
    nome: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):

    usuario = buscar_usuario(usuario_id, db)

    email_existente = db.query(Usuario).filter(
        Usuario.email == email,
        Usuario.id != usuario_id
    ).first()

    if email_existente:
        raise HTTPException(
            status_code=400,
            detail="Este e-mail já está sendo utilizado."
        )

    usuario.nome = nome
    usuario.email = email

    db.commit()
    db.refresh(usuario)

    return {
        "mensagem": "Perfil atualizado com sucesso!",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "foto_perfil": usuario.foto_perfil
        }
    }


# ATUALIZAR FOTO

@app.post("/usuarios/{usuario_id}/foto")
def atualizar_foto(
    usuario_id: int,
    foto: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    usuario = buscar_usuario(usuario_id, db)

    extensao = os.path.splitext(foto.filename)[1].lower()

    extensoes_permitidas = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]

    if extensao not in extensoes_permitidas:
        raise HTTPException(
            status_code=400,
            detail="Formato de imagem não permitido."
        )

    nome_arquivo = f"usuario_{usuario_id}{extensao}"
    caminho = os.path.join(PASTA_FOTOS, nome_arquivo)

    with open(caminho, "wb") as arquivo:
        shutil.copyfileobj(foto.file, arquivo)

    usuario.foto_perfil = caminho.replace("\\", "/")

    db.commit()
    db.refresh(usuario)

    return {
        "mensagem": "Foto de perfil atualizada com sucesso!",
        "foto_perfil": usuario.foto_perfil
    }


# REMOVER FOTO

@app.delete("/usuarios/{usuario_id}/foto")
def remover_foto(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    usuario = buscar_usuario(usuario_id, db)

    if usuario.foto_perfil:

        caminho_foto = usuario.foto_perfil

        if os.path.exists(caminho_foto):
            os.remove(caminho_foto)

    usuario.foto_perfil = None

    db.commit()

    return {
        "mensagem": "Foto de perfil removida com sucesso!",
        "foto_perfil": None
    }


# DASHBOARD

@app.get("/usuarios/{usuario_id}/dashboard")
def obter_dashboard(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    buscar_usuario(usuario_id, db)

    total_viagens = db.query(ControleFinanceiro).filter(
        ControleFinanceiro.usuario_id == usuario_id
    ).count()

    total_favoritos = db.query(Favorito).filter(
        Favorito.usuario_id == usuario_id
    ).count()

    total_experiencias = db.query(Experiencia).filter(
        Experiencia.usuario_id == usuario_id
    ).count()

    orcamento_total = db.query(
        func.coalesce(
            func.sum(ControleFinanceiro.orcamento_planejado),
            0
        )
    ).filter(
        ControleFinanceiro.usuario_id == usuario_id
    ).scalar()

    gasto_total = db.query(
        func.coalesce(
            func.sum(ControleFinanceiro.gasto_atual),
            0
        )
    ).filter(
        ControleFinanceiro.usuario_id == usuario_id
    ).scalar()

    return {
        "viagens": total_viagens,
        "favoritos": total_favoritos,
        "experiencias": total_experiencias,
        "orcamento_total": orcamento_total,
        "gasto_total": gasto_total
    }


# PLANEJAMENTO DE VIAGENS / CONTROLE FINANCEIRO

# LISTAR VIAGENS

@app.get("/usuarios/{usuario_id}/viagens")
def listar_viagens(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    buscar_usuario(usuario_id, db)

    viagens = db.query(ControleFinanceiro).filter(
        ControleFinanceiro.usuario_id == usuario_id
    ).all()

    return viagens


# CRIAR VIAGEM

@app.post("/usuarios/{usuario_id}/viagens")
def criar_viagem(
    usuario_id: int,
    viagem: ControleFinanceiroCreate,
    db: Session = Depends(get_db)
):

    buscar_usuario(usuario_id, db)

    nova_viagem = ControleFinanceiro(
        usuario_id=usuario_id,
        nome_viagem=viagem.nome_viagem,
        orcamento_planejado=viagem.orcamento_planejado,
        gasto_atual=viagem.gasto_atual
    )

    db.add(nova_viagem)
    db.commit()
    db.refresh(nova_viagem)

    return {
        "mensagem": "Viagem criada com sucesso!",
        "viagem": nova_viagem
    }


# EDITAR VIAGEM

@app.put("/viagens/{viagem_id}")
def editar_viagem(
    viagem_id: int,
    usuario_id: int,
    viagem: ControleFinanceiroCreate,
    db: Session = Depends(get_db)
):

    registro = db.query(ControleFinanceiro).filter(
        ControleFinanceiro.id == viagem_id,
        ControleFinanceiro.usuario_id == usuario_id
    ).first()

    if not registro:
        raise HTTPException(
            status_code=404,
            detail="Viagem não encontrada."
        )

    registro.nome_viagem = viagem.nome_viagem
    registro.orcamento_planejado = viagem.orcamento_planejado
    registro.gasto_atual = viagem.gasto_atual

    db.commit()
    db.refresh(registro)

    return {
        "mensagem": "Viagem atualizada com sucesso!",
        "viagem": registro
    }


# EXCLUIR VIAGEM

@app.delete("/viagens/{viagem_id}")
def excluir_viagem(
    viagem_id: int,
    usuario_id: int,
    db: Session = Depends(get_db)
):

    registro = db.query(ControleFinanceiro).filter(
        ControleFinanceiro.id == viagem_id,
        ControleFinanceiro.usuario_id == usuario_id
    ).first()

    if not registro:
        raise HTTPException(
            status_code=404,
            detail="Viagem não encontrada."
        )

    db.delete(registro)
    db.commit()

    return {
        "mensagem": "Viagem excluída com sucesso!"
    }


# EXPERIÊNCIAS

# LISTAR TODAS AS EXPERIÊNCIAS

@app.get("/experiencias")
def listar_experiencias(
    db: Session = Depends(get_db)
):

    experiencias = db.query(Experiencia).order_by(
        Experiencia.id.desc()
    ).all()

    return [
        formatar_experiencia(experiencia)
        for experiencia in experiencias
    ]


# LISTAR EXPERIÊNCIAS DE UM USUÁRIO

@app.get("/usuarios/{usuario_id}/experiencias")
def listar_experiencias_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    buscar_usuario(usuario_id, db)

    experiencias = db.query(Experiencia).filter(
        Experiencia.usuario_id == usuario_id
    ).order_by(
        Experiencia.id.desc()
    ).all()

    return [
        formatar_experiencia(experiencia)
        for experiencia in experiencias
    ]


# CRIAR EXPERIÊNCIA

@app.post("/usuarios/{usuario_id}/experiencias")
def criar_experiencia(
    usuario_id: int,
    experiencia: ExperienciaCreate,
    db: Session = Depends(get_db)
):

    buscar_usuario(usuario_id, db)

    nova_experiencia = Experiencia(
        usuario_id=usuario_id,
        destino=experiencia.destino,
        titulo=experiencia.titulo,
        relato=experiencia.relato,
        gasto_total=experiencia.gasto_total,
        avaliacao=experiencia.avaliacao
    )

    db.add(nova_experiencia)
    db.commit()
    db.refresh(nova_experiencia)

    return {
        "mensagem": "Experiência publicada com sucesso!",
        "experiencia": formatar_experiencia(nova_experiencia)
    }


# DETALHAR EXPERIÊNCIA

@app.get("/experiencias/{experiencia_id}")
def detalhar_experiencia(
    experiencia_id: int,
    db: Session = Depends(get_db)
):

    experiencia = buscar_experiencia(
        experiencia_id,
        db
    )

    return formatar_experiencia(experiencia)


# EDITAR EXPERIÊNCIA

@app.put("/experiencias/{experiencia_id}")
def editar_experiencia(
    experiencia_id: int,
    usuario_id: int,
    dados: ExperienciaCreate,
    db: Session = Depends(get_db)
):

    experiencia = db.query(Experiencia).filter(
        Experiencia.id == experiencia_id,
        Experiencia.usuario_id == usuario_id
    ).first()

    if not experiencia:
        raise HTTPException(
            status_code=404,
            detail="Experiência não encontrada."
        )

    experiencia.destino = dados.destino
    experiencia.titulo = dados.titulo
    experiencia.relato = dados.relato
    experiencia.gasto_total = dados.gasto_total
    experiencia.avaliacao = dados.avaliacao

    db.commit()
    db.refresh(experiencia)

    return {
        "mensagem": "Experiência atualizada com sucesso!",
        "experiencia": formatar_experiencia(experiencia)
    }


# EXCLUIR EXPERIÊNCIA

@app.delete("/experiencias/{experiencia_id}")
def excluir_experiencia(
    experiencia_id: int,
    usuario_id: int,
    db: Session = Depends(get_db)
):

    experiencia = db.query(Experiencia).filter(
        Experiencia.id == experiencia_id,
        Experiencia.usuario_id == usuario_id
    ).first()

    if not experiencia:
        raise HTTPException(
            status_code=404,
            detail="Experiência não encontrada."
        )

    db.query(Favorito).filter(
        Favorito.experiencia_id == experiencia_id
    ).delete(synchronize_session=False)

    db.query(Comentario).filter(
        Comentario.experiencia_id == experiencia_id
    ).delete(synchronize_session=False)

    db.delete(experiencia)
    db.commit()

    return {
        "mensagem": "Experiência excluída com sucesso!"
    }


# FAVORITOS

# LISTAR FAVORITOS

@app.get("/usuarios/{usuario_id}/favoritos")
def listar_favoritos(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    buscar_usuario(usuario_id, db)

    favoritos = db.query(Favorito).filter(
        Favorito.usuario_id == usuario_id
    ).all()

    return favoritos


# ADICIONAR FAVORITO

@app.post("/usuarios/{usuario_id}/favoritos")
def adicionar_favorito(
    usuario_id: int,
    dados: FavoritoCreate,
    db: Session = Depends(get_db)
):

    buscar_usuario(usuario_id, db)
    buscar_experiencia(dados.experiencia_id, db)

    favorito_existente = db.query(Favorito).filter(
        Favorito.usuario_id == usuario_id,
        Favorito.experiencia_id == dados.experiencia_id
    ).first()

    if favorito_existente:
        raise HTTPException(
            status_code=400,
            detail="Esta experiência já está nos favoritos."
        )

    novo_favorito = Favorito(
        usuario_id=usuario_id,
        experiencia_id=dados.experiencia_id
    )

    db.add(novo_favorito)
    db.commit()
    db.refresh(novo_favorito)

    return {
        "mensagem": "Experiência adicionada aos favoritos!",
        "favorito": novo_favorito
    }


# REMOVER FAVORITO

@app.delete(
    "/usuarios/{usuario_id}/favoritos/{experiencia_id}"
)
def remover_favorito(
    usuario_id: int,
    experiencia_id: int,
    db: Session = Depends(get_db)
):

    favorito = db.query(Favorito).filter(
        Favorito.usuario_id == usuario_id,
        Favorito.experiencia_id == experiencia_id
    ).first()

    if not favorito:
        raise HTTPException(
            status_code=404,
            detail="Favorito não encontrado."
        )

    db.delete(favorito)
    db.commit()

    return {
        "mensagem": "Favorito removido com sucesso!"
    }


# COMENTÁRIOS

# LISTAR COMENTÁRIOS

@app.get("/experiencias/{experiencia_id}/comentarios")
def listar_comentarios(
    experiencia_id: int,
    db: Session = Depends(get_db)
):

    buscar_experiencia(experiencia_id, db)

    comentarios = db.query(Comentario).filter(
        Comentario.experiencia_id == experiencia_id
    ).order_by(
        Comentario.id.desc()
    ).all()

    return comentarios


# PUBLICAR COMENTÁRIO

@app.post(
    "/experiencias/{experiencia_id}/comentarios/{usuario_id}"
)
def criar_comentario(
    experiencia_id: int,
    usuario_id: int,
    dados: ComentarioCreate,
    db: Session = Depends(get_db)
):

    buscar_usuario(usuario_id, db)
    buscar_experiencia(experiencia_id, db)

    novo_comentario = Comentario(
        experiencia_id=experiencia_id,
        usuario_id=usuario_id,
        comentario=dados.comentario
    )

    db.add(novo_comentario)
    db.commit()
    db.refresh(novo_comentario)

    return {
        "mensagem": "Comentário publicado com sucesso!",
        "comentario": novo_comentario
    }
