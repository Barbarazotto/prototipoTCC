
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Localiza e carrega o arquivo .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Recupera a conexão com o banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")

# Utiliza SQLite quando não houver DATABASE_URL
if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{BASE_DIR / 'tripinsight.db'}"

# Configura a conexão
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

