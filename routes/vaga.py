from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from datetime import datetime
from models.vaga import Vaga, VagaBase
from database import get_session

router = APIRouter(
    prefix="/vagas",  
    tags=["Vagas"],   
)


@router.post("/", response_model=Vaga)
def criar_vaga(
    vaga: Vaga, session: Session = Depends(get_session)
):
    try:
        if isinstance(vaga.data_publicacao, str):
            vaga.data_publicacao = datetime.strptime(vaga.data_publicacao, "%Y-%m-%d").date()

        session.add(vaga)
        session.commit()
        session.refresh(vaga)
        return vaga
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Formato de data inválido: {e}")



@router.get("/", response_model=list[Vaga])
def listar_vagas(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Vaga).offset(offset).limit(limit)).all()


@router.get("/{vaga_id}", response_model=Vaga)
def listar_vaga_por_id(
    vaga_id: int, session: Session = Depends(get_session)
):
    vaga = session.get(Vaga, vaga_id)
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga not found")
    return vaga

@router.put("/{vaga_id}", response_model=Vaga)
def atualizar_vaga(
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


@router.delete("/{vaga_id}")
def deletar_vaga(
    vaga_id: int, session: Session = Depends(get_session)
):
    vaga = session.get(Vaga, vaga_id)
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga not found")
    session.delete(vaga)
    session.commit()
    return {"ok": True}
