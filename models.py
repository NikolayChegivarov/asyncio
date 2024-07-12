from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Float
import os
from dotenv import load_dotenv
from typing import Optional
import json

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


# Создание подкласса для модели данных в базе данных, наследуемого от базового класса Base
# Это определяет таблицу "swapi_people" в базе данных.
class SwapiPeople(Base):
    __tablename__ = "swapi_people"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[Optional[str]] = mapped_column(String)
    eye_color: Mapped[Optional[str]] = mapped_column(String)
    films: Mapped[Optional[str]] = mapped_column(String)
    gender: Mapped[Optional[str]] = mapped_column(String)
    hair_color: Mapped[Optional[str]] = mapped_column(String)
    height: Mapped[Optional[float]] = mapped_column(Float)
    homeworld: Mapped[Optional[str]] = mapped_column(String)
    mass: Mapped[Optional[float]] = mapped_column(Float)
    name: Mapped[Optional[str]] = mapped_column(String)
    skin_color: Mapped[Optional[str]] = mapped_column(String)
    species: Mapped[Optional[str]] = mapped_column(String)
    starships: Mapped[Optional[str]] = mapped_column(String)
    vehicles: Mapped[Optional[str]] = mapped_column(String)

    def __init__(self, json_data: dict):
        self.id = json_data.get('id')
        self.birth_year = json_data.get('birth_year')
        self.eye_color = json_data.get('eye_color')
        self.films = ', '.join(json_data.get('films', [])) if json_data.get('films') else None
        self.gender = json_data.get('gender')
        self.hair_color = json_data.get('hair_color')
        self.height = float(json_data.get('height')) if json_data.get('height') and json_data.get(
            'height').isdigit() else None
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
