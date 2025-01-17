from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from datetime import datetime
from models.voluntario import Voluntario, VoluntarioBase
from database import get_session

router = APIRouter(
    prefix="/voluntarios",  # Prefixo para todas as rotas
    tags=["Voluntarios"],   # Tag para documentação automática
)

# Criar um novo voluntário
@router.post("/", response_model=Voluntario)
def create_voluntario(
    voluntario: Voluntario, session: Session = Depends(get_session)
):
    try:
        # Certifique-se de que o campo 'data_nascimento' é um objeto date
        if isinstance(voluntario.data_nascimento, str):
            voluntario.data_nascimento = datetime.strptime(voluntario.data_nascimento, "%Y-%m-%d").date()
            
        session.add(voluntario)
        session.commit()
        session.refresh(voluntario)
        return voluntario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Formato de data inválido: {e}")


# Ler todos os voluntários (com paginação)
@router.get("/", response_model=list[Voluntario])
def read_voluntarios(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Voluntario).offset(offset).limit(limit)).all()

# Ler um único voluntário pelo ID
@router.get("/{voluntario_id}", response_model=Voluntario)
def read_voluntario(
    voluntario_id: int, session: Session = Depends(get_session)
):
    voluntario = session.get(Voluntario, voluntario_id)
    if not voluntario:
        raise HTTPException(status_code=404, detail="Voluntario not found")
    return voluntario

# Atualizar um voluntário existente
@router.put("/{voluntario_id}", response_model=Voluntario)
def update_voluntario(
    voluntario_id: int,
    voluntario: VoluntarioBase,
    session: Session = Depends(get_session),
):
    db_voluntario = session.get(Voluntario, voluntario_id)
    if not db_voluntario:
        raise HTTPException(status_code=404, detail="Voluntario not found")
    for key, value in voluntario.dict(exclude_unset=True).items():
        setattr(db_voluntario, key, value)
    session.add(db_voluntario)
    session.commit()
    session.refresh(db_voluntario)
    return db_voluntario

# Deletar um voluntário
@router.delete("/{voluntario_id}")
def delete_voluntario(
    voluntario_id: int, session: Session = Depends(get_session)
):
    voluntario = session.get(Voluntario, voluntario_id)
    if not voluntario:
        raise HTTPException(status_code=404, detail="Voluntario not found")
    session.delete(voluntario)
    session.commit()
    return {"ok": True}
