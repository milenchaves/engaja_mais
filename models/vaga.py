from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from .inscricao import Inscricao
    from .organizacao import Organizacao

class VagaBase(SQLModel):
    id_vaga: Optional[int] = Field(default=None, primary_key=True)
    nome_vaga: str
    descricao_vaga: str
    data_publicacao: date
    status_vaga: str

class Vaga(VagaBase, table=True):
    id_organizacao: int = Field(foreign_key="organizacao.id_organizacao")
    inscricoes: List["Inscricao"] = Relationship(back_populates="vaga")
    organizacao: "Organizacao" = Relationship(back_populates="vagas")
