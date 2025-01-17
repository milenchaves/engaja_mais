from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from .organizacao import Organizacao
from .inscricao import Inscricao
if TYPE_CHECKING:
    from .organizacao import  OrganizacaoBase

class VagaBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome_vaga: str
    descricao_vaga: str
    data_publicacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status_vaga: str

class Vaga(VagaBase, table=True):
    id_organizacao: int = Field(foreign_key="organizacao.id")
    organizacao: list['Organizacao'] = Relationship(back_populates="vaga")
    inscricao: 'Inscricao' = Relationship(back_populates="vaga")

class VagaComOrganizacao(VagaBase):
    organizacao: 'OrganizacaoBase' 

