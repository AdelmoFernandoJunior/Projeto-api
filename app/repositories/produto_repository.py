"""
Repository: isola todo o acesso ao banco de dados (queries).
O Service não sabe como os dados são armazenados, apenas chama estes métodos.
"""
from sqlalchemy import update
from sqlalchemy.orm import Session
from app.models.produto_model import Produto
from app.schemas.produto_schema import ProdutoCreate, ProdutoReplace, ProdutoUpdate


class ConcorrenciaProdutoError(Exception):
    """Indica que o produto foi alterado desde a leitura do cliente."""


class ProdutoRepository:

    def __init__(self, db: Session):
        self.db = db

    def criar(self, produto: ProdutoCreate) -> Produto:
        novo_produto = Produto(**produto.model_dump())
        self.db.add(novo_produto)
        self.db.commit()
        self.db.refresh(novo_produto)
        return novo_produto

    def listar_todos(self, skip: int = 0, limit: int = 20) -> tuple[list[Produto], int]:
        consulta = self.db.query(Produto)
        total = consulta.count()
        produtos = consulta.offset(skip).limit(limit).all()
        return produtos, total

    def buscar_por_id(self, produto_id: int) -> Produto | None:
        return self.db.query(Produto).filter(Produto.id == produto_id).first()

    def buscar_por_nome(self, nome: str) -> list[Produto]:
        return self.db.query(Produto).filter(Produto.nome.ilike(f"%{nome}%")).all()

    def contar(self) -> int:
        return self.db.query(Produto).count()

    def atualizar(
        self,
        produto_id: int,
        dados: ProdutoUpdate | ProdutoReplace,
    ) -> Produto | None:
        campos = dados.model_dump(exclude={"versao"}, exclude_unset=True)
        campos["versao"] = Produto.versao + 1
        resultado = self.db.execute(
            update(Produto)
            .where(Produto.id == produto_id, Produto.versao == dados.versao)
            .values(**campos)
        )
        if resultado.rowcount == 0:
            self.db.rollback()
            if self.buscar_por_id(produto_id) is None:
                return None
            raise ConcorrenciaProdutoError

        self.db.commit()
        produto = self.buscar_por_id(produto_id)
        if produto is None:
            return None
        return produto

    def deletar(self, produto_id: int) -> bool:
        produto = self.buscar_por_id(produto_id)
        if produto is None:
            return False
        self.db.delete(produto)
        self.db.commit()
        return True
