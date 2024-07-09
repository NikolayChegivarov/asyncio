import asyncio  # для асинхронного программирования
import aiohttp  # для работы с HTTP в асинхронном режиме.
import datetime  # для работы с датой и временем
from more_itertools import chunked  # для разделения списка на части.  # pip install more_itertools
from models import init_orm
print("asinc.py")

max_requests = 5  # Определение максимального количества параллельных запросов


async def get_people(http_session, person_id):
    """
    Асинхронная функция для выполнения GET запроса к API SWAPI по указанному person_id.
    Возвращает JSON-ответ от сервера.
    """
    response = await http_session.get(f"https://swapi.dev/api/people/{person_id}/")
    json_data = await response.json()
    return json_data


async def main():
    """Основная асинхронная функция программы."""
    await init_orm()
    http_session = aiohttp.ClientSession()  # Создание объекта aiohttp.ClientSession для управления HTTP-сессией
    try:
        for chunk_i in chunked(range(1, 100), max_requests):
            # Итерация по разбитому на части диапазону [1, 2, ..., 99] с максимум max_requests элементов в части
            coros = [get_people(http_session, i) for i in chunk_i]  # Создание списка корутин для каждого person_id в текущем chunk_i
            result = await asyncio.gather(*coros)  # Ожидание выполнения всех корутин и сбор результатов в список result
            print(result)  # Вывод результатов каждой группы запросов (max_requests)
    finally:
        await http_session.close()  # Явное закрытие HTTP-сессии в блоке finally для избежания утечек ресурсов

start = datetime.datetime.now()  # Получение текущего времени перед запуском основной функции
asyncio.run(main())  # Запуск основной асинхронной функции main с помощью asyncio.run
print(datetime.datetime.now() - start)  # Вывод времени выполнения программы (разницы между текущим временем и start)
