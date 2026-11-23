
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Numeric,
    ForeignKey,
    text
)

from sqlalchemy.orm import relationship

from database import Base


# USUÁRIOS

class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

    data_cadastro = Column(
        DateTime,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP")
    )

    foto_perfil = Column(String(255), nullable=True)

    experiencias = relationship(
        "Experiencia",
        back_populates="usuario"
    )

    favoritos = relationship(
        "Favorito",
        back_populates="usuario"
    )

    comentarios = relationship(
        "Comentario",
        back_populates="usuario"
    )

    controles_financeiros = relationship(
        "ControleFinanceiro",
        back_populates="usuario"
    )


# EXPERIÊNCIAS

class Experiencia(Base):

    __tablename__ = "experiencias"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    destino = Column(String(100), nullable=False)
    titulo = Column(String(150), nullable=False)
    relato = Column(Text, nullable=False)
    gasto_total = Column(Numeric(10, 2), nullable=True)
    avaliacao = Column(Integer, nullable=True)

    data_publicacao = Column(
        DateTime,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP")
    )

    usuario = relationship(
        "Usuario",
        back_populates="experiencias"
    )

    favoritos = relationship(
        "Favorito",
        back_populates="experiencia"
    )

    comentarios = relationship(
        "Comentario",
        back_populates="experiencia"
    )


# FAVORITOS

class Favorito(Base):

    __tablename__ = "favoritos"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    experiencia_id = Column(
        Integer,
        ForeignKey("experiencias.id"),
        nullable=False
    )

    usuario = relationship(
        "Usuario",
        back_populates="favoritos"
    )

    experiencia = relationship(
        "Experiencia",
        back_populates="favoritos"
    )


# COMENTÁRIOS

class Comentario(Base):

    __tablename__ = "comentarios"

    id = Column(Integer, primary_key=True, index=True)

    experiencia_id = Column(
        Integer,
        ForeignKey("experiencias.id"),
        nullable=False
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    comentario = Column(Text, nullable=False)

    data_comentario = Column(
        DateTime,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP")
    )

    experiencia = relationship(
        "Experiencia",
        back_populates="comentarios"
    )

    usuario = relationship(
        "Usuario",
        back_populates="comentarios"
    )


# CONTROLE FINANCEIRO

class ControleFinanceiro(Base):

    __tablename__ = "controle_financeiro"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    nome_viagem = Column(String(100), nullable=False)

    orcamento_planejado = Column(
        Numeric(10, 2),
        nullable=False
    )

    gasto_atual = Column(
        Numeric(10, 2),
        nullable=True,
        server_default=text("0.00")
    )

    usuario = relationship(
        "Usuario",
        back_populates="controles_financeiros"
    )


# RECUPERAÇÃO DE SENHA

class RecuperacaoSenha(Base):

    __tablename__ = "recuperacao_senhas"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    # Armazena somente o hash do token.
    token_hash = Column(String(64), nullable=False, unique=True)

    expira_em = Column(DateTime, nullable=False)

    usado_em = Column(DateTime, nullable=True)

    criado_em = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
