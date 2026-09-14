"""
Ponto de entrada da aplicação: cria a instância do FastAPI,
inicializa o banco de dados e registra as rotas (Controllers).
"""
from fastapi import FastAPI
from app.database import Base, engine
from app.controllers import produto_controller

# Cria as tabelas no banco (se ainda não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Produtos",
    description="API REST em padrão MVC para gestão de produtos - Desafio Final Arquiteto(a) de Software",
    version="1.0.0",
)

app.include_router(produto_controller.router)


@app.get("/")
def raiz():
    return {"mensagem": "API de Produtos no ar. Acesse /docs para a documentação Swagger."}


print("Iniciando app...")
from app.controllers import produto_controller
print("Controller importado com sucesso")