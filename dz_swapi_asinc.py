import asyncio  # для асинхронного программирования
import aiohttp  # для работы с HTTP в асинхронном режиме.
import datetime  # для работы с датой и временем
from more_itertools import chunked  # для разделения списка на части.  # pip install more_itertools
from models import init_orm, SwapiPeople, Session
import requests
print("asinc.py")

max_requests = 5  # Определение максимального количества параллельных запросов


async def fetch_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def process_films(person_data):
    """Функция заходит по ссылкам в ключе 'films',
    извлекает название по ключу 'title', помещает через запятую названия вместо ссылок. """
    if 'films' in person_data:
        # Перебираем каждый фильм в списке films
        for i, film_url in enumerate(person_data['films']):
            # Отправляем запрос к API и получаем ответ
            response = requests.get(film_url)
            if response.status_code == 200:
                # Проверяем, что ответ содержит данные
                data = response.json()
                if 'title' in data:
                    # Заменяем URL на название фильма
                    person_data['films'][i] = data['title']
    return person_data


async def process_species(person_data):
    """Функция заходит по ссылкам в ключе 'species',
    извлекает название по ключу 'name', помещает через запятую названия вместо ссылок. """
    if 'species' in person_data:
        # Перебираем каждую разновидность в списке species
        for i, film_url in enumerate(person_data['species']):
            # Отправляем запрос к API и получаем ответ
            response = requests.get(film_url)
            if response.status_code == 200:
                # Проверяем, что ответ содержит данные
                data = response.json()
                if 'name' in data:
                    # Заменяем URL на название фильма
                    person_data['species'][i] = data['name']
    return person_data


async def process_starships(person_data):
    """Функция заходит по ссылкам в ключе 'starships',
    извлекает название по ключу 'name', помещает через запятую названия вместо ссылок. """
    if 'starships' in person_data:
        # Перебираем каждый фильм в списке films
        for i, starships_url in enumerate(person_data['starships']):
            # Отправляем запрос к API и получаем ответ
            response = requests.get(starships_url)
            if response.status_code == 200:
                # Проверяем, что ответ содержит данные
                data = response.json()
                if 'name' in data:
                    # Заменяем URL на название фильма
                    person_data['starships'][i] = data['name']
    return person_data


async def process_vehicles(person_data):
    """Функция заходит по ссылкам в ключе 'vehicles',
    извлекает название по ключу 'name', помещает через запятую названия вместо ссылок. """
    if 'vehicles' in person_data:
        # Перебираем каждый фильм в списке films
        for i, vehicles_url in enumerate(person_data['vehicles']):
            # Отправляем запрос к API и получаем ответ
            response = requests.get(vehicles_url)
            if response.status_code == 200:
                # Проверяем, что ответ содержит данные
                data = response.json()
                if 'name' in data:
                    # Заменяем URL на название фильма
                    person_data['vehicles'][i] = data['name']
    return person_data


async def get_people(http_session, person_id) -> list:
    """Заходит по ссылке, получает json, заменяет в указанных ключах, ссылки на называния."""
    response = await http_session.get(f"https://swapi.dev/api/people/{person_id}/")
    person_data = await response.json()

    await process_films(person_data)
    await process_species(person_data)
    await process_starships(person_data)
    await process_vehicles(person_data)
    print(person_data)
    return person_data


async def insert_to_database(json_list):
    """Вставляем данные в таблицу."""
    async with Session() as session:
        orm_objects = [SwapiPeople(json_data=item) for item in json_list]
        session.add_all(orm_objects)
        await session.commit()


async def main():
    """Основная асинхронная функция программы."""
    await init_orm()  # Наша функция из models.py
    http_session = aiohttp.ClientSession()  # Создание объекта aiohttp.ClientSession для управления HTTP-сессией
    try:
        for chunk_i in chunked(range(1, 100), max_requests):
            # Итерация по разбитому на части диапазону [1, 2, ..., 99] с максимум max_requests элементов в части
            coros = [get_people(http_session, i) for i in chunk_i]  # Создание списка корутин для каждого person_id в текущем chunk_i
            result = await asyncio.gather(*coros)  # Ожидание выполнения всех корутин и сбор результатов в список result
            print(result)
            await insert_to_database(result)  # Наша функция выше.
    finally:
        await http_session.close()  # Явное закрытие HTTP-сессии для избежания утечек ресурсов


start = datetime.datetime.now()  # Получение текущего времени перед запуском основной функции
asyncio.run(main())  # Запуск основной асинхронной функции main с помощью asyncio.run
print(datetime.datetime.now() - start)  # Вывод времени выполнения программы (разницы между текущим временем и start)
