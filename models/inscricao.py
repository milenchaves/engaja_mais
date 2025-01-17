from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .vaga import Vaga
    from .voluntario import Voluntario

class InscricaoBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    status: str
    
class Inscricao(InscricaoBase, table=True):
    id_vaga: int = Field(foreign_key="vaga.id")
    id_voluntario: int = Field(foreign_key="voluntario.id")
    vaga: 'Vaga' = Relationship(back_populates="inscricao")
    voluntario: 'Voluntario' = Relationship(back_populates="inscricao")
