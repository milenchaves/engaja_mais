from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from .inscricao import Inscricao
    from .voluntario_organizacao import VoluntarioOrganizacao
    from .organizacao import Organizacao

class VoluntarioBase(SQLModel):
    id_voluntario: Optional[int] = Field(default=None, primary_key=True)
    nome_voluntario: str
    email: str
    data_nascimento: date
    area_interesse: str

class Voluntario(VoluntarioBase, table=True):
    inscricoes: List["Inscricao"] = Relationship(back_populates="voluntario")
    organizacoes: List["VoluntarioOrganizacao"] = Relationship(back_populates="voluntario")