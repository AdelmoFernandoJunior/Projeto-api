"""
Model: representa a entidade de domínio Produto e seu mapeamento
para a tabela do banco de dados (camada M do MVC).
"""
from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(120), nullable=False, index=True)
    descricao = Column(String(500), nullable=True)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False, default=0)
