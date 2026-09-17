import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


class TestProdutoIntegracao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        cls.session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=cls.engine,
        )
        Base.metadata.create_all(bind=cls.engine)

        def sobrescrever_banco():
            db = cls.session_factory()
            try:
                yield db
            finally:
                db.close()

        cls.sobrescrever_banco = sobrescrever_banco
        app.dependency_overrides[get_db] = sobrescrever_banco
        cls.cliente = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=cls.engine)
        cls.engine.dispose()

    def setUp(self):
        with self.engine.begin() as conexao:
            for tabela in reversed(Base.metadata.sorted_tables):
                conexao.execute(tabela.delete())

    def test_fluxo_completo_de_produto(self):
        criado = self.cliente.post(
            "/produtos",
            json={
                "nome": "Carrinho Integrado",
                "descricao": "Produto criado no teste integrado",
                "preco": 39.90,
                "estoque": 5,
            },
        )

        self.assertEqual(criado.status_code, 201)
        produto = criado.json()
        produto_id = produto["id"]
        self.assertEqual(produto["nome"], "Carrinho Integrado")

        listado = self.cliente.get("/produtos")
        self.assertEqual(listado.status_code, 200)
        self.assertEqual(len(listado.json()), 1)

        por_id = self.cliente.get(f"/produtos/{produto_id}")
        self.assertEqual(por_id.status_code, 200)
        self.assertEqual(por_id.json()["id"], produto_id)

        por_nome = self.cliente.get("/produtos/nome/integrado")
        self.assertEqual(por_nome.status_code, 200)
        self.assertEqual(len(por_nome.json()), 1)

        contagem = self.cliente.get("/produtos/contar")
        self.assertEqual(contagem.status_code, 200)
        self.assertEqual(contagem.json(), {"total": 1})

        atualizado = self.cliente.put(
            f"/produtos/{produto_id}",
            json={"preco": 44.90, "estoque": 3},
        )
        self.assertEqual(atualizado.status_code, 200)
        self.assertEqual(atualizado.json()["preco"], 44.90)
        self.assertEqual(atualizado.json()["estoque"], 3)

        removido = self.cliente.delete(f"/produtos/{produto_id}")
        self.assertEqual(removido.status_code, 204)

        depois_da_remocao = self.cliente.get(f"/produtos/{produto_id}")
        self.assertEqual(depois_da_remocao.status_code, 404)

    def test_api_rejeita_produto_com_preco_invalido(self):
        resposta = self.cliente.post(
            "/produtos",
            json={
                "nome": "Produto inválido",
                "descricao": "Preço zero não é permitido",
                "preco": 0,
                "estoque": 1,
            },
        )

        self.assertEqual(resposta.status_code, 422)


if __name__ == "__main__":
    unittest.main()
