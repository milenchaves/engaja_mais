from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.organizacao import Organizacao, OrganizacaoBase
from database import get_session

router = APIRouter(
    prefix="/organizacoes",  # Prefixo para todas as rotas
    tags=["Organizações"],   # Tag para documentação automática
)

# Criar uma nova organização
@router.post("/", response_model=Organizacao)
def criar_organizacao(
    organizacao: Organizacao, session: Session = Depends(get_session)
):
    session.add(organizacao)
    session.commit()
    session.refresh(organizacao)
    return organizacao

# Ler todas as organizações (com paginação)
@router.get("/", response_model=list[Organizacao])
def listar_organizacoes(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Organizacao).offset(offset).limit(limit)).all()

# Ler uma única organização pelo ID
@router.get("/{organizacao_id}", response_model=Organizacao)
def listar_organizacao_por_id(
    organizacao_id: int, session: Session = Depends(get_session)
):
    organizacao = session.get(Organizacao, organizacao_id)
    if not organizacao:
        raise HTTPException(status_code=404, detail="Organizacao not found")
    return organizacao

# Atualizar uma organização existente
@router.put("/{organizacao_id}", response_model=Organizacao)
def atualizar_organizacao(
    organizacao_id: int,
    organizacao: OrganizacaoBase,
    session: Session = Depends(get_session),
):
    db_organizacao = session.get(Organizacao, organizacao_id)
    if not db_organizacao:
        raise HTTPException(status_code=404, detail="Organizacao not found")
    for key, value in organizacao.dict(exclude_unset=True).items():
        setattr(db_organizacao, key, value)
    session.add(db_organizacao)
    session.commit()
    session.refresh(db_organizacao)
    return db_organizacao

# Deletar uma organização
@router.delete("/{organizacao_id}")
def deletar_organizacao(
    organizacao_id: int, session: Session = Depends(get_session)
):
    organizacao = session.get(Organizacao, organizacao_id)
    if not organizacao:
        raise HTTPException(status_code=404, detail="Organizacao not found")
    session.delete(organizacao)
    session.commit()
    return {"ok": True}
