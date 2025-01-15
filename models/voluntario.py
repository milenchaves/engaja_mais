from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING
from datetime import date
if TYPE_CHECKING:
    from .inscricao import Inscricao
    from .organizacao import Organizacao, OrganizacaoVoluntario

class VoluntarioBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    nome_voluntario: str
    email: str
    data_nascimento: date
    area_interesse: str

class Voluntario(VoluntarioBase, table=True):
    inscricoes: List["Inscricao"] = Relationship(back_populates="voluntario")
    organizacoes: List["Organizacao"] = Relationship(link_model=OrganizacaoVoluntario)
    
class VoluntarioComInscricaoOrganizacao(VoluntarioBase):
    inscricoes: list[Inscricao] = None
    organizacoes: list[Organizacao] = None