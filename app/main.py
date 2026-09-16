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


# def executar_teste_manual():
#     from fastapi.testclient import TestClient

#     cliente = TestClient(app)

#     resposta = cliente.post(
#         "/produtos",
#         json={
#             "nome": "Produto de teste",
#             "descricao": "Produto criado durante o teste manual",
#             "preco": 99.90,
#             "estoque": 10,
#         },
#     )
#     resposta.raise_for_status()
#     produto_id = resposta.json()["id"]

#     cliente.get("/produtos").raise_for_status()
#     cliente.get(f"/produtos/{produto_id}").raise_for_status()
#     cliente.get("/produtos/nome/teste").raise_for_status()
#     cliente.get("/produtos/contar").raise_for_status()

#     cliente.put(
#         f"/produtos/{produto_id}",
#         json={"preco": 109.90, "estoque": 8},
#     ).raise_for_status()
#     cliente.delete(f"/produtos/{produto_id}").raise_for_status()

#     print("Teste manual concluído com sucesso.")


# def inserir_brinquedos_teste():
#     from fastapi.testclient import TestClient

#     cliente = TestClient(app)
#     brinquedos = [
#         {
#             "nome": "Blocos de Montar",
#             "descricao": "Conjunto colorido com 120 pecas para montar",
#             "preco": 79.90,
#             "estoque": 18,
#         },
#         {
#             "nome": "Boneca de Pano",
#             "descricao": "Boneca macia de pano com vestido colorido",
#             "preco": 45.50,
#             "estoque": 12,
#         },
#         {
#             "nome": "Carrinho de Corrida",
#             "descricao": "Carrinho metalizado para brincar e colecionar",
#             "preco": 29.90,
#             "estoque": 25,
#         },
#         {
#             "nome": "Quebra-cabeca Infantil",
#             "descricao": "Quebra-cabeca com 100 pecas e ilustracao de animais",
#             "preco": 34.90,
#             "estoque": 9,
#         },
#         {
#             "nome": "Jogo de Tabuleiro",
#             "descricao": "Jogo familiar de estrategia para ate quatro pessoas",
#             "preco": 89.90,
#             "estoque": 7,
#         },
#     ]

#     produtos_criados = 0
#     for brinquedo in brinquedos:
#         existentes = cliente.get(
#             f"/produtos/nome/{brinquedo['nome']}"
#         )
#         existentes.raise_for_status()
#         if not any(produto["nome"] == brinquedo["nome"] for produto in existentes.json()):
#             resposta = cliente.post("/produtos", json=brinquedo)
#             resposta.raise_for_status()
#             produtos_criados += 1

#     produtos = cliente.get("/produtos")
#     produtos.raise_for_status()

#     busca = cliente.get("/produtos/nome/boneca")
#     busca.raise_for_status()

#     total = cliente.get("/produtos/contar")
#     total.raise_for_status()

#     print(f"Teste de brinquedos concluído. Novos produtos: {produtos_criados}.")
#     print(f"Produtos cadastrados no banco: {total.json()['total']}.")


# if __name__ == "__main__":
#     inserir_brinquedos_teste()


