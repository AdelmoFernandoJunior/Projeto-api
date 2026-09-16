import unittest
from unittest.mock import Mock

from pydantic import ValidationError

from app.schemas.produto_schema import ProdutoCreate, ProdutoUpdate
from app.services.produto_service import ProdutoService


class TestProdutoService(unittest.TestCase):
    def setUp(self):
        self.repository = Mock()
        self.service = ProdutoService(db=Mock())
        self.service.repository = self.repository

    def test_criar_produto_delega_para_o_repository(self):
        produto = ProdutoCreate(
            nome="Boneca de Pano",
            descricao="Brinquedo de tecido",
            preco=45.50,
            estoque=12,
        )
        produto_criado = Mock(id=1)
        self.repository.criar.return_value = produto_criado

        resultado = self.service.criar_produto(produto)

        self.assertIs(resultado, produto_criado)
        self.repository.criar.assert_called_once_with(produto)

    def test_listar_todos_delega_para_o_repository(self):
        produtos = [Mock(id=1), Mock(id=2)]
        self.repository.listar_todos.return_value = produtos

        resultado = self.service.listar_todos()

        self.assertEqual(resultado, produtos)
        self.repository.listar_todos.assert_called_once_with()

    def test_buscar_por_id_delega_para_o_repository(self):
        produto = Mock(id=3)
        self.repository.buscar_por_id.return_value = produto

        resultado = self.service.buscar_por_id(3)

        self.assertIs(resultado, produto)
        self.repository.buscar_por_id.assert_called_once_with(3)

    def test_buscar_por_nome_delega_para_o_repository(self):
        produtos = [Mock(id=4)]
        self.repository.buscar_por_nome.return_value = produtos

        resultado = self.service.buscar_por_nome("boneca")

        self.assertEqual(resultado, produtos)
        self.repository.buscar_por_nome.assert_called_once_with("boneca")

    def test_contar_produtos_delega_para_o_repository(self):
        self.repository.contar.return_value = 6

        resultado = self.service.contar_produtos()

        self.assertEqual(resultado, 6)
        self.repository.contar.assert_called_once_with()

    def test_atualizar_produto_delega_para_o_repository(self):
        dados = ProdutoUpdate(preco=49.90)
        produto = Mock(id=5)
        self.repository.atualizar.return_value = produto

        resultado = self.service.atualizar_produto(5, dados)

        self.assertIs(resultado, produto)
        self.repository.atualizar.assert_called_once_with(5, dados)

    def test_deletar_produto_delega_para_o_repository(self):
        self.repository.deletar.return_value = True

        resultado = self.service.deletar_produto(5)

        self.assertTrue(resultado)
        self.repository.deletar.assert_called_once_with(5)


class TestProdutoSchema(unittest.TestCase):
    def test_preco_deve_ser_maior_que_zero(self):
        with self.assertRaises(ValidationError):
            ProdutoCreate(nome="Brinquedo inválido", preco=0, estoque=1)

    def test_estoque_nao_pode_ser_negativo(self):
        with self.assertRaises(ValidationError):
            ProdutoCreate(nome="Brinquedo inválido", preco=10, estoque=-1)


if __name__ == "__main__":
    unittest.main()
