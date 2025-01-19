from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session
from models.organizacao import Organizacao
from models.vaga import Vaga
from models.voluntario import Voluntario
from models.inscricao import Inscricao
from datetime import date
from database import get_session
from sqlalchemy.orm import joinedload

router = APIRouter(
    prefix="/consultas",  
    tags=["Consultas"],  
)

@router.get("/{id_organizacao}/Vaga_Organizacao")
def listar_vagas_por_organizacao(id_organizacao: int, session: Session = Depends(get_session)):
    organizacao = session.query(Organizacao).options(joinedload(Organizacao.vaga))\
        .filter(Organizacao.id == id_organizacao).first()

    if not organizacao:
        raise HTTPException(status_code=404, detail="Organização não encontrada")
    
    return {"organizacao": organizacao.nome_organizacao, "vagas": organizacao.vaga}

@router.get("/{id_organizacao}/Voluntario_Organizacao")
def listar_voluntarios_por_organizacao(id_organizacao: int, session: Session = Depends(get_session)):
    organizacao = session.query(Organizacao).options(joinedload(Organizacao.voluntarios))\
        .filter(Organizacao.id == id_organizacao).first()

    if not organizacao:
        raise HTTPException(status_code=404, detail="Organização não encontrada")
    
    return {"organizacao": organizacao.nome_organizacao, "voluntarios": [voluntario.nome_voluntario for voluntario in organizacao.voluntarios]}

@router.get("/Vagas")
def listar_vagas_por_data(data_inicio: date = Query(None), data_fim: date = Query(None), 
    order: str = Query("asc", enum=["asc", "desc"]),
    session: Session = Depends(get_session)):
        query = session.query(Vaga)
    
        if data_inicio:
            query = query.filter(Vaga.data_publicacao >= data_inicio)
        if data_fim:
            query = query.filter(Vaga.data_publicacao <= data_fim)

        if order == "asc":
            vagas = query.order_by(Vaga.data_publicacao.asc()).all()
        else:
            vagas = query.order_by(Vaga.data_publicacao.desc()).all()
    
        if not vagas:
            raise HTTPException(status_code=404, detail="Vagas não encontradas nesse período de data")

        return {"vaga": vagas}

    
@router.get("/voluntarios_inscrito_por_organizacao")
def listar_voluntarios_inscrito_por_organizacao(nome_organizacao: str, session: Session = Depends(get_session)):
    query = session.query(Voluntario).\
        join(Inscricao, Inscricao.id_voluntario == Voluntario.id).\
        join(Vaga, Vaga.id == Inscricao.id_vaga).\
        join(Organizacao, Organizacao.id == Vaga.id_organizacao).\
        filter(Organizacao.nome_organizacao == nome_organizacao) 
    voluntarios = query.all()

    if not voluntarios:
        raise HTTPException(status_code=404, detail="Nenhum voluntário inscrito para essa organização")

    return {"voluntarios": voluntarios}

@router.get("/vagas_por_status")
def listar_vagas_status(status: str = Query("Ativa", enum=["Ativa", "Encerrada"]),
    session: Session = Depends(get_session)):
    
    vagas = session.query(Vaga).filter(Vaga.status_vaga == status).all()
    
    if not vagas:
        raise HTTPException(status_code=404, detail="Nenhuma vaga encontrada com o status especificado.")
    
    return {"vaga" : vagas}
