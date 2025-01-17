from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING
from datetime import datetime, timezone
from .inscricao import Inscricao

if TYPE_CHECKING:
    from .organizacao import  Organizacao

class VagaBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    nome_vaga: str
    descricao_vaga: str
    data_publicacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status_vaga: str

class Vaga(VagaBase, table=True):
    id_organizacao: int = Field(foreign_key="organizacao.id")
    organizacao: List['Organizacao'] = Relationship(back_populates="vaga")
    inscricao: List['Inscricao'] = Relationship(back_populates="vaga")

