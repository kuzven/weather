import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import CitySearchHistory


def index(request):
    """
    Главная страница сайта. Отображает форму для ввода города и прогноз погоды.
    """
    return render(request, "core/weather.html")


def autocomplete_city(request):
    """
    Обработчик автодополнения названий городов.
    Запрашивает данные из Open-Meteo Geocoding API и возвращает список городов на русском языке.
    
    Аргументы:
    - request: HTTP-запрос с параметром GET "query" (введённое название города).
    
    Возвращает:
    - JSON-ответ со списком городов, содержащим название, широту и долготу.
    """
    query = request.GET.get("query", "").strip()
    if query:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=5&language=ru"
        response = requests.get(url).json()

        results = response.get("results", [])

        if not results:
            return JsonResponse({"cities": []})  # Если API ничего не вернул, отправляем пустой список

        # Фильтруем уникальные названия городов через set
        unique_cities = set()
        cities = []

        for city in results:
            city_name = city["name"]
            if city_name not in unique_cities:
                unique_cities.add(city_name)  # Добавляем город в множество (убираем дубликаты)
                cities.append({
                    "name": city_name,
                    "latitude": city["latitude"],
                    "longitude": city["longitude"]
                })

        return JsonResponse({"cities": cities})

    return JsonResponse({"cities": []})


def get_weather(request):
    """
    Получение прогноза погоды на 3 дня через Open-Meteo API.
    Запрашивает сначала координаты города через Geocoding API, а затем прогноз погоды.
    Сохраняет последний введённый город в сессии пользователя.
    Записывает историю поиска и увеличивает счётчик запросов.
    """
    city_name = request.GET.get("city", "").strip()

    if not city_name:
        return JsonResponse({"error": "Название города не указано"})

    # Запоминаем последний введённый город в сессии пользователя
    request.session["last_city_name"] = city_name

    # Запрашиваем координаты города
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ru"
    geo_response = requests.get(geo_url).json()
    results = geo_response.get("results", [])

    if not results:
        return JsonResponse({"error": "Город не найден"})

    latitude = results[0]["latitude"]
    longitude = results[0]["longitude"]

    # Запрашиваем прогноз погоды по координатам
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,cloudcover_mean&timezone=Europe/Moscow&language=ru"
    weather_response = requests.get(weather_url).json()
    forecast = weather_response.get("daily", {})

    weather_info = [
        {
            "date": forecast.get("time", [""])[i],
            "temperature_max": forecast.get("temperature_2m_max", [None])[i],
            "temperature_min": forecast.get("temperature_2m_min", [None])[i],
            "wind_speed": round(forecast.get("wind_speed_10m_max", [None])[i] / 3.6, 1),
            "precipitation": forecast.get("precipitation_sum", [None])[i],
            "cloud_cover": forecast.get("cloudcover_mean", [None])[i],
        }
        for i in range(3)  # Берем прогноз на 3 дня
    ]

    # Записываем историю поиска
    city_entry, created = CitySearchHistory.objects.get_or_create(city_name=city_name)
    city_entry.search_count += 1  # Увеличиваем количество запросов
    city_entry.save()

    return JsonResponse({"city": city_name, "weather": weather_info})


def get_last_city(request):
    """
    Получение последнего введённого города из сессии пользователя.
    """
    last_city_name = request.session.get("last_city_name", None)
    return JsonResponse({"last_city_name": last_city_name})


def get_search_history(request):
    """
    Возвращает список городов и количество их запросов.
    """
    history = CitySearchHistory.objects.all().values("city_name", "search_count")
    return JsonResponse({"history": list(history)})


def search_history(request):
    """
    Отображает историю поиска только для текущего session_key.
    """
    # Получаем session_key текущего пользователя
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # Фильтруем историю только для текущего session_key
    search_history = CitySearchHistory.objects.filter(session_key=session_key).order_by("-search_count")

    return render(request, "core/search_history.html", {"search_history": search_history})


def search_city(request):
    """
    Сохраняет историю поиска для каждого уникального устройства (по session_key).
    Возвращает список запрашиваемых городов.
    """
    # Генерируем новый session_key, если его нет
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    city_name = request.GET.get("city_name", "").strip()
    if not city_name:
        return JsonResponse({"error": "Название города не указано"})

    # Проверяем, существует ли запись с этим session_key
    city_entry = CitySearchHistory.objects.filter(session_key=session_key, city_name=city_name).first()
    if city_entry:
        city_entry.search_count += 1  # Увеличиваем, если запись уже есть
        city_entry.save()
    else:
        CitySearchHistory.objects.create(session_key=session_key, city_name=city_name, search_count=1)  # Создаём новую запись

    # Получаем историю поиска текущего устройства
    history = CitySearchHistory.objects.filter(session_key=session_key).order_by("-search_count")

    return JsonResponse({"history": list(history.values("city_name", "search_count"))})
