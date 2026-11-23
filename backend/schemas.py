
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# CONFIGURAÇÃO BASE

class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# USUÁRIOS

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str = Field(min_length=8)


class UsuarioResponse(SchemaBase):
    id: int
    nome: str
    email: str
    foto_perfil: Optional[str] = None
    data_cadastro: Optional[datetime] = None


class LoginSchema(BaseModel):
    email: str
    senha: str


# RECUPERAÇÃO DE SENHA

class RecuperarSenhaSchema(BaseModel):
    email: str


class RedefinirSenhaSchema(BaseModel):
    token: str
    nova_senha: str = Field(min_length=8)


# EXPERIÊNCIAS

class ExperienciaCreate(BaseModel):
    destino: str
    titulo: str
    relato: str
    gasto_total: Optional[Decimal] = None
    avaliacao: Optional[int] = Field(default=None, ge=1, le=5)


class ExperienciaResponse(SchemaBase):
    id: int
    usuario_id: int
    destino: str
    titulo: str
    relato: str
    gasto_total: Optional[Decimal] = None
    avaliacao: Optional[int] = None
    data_publicacao: Optional[datetime] = None


# FAVORITOS

class FavoritoCreate(BaseModel):
    experiencia_id: int


class FavoritoResponse(SchemaBase):
    id: int
    usuario_id: int
    experiencia_id: int


# COMENTÁRIOS

class ComentarioCreate(BaseModel):
    comentario: str = Field(min_length=1)


class ComentarioResponse(SchemaBase):
    id: int
    experiencia_id: int
    usuario_id: int
    comentario: str
    data_comentario: Optional[datetime] = None


# CONTROLE FINANCEIRO

class ControleFinanceiroCreate(BaseModel):
    nome_viagem: str
    orcamento_planejado: Decimal = Field(ge=0)
    gasto_atual: Decimal = Field(default=Decimal("0.00"), ge=0)


class ControleFinanceiroResponse(SchemaBase):
    id: int
    usuario_id: int
    nome_viagem: str
    orcamento_planejado: Decimal
    gasto_atual: Optional[Decimal] = None
