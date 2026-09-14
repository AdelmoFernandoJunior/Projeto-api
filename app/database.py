"""
Configuração da conexão com o banco de dados.
Usa SQLite para simplicidade (zero configuração), mas pode ser trocado
para PostgreSQL/MySQL apenas mudando a DATABASE_URL.
"""
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, declarative_base
except Exception as e:
    raise RuntimeError(
        "SQLAlchemy is required but could not be imported. Install it with: pip install SQLAlchemy"
    ) from e

DATABASE_URL = "sqlite:///./produtos.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessário apenas para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency do FastAPI: abre uma sessão de banco por requisição
    e garante o fechamento ao final, mesmo em caso de erro.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
