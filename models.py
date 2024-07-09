
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Float
import os
from dotenv import load_dotenv

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
        f"postgresql+asyncio://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    engine = create_async_engine(PG_DSN)
    Session = async_sessionmaker(engine)
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
    birth_year = mapped_column(String)
    eye_color = mapped_column(String)
    films = mapped_column(String)  # Строка с названиями фильмов через запятую
    gender = mapped_column(String)
    hair_color = mapped_column(String)
    height = mapped_column(Float)
    homeworld = mapped_column(String)
    mass = mapped_column(Float)
    name = mapped_column(String)
    skin_color = mapped_column(String)
    species = mapped_column(String)  # Строка с названиями типов через запятую
    starships = mapped_column(String)  # Строка с названиями кораблей через запятую
    vehicles = mapped_column(String)


# Асинхронная функция для инициализации ORM и создания всех необходимых таблиц в базе данных.
async def init_orm():
    async with engine.begin() as conn:  # Начало транзакции в базе данных через движок.
        # Выполнение синхронной операции внутри асинхронного контекста.
        # Это необходимо для создания таблиц, так как сам метод create_all является синхронным.
        await conn.run_sync(Base.metadata.create_all)
