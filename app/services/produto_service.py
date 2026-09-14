"""
Service: concentra a lógica de negócio, conectando o Controller ao Repository.
Nenhuma query SQL aparece aqui - apenas regras de negócio e orquestração.
"""
from sqlalchemy.orm import Session
from app.repositories.produto_repository import ProdutoRepository
from app.schemas.produto_schema import ProdutoCreate, ProdutoUpdate
from app.models.produto_model import Produto


class ProdutoService:

    def __init__(self, db: Session):
        self.repository = ProdutoRepository(db)

    def criar_produto(self, produto: ProdutoCreate) -> Produto:
        return self.repository.criar(produto)

    def listar_todos(self) -> list[Produto]:
        return self.repository.listar_todos()

    def buscar_por_id(self, produto_id: int) -> Produto | None:
        return self.repository.buscar_por_id(produto_id)

    def buscar_por_nome(self, nome: str) -> list[Produto]:
        return self.repository.buscar_por_nome(nome)

    def contar_produtos(self) -> int:
        return self.repository.contar()

    def atualizar_produto(self, produto_id: int, dados: ProdutoUpdate) -> Produto | None:
        return self.repository.atualizar(produto_id, dados)

    def deletar_produto(self, produto_id: int) -> bool:
        return self.repository.deletar(produto_id)
