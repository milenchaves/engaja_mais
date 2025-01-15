from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
if TYPE_CHECKING:
    from .organizacao import Organizacao, OrganizacaoBase

class VagaBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome_vaga: str
    descricao_vaga: str
    data_publicacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status_vaga: str

class Vaga(VagaBase, table=True):
    id_organizacao: int = Field(foreign_key="organizacao.id")
    organizacao: 'Organizacao' = Relationship(back_populates="vagas")

class VagaComOrganizacao(VagaBase):
    organizacao: OrganizacaoBase | None

