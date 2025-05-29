from django.test import TestCase
from django.urls import reverse
from .models import CitySearchHistory


class WeatherEdgeCaseTests(TestCase):
    def test_get_weather_empty_city(self):
        """Тест запроса с пустым названием города."""
        response = self.client.get(reverse("get_weather"), {"city": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.json())

    def test_get_weather_none_city(self):
        """Тест запроса без параметра 'city'."""
        response = self.client.get(reverse("get_weather"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.json())

    def test_get_weather_long_city(self):
        """Тест запроса с очень длинным названием города."""
        long_city_name = "Город" * 100  # Очень длинная строка
        response = self.client.get(reverse("get_weather"), {"city": long_city_name})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.json())

    def test_get_weather_numeric_city(self):
        """Тест запроса с числовым значением вместо названия города."""
        response = self.client.get(reverse("get_weather"), {"city": "123456"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.json())

    def test_get_weather_special_chars(self):
        """Тест запроса с особыми символами."""
        response = self.client.get(reverse("get_weather"), {"city": "@#$%^&*"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.json())

    def test_get_weather_mixed_case(self):
        """Тест запроса с разным регистром букв."""
        response = self.client.get(reverse("get_weather"), {"city": "мОсКва"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("weather", response.json())  # API должно корректно обработать регистр


class AutocompleteCityTests(TestCase):
    def test_autocomplete_no_query(self):
        """Тест обработки запроса без параметра query."""
        response = self.client.get(reverse("autocomplete_city"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("cities"), [])

    def test_autocomplete_empty_query(self):
        """Тест обработки пустого значения query."""
        response = self.client.get(reverse("autocomplete_city"), {"query": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("cities"), [])

    def test_autocomplete_long_query(self):
        """Тест обработки слишком длинного запроса."""
        long_query = "Город" * 100  # 500 символов
        response = self.client.get(reverse("autocomplete_city"), {"query": long_query})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("cities"), [])

    def test_autocomplete_special_chars(self):
        """Тест обработки специальных символов в query."""
        response = self.client.get(reverse("autocomplete_city"), {"query": "@#$%^&*"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("cities"), [])

    def test_autocomplete_numeric_query(self):
        """Тест обработки числового значения вместо названия."""
        response = self.client.get(reverse("autocomplete_city"), {"query": "12345"})
        self.assertEqual(response.status_code, 200)
        cities = response.json().get("cities", [])

        for city in cities:
            self.assertFalse(city["name"].isdigit())  # Проверяем, что название города НЕ состоит только из цифр


class AutocompleteCityEdgeCaseTests(TestCase):
    def test_autocomplete_single_emoji(self):
        """Тест запроса с одиночным emoji."""
        response = self.client.get(reverse("autocomplete_city"), {"query": "🌍"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("cities"), [])

    def test_autocomplete_mixed_emoji(self):
        """Тест запроса с сочетанием букв и emoji."""
        response = self.client.get(reverse("autocomplete_city"), {"query": "Мос🌆"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("cities"), [])

    def test_autocomplete_multiple_emoji(self):
        """Тест запроса с множеством emoji подряд."""
        response = self.client.get(reverse("autocomplete_city"), {"query": "🔥🔥🔥"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("cities"), [])

    def test_autocomplete_special_symbols(self):
        """Тест запроса с редкими символами (✈️🏝️🚀)."""
        response = self.client.get(reverse("autocomplete_city"), {"query": "✈️🏝️🚀"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("cities"), [])
