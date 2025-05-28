import requests
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
    query = request.GET.get("query", "")
    if query:  # Если пользователь ввёл хотя бы один символ
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=5&language=ru"
        response = requests.get(url).json()

        # Формируем список городов для ответа
        cities = [{"name": city["name"], "latitude": city["latitude"], "longitude": city["longitude"]}
                  for city in response.get("results", [])]

        return JsonResponse({"cities": cities})

    return JsonResponse({"cities": []})  # Пустой список, если ничего не найдено


def get_weather(request):
    """
    Получение прогноза погоды на 3 дня через Open-Meteo API.
    Запрашивает сначала координаты города через Geocoding API, а затем прогноз погоды.

    Аргументы:
    - request: HTTP-запрос с параметром GET "city" (название города).

    Возвращает:
    - JSON-ответ с прогнозом температуры, ветра, осадков и облачности на 3 дня.
    """
    city_name = request.GET.get("city", "").strip()

    if not city_name:
        return JsonResponse({"error": "Название города не указано"})

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

    return JsonResponse({"city": city_name, "weather": weather_info})
