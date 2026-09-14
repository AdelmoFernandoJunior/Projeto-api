"""
Repository: isola todo o acesso ao banco de dados (queries).
O Service não sabe como os dados são armazenados, apenas chama estes métodos.
"""
from sqlalchemy.orm import Session
from app.models.produto_model import Produto
from app.schemas.produto_schema import ProdutoCreate, ProdutoUpdate


class ProdutoRepository:

    def __init__(self, db: Session):
        self.db = db

    def criar(self, produto: ProdutoCreate) -> Produto:
        novo_produto = Produto(**produto.model_dump())
        self.db.add(novo_produto)
        self.db.commit()
        self.db.refresh(novo_produto)
        return novo_produto

    def listar_todos(self) -> list[Produto]:
        return self.db.query(Produto).all()

    def buscar_por_id(self, produto_id: int) -> Produto | None:
        return self.db.query(Produto).filter(Produto.id == produto_id).first()

    def buscar_por_nome(self, nome: str) -> list[Produto]:
        return self.db.query(Produto).filter(Produto.nome.ilike(f"%{nome}%")).all()

    def contar(self) -> int:
        return self.db.query(Produto).count()

    def atualizar(self, produto_id: int, dados: ProdutoUpdate) -> Produto | None:
        produto = self.buscar_por_id(produto_id)
        if produto is None:
            return None
        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(produto, campo, valor)
        self.db.commit()
        self.db.refresh(produto)
        return produto

    def deletar(self, produto_id: int) -> bool:
        produto = self.buscar_por_id(produto_id)
        if produto is None:
            return False
        self.db.delete(produto)
        self.db.commit()
        return True
