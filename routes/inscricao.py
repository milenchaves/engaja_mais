from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.inscricao import Inscricao, InscricaoBase
from database import get_session

router = APIRouter(
    prefix="/inscricoes",  # Prefixo para todas as rotas
    tags=["Inscrições"],   # Tag para documentação automática
)

# Criar uma nova inscrição
@router.post("/", response_model=Inscricao)
def criar_inscricao(
    inscricao: Inscricao, session: Session = Depends(get_session)
):
    session.add(inscricao)
    session.commit()
    session.refresh(inscricao)
    return inscricao

# Ler todas as inscrições (com paginação)
@router.get("/", response_model=list[Inscricao])
def listar_inscricoes(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Inscricao).offset(offset).limit(limit)).all()

# Ler uma única inscrição pelo ID
@router.get("/{inscricao_id}", response_model=Inscricao)
def listar_inscricao_por_id(
    inscricao_id: int, session: Session = Depends(get_session)
):
    inscricao = session.get(Inscricao, inscricao_id)
    if not inscricao:
        raise HTTPException(status_code=404, detail="Inscricao not found")
    return inscricao

# Atualizar uma inscrição existente
@router.put("/{inscricao_id}", response_model=Inscricao)
def atualizar_inscricao(
    inscricao_id: int,
    inscricao: InscricaoBase,
    session: Session = Depends(get_session),
):
    db_inscricao = session.get(Inscricao, inscricao_id)
    if not db_inscricao:
        raise HTTPException(status_code=404, detail="Inscricao not found")
    for key, value in inscricao.dict(exclude_unset=True).items():
        setattr(db_inscricao, key, value)
    session.add(db_inscricao)
    session.commit()
    session.refresh(db_inscricao)
    return db_inscricao

# Deletar uma inscrição
@router.delete("/{inscricao_id}")
def deletar_inscricao(
    inscricao_id: int, session: Session = Depends(get_session)
):
    inscricao = session.get(Inscricao, inscricao_id)
    if not inscricao:
        raise HTTPException(status_code=404, detail="Inscricao not found")
    session.delete(inscricao)
    session.commit()
    return {"ok": True}
