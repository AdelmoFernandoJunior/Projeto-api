"""
Configuração da conexão com o banco de dados.
Usa SQLite para simplicidade (zero configuração), mas pode ser trocado
para PostgreSQL/MySQL apenas mudando a DATABASE_URL.
"""
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_PATH = Path(__file__).resolve().parent.parent / "produtos.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

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
