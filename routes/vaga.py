from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.vaga import Vaga, VagaBase, VagaComOrganizacao
from database import get_session

router = APIRouter(
    prefix="/vagas",  # Prefixo para todas as rotas
    tags=["Vagas"],   # Tag para documentação automática
)

# Criar uma nova vaga
@router.post("/", response_model=Vaga)
def create_vaga(
    vaga: Vaga, session: Session = Depends(get_session)
):
    session.add(vaga)
    session.commit()
    session.refresh(vaga)
    return vaga

# Ler todas as vagas (com paginação)
@router.get("/", response_model=list[Vaga])
def read_vagas(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Vaga).offset(offset).limit(limit)).all()

# Ler uma única vaga pelo ID
@router.get("/{vaga_id}", response_model=VagaComOrganizacao)
def read_vaga(
    vaga_id: int, session: Session = Depends(get_session)
):
    vaga = session.get(Vaga, vaga_id)
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga not found")
    return vaga

# Atualizar uma vaga existente
@router.put("/{vaga_id}", response_model=Vaga)
def update_vaga(
    vaga_id: int,
    vaga: VagaBase,
    session: Session = Depends(get_session),
):
    db_vaga = session.get(Vaga, vaga_id)
    if not db_vaga:
        raise HTTPException(status_code=404, detail="Vaga not found")
    for key, value in vaga.dict(exclude_unset=True).items():
        setattr(db_vaga, key, value)
    session.add(db_vaga)
    session.commit()
    session.refresh(db_vaga)
    return db_vaga

# Deletar uma vaga
@router.delete("/{vaga_id}")
def delete_vaga(
    vaga_id: int, session: Session = Depends(get_session)
):
    vaga = session.get(Vaga, vaga_id)
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga not found")
    session.delete(vaga)
    session.commit()
    return {"ok": True}
