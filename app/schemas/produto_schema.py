"""
Schemas (DTOs): definem o formato dos dados que entram e saem da API,
separados da entidade do banco (Model). Isso evita expor a estrutura
interna do banco diretamente e permite validação automática.
"""
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=120)
    descricao: Optional[str] = Field(None, max_length=500)
    preco: Decimal = Field(..., gt=0, description="Preço deve ser maior que zero")
    estoque: int = Field(0, ge=0, description="Estoque não pode ser negativo")


class ProdutoCreate(ProdutoBase):
    """Usado no POST - criação de um novo produto."""
    pass


class ProdutoUpdate(BaseModel):
    """Usado no PATCH - atualização parcial protegida por concorrência otimista."""
    versao: int = Field(..., ge=1, description="Versão lida antes da atualização")
    nome: Optional[str] = Field(None, min_length=1, max_length=120)
    descricao: Optional[str] = Field(None, max_length=500)
    preco: Optional[Decimal] = Field(None, gt=0)
    estoque: Optional[int] = Field(None, ge=0)


class ProdutoReplace(ProdutoBase):
    """Usado no PUT - substituição completa protegida por concorrência."""
    versao: int = Field(..., ge=1, description="Versão lida antes da atualização")


class ProdutoResponse(ProdutoBase):
    """Usado nas respostas da API - inclui o ID gerado pelo banco."""
    id: int
    versao: int

    class Config:
        from_attributes = True  # permite converter direto do objeto ORM


class ProdutoListaResponse(BaseModel):
    """Resposta paginada da listagem de produtos."""
    items: list[ProdutoResponse]
    total: int
    page: int
    has_next: bool
