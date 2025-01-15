from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .vaga import Vaga

class OrganizacaoVoluntario(SQLModel, table=True):
    id_organizacao: int = Field(default=None, foreign_key="organizacao.id", primary_key=True)
    id_voluntario: int = Field(default=None, foreign_key="voluntario.id", primary_key=True)
    
class OrganizacaoBase(SQLModel):
    id: int | None = Field (default=None, primary_key=True)
    nome_organizacao: str 
    localizacao: str 
    causa_apoiada: str

class Organizacao(OrganizacaoBase, table=True):
    vagas: list[Vaga] = Relationship(back_populates="organizacao")
    
class OrganizacaoComVaga(OrganizacaoVoluntario):
    vagas: list[Vaga] = None