# API de Produtos — Desafio Final (Arquiteto(a) de Software)

API REST em Python (FastAPI), seguindo o padrão arquitetural MVC, com CRUD
completo do domínio **Produto**, persistência em SQLite via SQLAlchemy.

## Estrutura de pastas

```
produto-api/
├── app/
│   ├── main.py                       # ponto de entrada, cria o app e inclui as rotas
│   ├── database.py                   # configuração da conexão com o banco (SQLite)
│   ├── controllers/
│   │   └── produto_controller.py     # Controller: define os endpoints HTTP
│   ├── services/
│   │   └── produto_service.py        # Service: lógica de negócio
│   ├── repositories/
│   │   └── produto_repository.py     # acesso a dados (queries via SQLAlchemy)
│   ├── models/
│   │   └── produto_model.py          # Model: entidade ORM (tabela produtos)
│   └── schemas/
│       └── produto_schema.py         # DTOs Pydantic (validação de entrada/saída)
├── requirements.txt
└── README.md
```

### Papel de cada camada (MVC)

- **Controller** (`controllers/`): recebe a requisição HTTP, valida o formato
  dos dados (via schema) e delega ao Service. Não contém regra de negócio.
- **Service** (`services/`): concentra a lógica de negócio e orquestra o
  fluxo entre Controller e Repository. Faz o papel equivalente à "View" em
  uma API sem interface gráfica.
- **Model** (`models/`): representa a entidade de domínio e seu mapeamento
  para a tabela do banco de dados.
- **Repository** (`repositories/`): isola o acesso a dados (queries),
  mantendo o Service independente de como os dados são persistidos.
- **Schema** (`schemas/`): define o contrato de entrada/saída da API,
  separado da entidade do banco.

## Como rodar

```bash
# 1. Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar a aplicação
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`. A documentação Swagger gerada
automaticamente fica em `http://localhost:8000/docs`.

## Endpoints

| Método | Rota                    | Descrição                          |
|--------|--------------------------|-------------------------------------|
| POST   | `/produtos`              | Cria um novo produto               |
| GET    | `/produtos`               | Lista todos os produtos            |
| GET    | `/produtos/{id}`          | Busca produto por ID               |
| GET    | `/produtos/nome/{nome}`   | Busca produtos por nome            |
| GET    | `/produtos/contar`        | Retorna o total de produtos        |
| PUT    | `/produtos/{id}`          | Atualiza um produto existente      |
| DELETE | `/produtos/{id}`          | Remove um produto                  |

## Persistência

O banco de dados SQLite é criado automaticamente (`produtos.db`) na primeira
execução — não é necessário nenhum setup manual de banco.



