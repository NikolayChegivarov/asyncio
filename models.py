from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Column, Integer, String, Float
from typing import Optional
import os
from dotenv import load_dotenv
import json
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
print("models.py")

try:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT]):
        raise ValueError("One or more required environment variables are missing.")

    PG_DSN = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    engine = create_async_engine(PG_DSN)
    Session = async_sessionmaker(bind=engine, expire_on_commit=False)  # expire_on_commit - по умолчанию True и означает
    # что сессия становиться не действительной после каждого commit. Мы его исправляем на False.
except Exception as e:
    print(f"An error occurred: {e}")


# Определение базового класса для ORM (Object-Relational Mapping) с использованием DeclarativeBase из SQLAlchemy
# и AsyncAttrs для поддержки асинхронных атрибутов.
class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = "swapi_people"
    id: int = Column(Integer, primary_key=True)
    birth_year: Optional[str] = Column(String)
    eye_color: Optional[str] = Column(String)
    films: Optional[str] = Column(String)
    gender: Optional[str] = Column(String)
    hair_color: Optional[str] = Column(String)
    height: Optional[float] = Column(Float)
    homeworld: Optional[str] = Column(String)
    mass: Optional[float] = Column(Float)
    name: Optional[str] = Column(String)
    skin_color: Optional[str] = Column(String)
    species: Optional[str] = Column(String)
    starships: Optional[str] = Column(String)
    vehicles: Optional[str] = Column(String)

    def __init__(self, json_data: dict):
        self.id = json_data.get('id')
        self.birth_year = json_data.get('birth_year')
        self.eye_color = json_data.get('eye_color')
        self.films = ', '.join(json_data.get('films', [])) if json_data.get('films') else None
        self.gender = json_data.get('gender')
        self.hair_color = json_data.get('hair_color')
        self.height = float(json_data.get('height')) if json_data.get('height') and json_data.get('height').isdigit() else None
        self.homeworld = json_data.get('homeworld')
        self.mass = float(json_data.get('mass')) if json_data.get('mass') and json_data.get('mass').isdigit() else None
        self.name = json_data.get('name')
        self.skin_color = json_data.get('skin_color')
        self.species = ', '.join(json_data.get('species', [])) if json_data.get('species') else None
        self.starships = ', '.join(json_data.get('starships', [])) if json_data.get('starships') else None
        self.vehicles = ', '.join(json_data.get('vehicles', [])) if json_data.get('vehicles') else None


# Асинхронная функция для инициализации ORM и создания всех необходимых таблиц в базе данных.
async def init_orm():
    async with engine.begin() as conn:  # Начало транзакции в базе данных через движок.
        # Выполнение синхронной операции внутри асинхронного контекста.
        # run_sync для асинхронного создания таблиц, так как сам метод create_all является синхронным.
        await conn.run_sync(Base.metadata.create_all)
