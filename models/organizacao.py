from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from .voluntario import OrganizacaoVoluntario
if TYPE_CHECKING:
    from .voluntario import Voluntario

class OrganizacaoBase(SQLModel):
    id: int | None = Field (default=None, primary_key=True)
    nome_organizacao: str 
    localizacao: str 
    causa_apoiada: str
    
class Organizacao(OrganizacaoBase, table=True):
    voluntarios: list ['Voluntario'] = Relationship(link_model=OrganizacaoVoluntario)
