import requests
from django.shortcuts import render
from django.http import JsonResponse
from .models import CitySearchHistory


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
    Запрашивает данные по координатам города.

    Аргументы:
    - request: HTTP-запрос с параметрами GET "lat" (широта) и "lon" (долгота).

    Возвращает:
    - JSON-ответ с прогнозом температуры, ветра, осадков и облачности на 3 дня.
    """
    latitude = request.GET.get("lat")
    longitude = request.GET.get("lon")

    if latitude and longitude:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,cloudcover_mean&timezone=Europe/Moscow&language=ru"
        response = requests.get(url).json()

        # Извлекаем данные о погоде
        forecast = response.get("daily", {})
        weather_info = []

        for i in range(3):  # Берем прогноз на 3 ближайших дня
            weather_info.append({
                "date": forecast.get("time", [""])[i],  # Дата прогноза
                "temperature_max": forecast.get("temperature_2m_max", [None])[i],  # Максимальная температура
                "temperature_min": forecast.get("temperature_2m_min", [None])[i],  # Минимальная температура
                "wind_speed": round(forecast.get("wind_speed_10m_max", [None])[i] / 3.6, 1),  # Скорость ветра (перевод в м/с)
                "precipitation": forecast.get("precipitation_sum", [None])[i],  # Осадки (мм)
                "cloud_cover": forecast.get("cloudcover_mean", [None])[i],  # Средняя облачность (%)
            })

        return JsonResponse({"city": request.GET.get("city", ""), "weather": weather_info})

    return JsonResponse({"error": "Город не найден"})
