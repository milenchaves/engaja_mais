from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List
from .voluntario import OrganizacaoVoluntario
if TYPE_CHECKING:
    from .voluntario import Voluntario
    from .vaga import Vaga

class OrganizacaoBase(SQLModel):
    id: int | None = Field (default=None, primary_key=True)
    nome_organizacao: str 
    localizacao: str 
    causa_apoiada: str
    
class Organizacao(OrganizacaoBase, table=True):
    voluntarios: List ['Voluntario'] = Relationship(link_model=OrganizacaoVoluntario)
    vaga: List ['Vaga'] = Relationship(back_populates='organizacao')
    
