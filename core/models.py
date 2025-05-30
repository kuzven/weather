from django.db import models


class CitySearchHistory(models.Model):
    session_key = models.CharField(max_length=32, verbose_name="Ключ сессии", db_index=True)
    city_name = models.CharField(max_length=100, verbose_name="Название города")
    search_count = models.IntegerField(default=0, verbose_name="Количество запросов")

    def __str__(self):
        return f"{self.session_key}: {self.city_name} ({self.search_count} запросов)"

    class Meta:
        verbose_name = 'История поиска городов'
        verbose_name_plural = 'Истории поиска городов'
