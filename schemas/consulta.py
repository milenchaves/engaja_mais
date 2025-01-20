from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.organizacao import Organizacao
from models.vaga import Vaga
from models.voluntario import Voluntario
from models.inscricao import Inscricao
from datetime import date
from database import get_session
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func

router = APIRouter(
    prefix="/consultas",  
    tags=["Consultas"],  
)

@router.get("/{id_organizacao}/Vagas_por_Organiazacao")
def listar_vagas_por_organizacao(id_organizacao: int,session: Session = Depends(get_session)):
    
    organizacao = session.query(Organizacao).options(joinedload(Organizacao.vaga))\
        .filter(Organizacao.id == id_organizacao).first()

    if not organizacao:
        raise HTTPException(status_code=404, detail="Organização não encontrada")
    
    return {"organizacao": organizacao.nome_organizacao, "vagas": organizacao.vaga}

@router.get("/{id_organizacao}/Voluntario_por_Organizacao")
def listar_voluntarios_por_organizacao(id_organizacao: int, session: Session = Depends(get_session)):
    
    organizacao = session.query(Organizacao).options(joinedload(Organizacao.voluntarios))\
        .filter(Organizacao.id == id_organizacao).first()

    if not organizacao:
        raise HTTPException(status_code=404, detail="Organização não encontrada")
    
    return {"organizacao": organizacao.nome_organizacao, "voluntarios": [voluntario.nome_voluntario for voluntario in organizacao.voluntarios]}

@router.get("/Vagas_por_data")
def listar_vagas_por_data(data_inicio: date = Query(None), data_fim: date = Query(None),
    order: str = Query("asc", enum=["asc", "desc"]),session: Session = Depends(get_session)):
    
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

    
@router.get("/Voluntarios_inscrito_por_organizacao")
def listar_voluntarios_inscrito_por_organizacao(nome_organizacao: str, 
limit: int = Query(default=10, le=100),
session: Session = Depends(get_session)):
    query = session.query(Voluntario).\
        join(Inscricao, Inscricao.id_voluntario == Voluntario.id).\
        join(Vaga, Vaga.id == Inscricao.id_vaga).\
        join(Organizacao, Organizacao.id == Vaga.id_organizacao).\
        filter(Organizacao.nome_organizacao == nome_organizacao) 
    voluntarios = query.all()

    if not voluntarios:
        raise HTTPException(status_code=404, detail="Nenhum voluntário inscrito para essa organização")

    return {"voluntarios": voluntarios}

@router.get("/Vagas_por_status")
def listar_vagas_status(status: str = Query("Ativa", enum=["Ativa", "Encerrada"]),
session: Session = Depends(get_session)):
    
    vagas = session.query(Vaga).filter(Vaga.status_vaga == status).all()
    
    if not vagas:
        raise HTTPException(status_code=404, detail="Nenhuma vaga encontrada com o status especificado.")
    
    return {"vaga" : vagas}

@router.get("/Vagas_por_localizacao")
def listar_organizacoes_por_localizacao(localizacao: str = Query(...),limit: int = Query(default=10, le=100),
session: Session = Depends(get_session)):
    
    query = session.query(Organizacao).options(joinedload(Organizacao.vaga)
            ).filter(Organizacao.localizacao.contains(localizacao)).limit(limit)
    organizacoes = query.all()

    if not organizacoes:
        raise HTTPException(status_code=404, detail="Nenhuma organização encontrada para essa localização.")

    return {"organizacoes": organizacoes}

@router.get("/{id_organizacao}/Contar_vaga_por_organizacao")
def contar_vagas_por_organizacao(id_organizacao: int, session: Session = Depends(get_session)):

    organizacao = session.query(Organizacao).options(joinedload(Organizacao.vaga)
    ).filter(Organizacao.id == id_organizacao).first()

    if not organizacao:
        raise HTTPException(status_code=404, detail="Organização não encontrada.")
    
    total_vagas = len(organizacao.vaga)  

    return {"organizacao": organizacao.nome_organizacao, "total_vagas": total_vagas}

@router.get("/inscricoes/contagem/{id_vaga}")
def contar_inscricoes_por_vaga(id_vaga: int,session: Session = Depends(get_session)):
    
    vaga = session.query(Vaga).filter(Vaga.id == id_vaga).first()
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada.")

    total_inscricoes = (session.query(func.count(Inscricao.id)).filter(Inscricao.id_vaga == id_vaga).scalar() )

    return {"vaga": vaga.nome_vaga,"total_inscricoes": total_inscricoes}