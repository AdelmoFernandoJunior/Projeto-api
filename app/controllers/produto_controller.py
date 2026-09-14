"""
Controller: recebe as requisições HTTP, delega ao Service e devolve a
resposta. Não contém lógica de negócio nem acesso direto ao banco.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.produto_service import ProdutoService
from app.schemas.produto_schema import ProdutoCreate, ProdutoUpdate, ProdutoResponse

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    service = ProdutoService(db)
    return service.criar_produto(produto)


@router.get("", response_model=list[ProdutoResponse])
def listar_todos(db: Session = Depends(get_db)):
    service = ProdutoService(db)
    return service.listar_todos()


@router.get("/contar")
def contar_produtos(db: Session = Depends(get_db)):
    service = ProdutoService(db)
    return {"total": service.contar_produtos()}


@router.get("/nome/{nome}", response_model=list[ProdutoResponse])
def buscar_por_nome(nome: str, db: Session = Depends(get_db)):
    service = ProdutoService(db)
    return service.buscar_por_nome(nome)


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_por_id(produto_id: int, db: Session = Depends(get_db)):
    service = ProdutoService(db)
    produto = service.buscar_por_id(produto_id)
    if produto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoUpdate, db: Session = Depends(get_db)):
    service = ProdutoService(db)
    produto = service.atualizar_produto(produto_id, dados)
    if produto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    service = ProdutoService(db)
    sucesso = service.deletar_produto(produto_id)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return None
