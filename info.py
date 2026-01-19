import json
import random
import csv
import os
from typing import List, Dict, Any
from math import radians, cos, sin, asin, sqrt

# ДАННЫЕ: 40+ крупнейших городов Европы и Азии
MAJOR_CITIES = [
    # АЗИЯ
    {"name": "Токио", "country": "Япония", "lat": 35.6762, "lon": 139.6503},
    {"name": "Дели", "country": "Индия", "lat": 28.7041, "lon": 77.1025},
    {"name": "Шанхай", "country": "Китай", "lat": 31.2304, "lon": 121.4737},
    {"name": "Бангкок", "country": "Таиланд", "lat": 13.7563, "lon": 100.5018},
    {"name": "Пекин", "country": "Китай", "lat": 39.9042, "lon": 116.4074},
    {"name": "Сингапур", "country": "Сингапур", "lat": 1.3521, "lon": 103.8198},
    {"name": "Гонконг", "country": "Китай", "lat": 22.3193, "lon": 114.1694},
    {"name": "Манила", "country": "Филиппины", "lat": 14.5995, "lon": 120.9842},
    {"name": "Стамбул", "country": "Турция", "lat": 41.0082, "lon": 28.9784},
    {"name": "Карачи", "country": "Пакистан", "lat": 24.8607, "lon": 67.0011},
    {"name": "Куала-Лумпур", "country": "Малайзия", "lat": 3.1390, "lon": 101.6869},
    {"name": "Дубай", "country": "ОАЭ", "lat": 25.2048, "lon": 55.2708},
    {"name": "Бангалор", "country": "Индия", "lat": 12.9716, "lon": 77.5946},
    {"name": "Чэнду", "country": "Китай", "lat": 30.5728, "lon": 104.0668},
    {"name": "Сеул", "country": "Южная Кореа", "lat": 37.5665, "lon": 126.9780},
    # ЕВРОПА
    {"name": "Москва", "country": "Россия", "lat": 55.7558, "lon": 37.6173},
    {"name": "Лондон", "country": "Великобритания", "lat": 51.5074, "lon": -0.1278},
    {"name": "Париж", "country": "Франция", "lat": 48.8566, "lon": 2.3522},
    {"name": "Берлин", "country": "Германия", "lat": 52.5200, "lon": 13.4050},
    {"name": "Мадрид", "country": "Испания", "lat": 40.4168, "lon": -3.7038},
    {"name": "Рим", "country": "Италия", "lat": 41.9028, "lon": 12.4964},
    {"name": "Амстердам", "country": "Нидерланды", "lat": 52.3676, "lon": 4.9041},
    {"name": "Барселона", "country": "Испания", "lat": 41.3851, "lon": 2.1734},
    {"name": "Вена", "country": "Австрия", "lat": 48.2082, "lon": 16.3738},
    {"name": "Прага", "country": "Чехия", "lat": 50.0755, "lon": 14.4378},
    {"name": "Варшава", "country": "Польша", "lat": 52.2297, "lon": 21.0122},
    {"name": "Будапешт", "country": "Венгрия", "lat": 47.4979, "lon": 19.0402},
    {"name": "Афины", "country": "Греция", "lat": 37.9838, "lon": 23.7275},
    {"name": "Стокгольм", "country": "Швеция", "lat": 59.3293, "lon": 18.0686},
    {"name": "Цюрих", "country": "Швейцария", "lat": 47.3769, "lon": 8.5472},
    {"name": "Копенгаген", "country": "Дания", "lat": 55.6761, "lon": 12.5683},
    {"name": "Брюссель", "country": "Бельгия", "lat": 50.8503, "lon": 4.3517},
    {"name": "Лиссабон", "country": "Португалия", "lat": 38.7223, "lon": -9.1393},
    {"name": "Санкт-Петербург", "country": "Россия", "lat": 59.9311, "lon": 30.3609},
    {"name": "Киев", "country": "Украина", "lat": 50.4501, "lon": 30.5234},
    {"name": "Стамбул", "country": "Турция", "lat": 41.0082, "lon": 28.9784},
    {"name": "Бирмингем", "country": "Великобритания", "lat": 52.5086, "lon": -1.8755},
    # Дополнительные города России
    {"name": "Ростов-на-Дону", "country": "Россия", "lat": 47.2357, "lon": 39.7015},
    {"name": "Великий Новгород", "country": "Россия", "lat": 58.5215, "lon": 31.2756},
    {"name": "Самара", "country": "Россия", "lat": 53.2415, "lon": 50.2212},
    {"name": "Псков", "country": "Россия", "lat": 57.8194, "lon": 28.3318},
    {"name": "Казань", "country": "Россия", "lat": 55.7961, "lon": 49.1064},
    {"name": "Нижний Новгород", "country": "Россия", "lat": 56.2965, "lon": 43.9361},
    {"name": "Екатеринбург", "country": "Россия", "lat": 56.8389, "lon": 60.6057},
    {"name": "Магадан", "country": "Россия", "lat": 59.5680, "lon": 150.8077},
]

# Базовая ставка (в условных единицах) за 1 час полета
BASE_RATE = 50

# Минимальная и максимальная цена для реалистичности
MIN_PRICE = 50
MAX_PRICE = 1000


# ФУНКЦИИ

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Вычисляет расстояние между двумя точками на земле (в км) используя формулу Хаверсинуса.
    """
    # Радиус Земли в км
    R = 6371

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c


def distance_to_flight_time(distance_km: float) -> float:
    """
    Конвертирует расстояние (км) в время полета (часы).

    Средняя крейсерская скорость самолета: ~900 км/ч
    Добавляем 20% времени на взлет, посадку и маршрут
    """
    cruise_speed = 900  # км/ч
    flight_time = (distance_km / cruise_speed) * 1.2

    return round(flight_time, 1)


def calculate_ticket_price(
        flight_duration: float,
        base_rate: float = BASE_RATE,
        frequency_coefficient: float = None
) -> float:
    """
    Рассчитывает цену билета по формуле:
    цена = базовая_ставка * время_полета * коэффициент_частоты
    """
    if frequency_coefficient is None:
        frequency_coefficient = random.uniform(0.8, 1.5)

    price = base_rate * flight_duration * frequency_coefficient
    price = max(MIN_PRICE, min(price, MAX_PRICE))

    return round(price, 2)


def generate_random_tickets(count: int = 2000) -> List[Dict[str, Any]]:
    tickets = []

    for _ in range(count):
        # Выбираем два разных города
        city_from = random.choice(MAJOR_CITIES)
        city_to = random.choice(MAJOR_CITIES)

        while city_to["name"] == city_from["name"]:
            city_to = random.choice(MAJOR_CITIES)

        # Вычисляем расстояние и время полета
        distance = haversine_distance(
            city_from["lat"], city_from["lon"],
            city_to["lat"], city_to["lon"]
        )

        flight_duration = distance_to_flight_time(distance)

        # День в расписании: 1..14 (две недели)
        day = random.randint(1, 14)
        weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        weekday = weekdays[(day - 1) % 7]

        # Рассчитываем цену билета
        price = calculate_ticket_price(flight_duration)

        # Увеличиваем цену на 20% в субботу/воскресенье
        if day in {6, 7, 13, 14}:
            price = round(price * 1.2, 2)
            price = max(MIN_PRICE, min(price, MAX_PRICE))

        ticket = {
            "from": city_from["name"],
            "to": city_to["name"],
            "duration_hours": flight_duration,
            "price": price,
            "day": day,
            "weekday": weekday
        }

        tickets.append(ticket)

    return tickets


def generate_tickets_json(count: int = 10, indent: int = 2) -> str:
    """
    Генерирует список билетов и возвращает в формате JSON.
    """
    tickets = generate_random_tickets(count)
    return json.dumps(tickets, ensure_ascii=False, indent=indent)


def save_tickets_to_csv(tickets: List[Dict[str, Any]], file_path: str) -> None:
    """
    Сохраняет список билетов в CSV-файл.
    """
    fieldnames = ["from", "to", "duration_hours", "price", "day", "weekday"]

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for t in tickets:
            writer.writerow({k: t.get(k, "") for k in fieldnames})


def get_routes_dict_from_tickets(tickets: List[Dict[str, Any]]) -> dict:
    """
    Преобразует список билетов в словарь routes для get_routes.
    Возвращает словарь в формате: {city: {destination: (time, price)}}
    """
    routes_dict = {}

    for ticket in tickets:
        from_city = ticket["from"]
        to_city = ticket["to"]

        if from_city not in routes_dict:
            routes_dict[from_city] = {}

        routes_dict[from_city][to_city] = (
            ticket["duration_hours"],
            ticket["price"]
        )

    return routes_dict
