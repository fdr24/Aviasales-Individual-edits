# БЛОК ГОЛЯТКИН Д.К ИСУ-505046
# Этот модуль добавляет фильтры для поиска рейсов: самые быстрые, самые дешевые, прямые рейсы, рейсы с 1 пересадкой.
# Функция filter_flights() принимает список найденных маршрутов и режим фильтрации.
# Все данные (города и маршруты) импортируются из info.py для согласованности.

from datetime import datetime
from info import generate_random_tickets, get_routes_dict_from_tickets, MAJOR_CITIES


def get_routes(departure, destination, routes_dict, mode):
    """
    Находит рейсы (прямые + 1 пересадка).
    mode: 1 - быстрые, 2 - дешевые, 0 - все.
    Возвращает список [описание_маршрута, время, цена].
    Сохраняем совместимость с существующим кодом.
    """
    found_routes = []

    # Прямые рейсы
    if departure in routes_dict and destination in routes_dict[departure]:
        time, price = routes_dict[departure][destination]
        route_str = f"{departure} : {destination}"
        found_routes.append([route_str, time, price])

    # Рейсы с одной пересадкой
    if departure in routes_dict:
        for transfer_city in routes_dict[departure]:
            if (transfer_city in routes_dict and
                    destination in routes_dict[transfer_city] and
                    transfer_city != destination and
                    transfer_city != departure):
                time1, price1 = routes_dict[departure][transfer_city]
                time2, price2 = routes_dict[transfer_city][destination]

                total_time = time1 + time2
                total_price = price1 + price2
                route_str = f"{departure} : {transfer_city} : {destination}"

                found_routes.append([route_str, total_time, total_price])

    # Сортировка в зависимости от выбора
    if mode == 1:  # Самые быстрые
        found_routes.sort(key=lambda x: (x[1], x[2], x[0]))
    elif mode == 2:  # Самые дешевые
        found_routes.sort(key=lambda x: (x[2], x[1], x[0]))
    # mode == 0 - без сортировки (оставляем как есть)

    # Возвращаем не более 3 маршрутов наиболее удобных клиенту
    return found_routes[:3]


def find_flights(departure: str, destination: str, routes_dict, mode: int = 0):
    """
    Находит рейсы (прямые + 1 пересадка).
    mode: 0 - все, 1 - по времени, 2 - по цене.
    Возвращает список (описание_маршрута, время, цена).
    """
    found_routes = []

    # Прямые рейсы
    if departure in routes_dict and destination in routes_dict[departure]:
        time, price = routes_dict[departure][destination]
        route_str = f"{departure} : {destination}"
        found_routes.append((route_str, time, price))

    # Рейсы с 1 пересадкой
    if departure in routes_dict:
        for transfer_city in routes_dict[departure]:
            if (transfer_city in routes_dict and
                    destination in routes_dict[transfer_city] and
                    transfer_city != destination and
                    transfer_city != departure):
                time1, price1 = routes_dict[departure][transfer_city]
                time2, price2 = routes_dict[transfer_city][destination]

                total_time = time1 + time2
                total_price = price1 + price2
                route_str = f"{departure} : {transfer_city} : {destination}"

                found_routes.append((route_str, total_time, total_price))

    # Сортировка по режиму
    if mode == 1:  # Самые быстрые
        found_routes.sort(key=lambda x: (x[1], x[2]))  # по времени, затем по цене
    elif mode == 2:  # Самые дешевые
        found_routes.sort(key=lambda x: (x[2], x[1]))  # по цене, затем по времени
    # mode 0 - без сортировки (все)

    return found_routes


def filter_flights(departure: str, destination: str, filter_type: str = "all"):
    """
    САМОДОСТАТОЧНАЯ ФУНКЦИЯ-ФИЛЬТР ДЛЯ ВСТАВКИ В ОСНОВНОЙ КОД.
    filter_type: 'fastest' - самые быстрые, 'cheapest' - самые дешевые,
                 'direct' - только прямые, 'one_stop' - только 1 пересадка, 'all' - все.
    Использует данные из info.py.
    """
    # Проверяем, что города существуют в данных
    all_cities = [city["name"] for city in MAJOR_CITIES]
    if departure not in all_cities:
        raise ValueError(f"Город отправления '{departure}' не найден")
    if destination not in all_cities:
        raise ValueError(f"Город назначения '{destination}' не найден")

    # Генерация данных из info.py
    tickets = generate_random_tickets(count=2000)
    routes_dict = get_routes_dict_from_tickets(tickets)

    # Поиск всех рейсов
    all_flights = find_flights(departure, destination, routes_dict, mode=0)

    # Фильтрация по типу
    filtered = []
    if filter_type == "all":
        filtered = all_flights[:10]  # Топ-10
    elif filter_type == "fastest":
        fast_flights = find_flights(departure, destination, routes_dict, mode=1)
        filtered = fast_flights[:5]  # Топ-5 самых быстрых
    elif filter_type == "cheapest":
        cheap_flights = find_flights(departure, destination, routes_dict, mode=2)
        filtered = cheap_flights[:5]  # Топ-5 самых дешевых
    elif filter_type == "direct":
        for route in all_flights:
            # Проверяем, что это прямой рейс (только 1 " : " в описании)
            if route[0].count(" : ") == 1:
                filtered.append(route)
    elif filter_type == "one_stop":
        for route in all_flights:
            # Проверяем, что это рейс с 1 пересадкой (2 " : " в описании)
            if route[0].count(" : ") == 2:
                filtered.append(route)
    else:
        raise ValueError(f"Неизвестный тип фильтра: {filter_type}")

    return filtered

# КОНЕЦ БЛОКА ГОЛЯТКИН Д.К ИСУ-505046