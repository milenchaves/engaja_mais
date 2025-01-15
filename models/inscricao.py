from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .vaga import Vaga, VagaBase
    from .voluntario import Voluntario

class InscricaoBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    status: str
    
class Inscricao(InscricaoBase, table=True):
    id_vaga: int = Field(default=None, foreign_key=True)
    id_voluntario: int = Field(default=None, foreign_key=True)
    vaga: 'Vaga' = Relationship(back_populates="inscricao")
    voluntario: 'Voluntario' = Relationship(back_populates="inscricao")

class IncricaoComVoluntario(InscricaoBase):
    vaga: VagaBase | None
    inscritos: list[Voluntario] = None